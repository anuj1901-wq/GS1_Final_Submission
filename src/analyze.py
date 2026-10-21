"""Rebuild GS1 metrics from the two private raw extracts. Python 3.10+."""
from pathlib import Path
import argparse, json
import numpy as np
import pandas as pd

AS_OF = pd.Timestamp('2026-10-20')
NULLS = ['', 'NULL', 'NULQ', 'nan', 'NaN', 'None', 'NA']

def load_csv(path):
    return pd.read_csv(path, dtype=str, keep_default_na=False, low_memory=False).replace(NULLS, pd.NA)

def dates(series):
    s = series.astype('string').str.strip()
    d = pd.to_datetime(s, format='%d-%m-%Y', errors='coerce')
    d = d.fillna(pd.to_datetime(s, format='%d/%m/%Y', errors='coerce'))
    return d.fillna(pd.to_datetime(s, format='%Y-%m-%d', errors='coerce'))

def timestamp(series):
    # Normalize all activity timestamps to UTC calendar dates.
    return pd.to_datetime(series, utc=True, errors='coerce', format='mixed').dt.tz_localize(None).dt.normalize()

def run(root, out):
    out.mkdir(parents=True, exist_ok=True)
    a=load_csv(root/'gtin_activity.csv'); s=load_csv(root/'subscriptions.csv')
    for d in (a,s):
        for c in ['gcp','company_id']:
            d[c]=d[c].astype('string').str.strip()
    for c in ['gcp_registered_date','subscription_start_date','subscription_end_date']:
        s[c+'_parsed']=dates(s[c])
    for c in ['first_gtin_created_at','last_gtin_created_at']:
        a[c+'_parsed']=timestamp(a[c])
    a['total_gtins_num']=pd.to_numeric(a.total_gtins,errors='coerce')
    ag=a.groupby('gcp',dropna=False).size(); sg=s.groupby('gcp',dropna=False).size()
    ambiguous=set(ag[ag>1].index)|set(sg[sg>1].index)
    ambiguous.discard('0')
    a1=a[~a.gcp.isin(ambiguous) & a.gcp.notna() & (a.gcp!='0')].copy()
    s1=s[~s.gcp.isin(ambiguous) & s.gcp.notna() & (s.gcp!='0')].copy()
    # Preserve unmatched rows, and prevent many-to-many joins.
    assert a1.gcp.is_unique and s1.gcp.is_unique
    m=s1.merge(a1,on='gcp',how='outer',suffixes=('_sub','_activity'),indicator=True,validate='one_to_one')
    m['company_id']=m.company_id_sub.combine_first(m.company_id_activity)
    m['company_name']=m.company_name_sub.combine_first(m.company_name_activity)
    m['identity_mismatch']=m.company_id_sub.notna() & m.company_id_activity.notna() & (m.company_id_sub!=m.company_id_activity)
    m['invalid_period']=m.subscription_end_date_parsed.lt(m.subscription_start_date_parsed)
    m['first_date']=m.first_gtin_created_at_parsed
    m['last_date']=m.last_gtin_created_at_parsed
    m['registered']=m.gcp_registered_date_parsed
    m['end']=m.subscription_end_date_parsed
    m['days_to_first']=(m.first_date-m.registered).dt.days
    m['days_since_last']=(AS_OF-m.last_date).dt.days
    m['days_to_expiry']=(m.end-AS_OF).dt.days
    m['gtins']=m.total_gtins_num
    matched=m['_merge'].eq('both')
    zero=matched & m.gtins.eq(0)
    m['engagement']=np.select([zero,matched & m.last_date.gt(AS_OF),matched & m.last_date.notna() & m.days_since_last.le(90),matched & m.days_since_last.le(180),matched & m.last_date.notna()],['NEVER ACTIVATED','FUTURE ACTIVITY','ACTIVE','QUIET','DORMANT'],default='UNKNOWN')
    m.loc[~matched,'engagement']='ACTIVITY NOT OBSERVED' if False else 'UNMATCHED'
    m['post_expiry']=matched & ~m.invalid_period & m.end.notna() & m.last_date.gt(m.end) & m.last_date.le(AS_OF)
    scoreable=matched & ~m.identity_mismatch & ~m.invalid_period & m.company_id.notna() & m.end.notna() & m.registered.le(AS_OF) & m.end.ge(m.registered) & m.gtins.ge(0) & (m.last_date.isna()|m.last_date.le(AS_OF)) & (m.first_date.isna()|m.first_date.le(AS_OF))
    m['scoreable']=scoreable
    urgency=np.select([m.days_to_expiry.lt(0),m.days_to_expiry.le(30),m.days_to_expiry.le(90)],[40,35,25],default=0)
    engagement=np.select([m.engagement.isin(['DORMANT','NEVER ACTIVATED']),m.engagement.eq('QUIET')],[30,20],default=0)
    activation=np.select([zero,m.days_to_first.gt(90),m.days_to_first.between(31,90)],[20,15,8],default=0)
    usage=np.select([m.gtins.eq(0),m.gtins.between(1,10),m.gtins.between(11,50)],[10,7,4],default=0)
    m['score']=pd.Series(urgency+engagement+activation+usage,index=m.index).where(scoreable)
    m['priority']=pd.cut(m.score,[-1,24,49,74,100],labels=['LOW','MEDIUM','HIGH','CRITICAL']).astype('string').fillna('REVIEW REQUIRED')
    valid=m[matched & ~m.identity_mismatch]
    engagement_summary=valid.groupby('engagement').size().rename('gcps').reset_index()
    engagement_summary.to_csv(out/'engagement_aggregate.csv',index=False)
    m.groupby('priority',dropna=False).agg(gcps=('gcp','size'),avg_score=('score','mean')).reset_index().to_csv(out/'score_aggregate.csv',index=False)
    companies=m[m.company_id.notna()].groupby('company_id').agg(gcps=('gcp','size'),max_score=('score','max'),review_gcps=('scoreable',lambda x:(~x).sum()))
    company_priority=pd.cut(companies.max_score,[-1,24,49,74,100],labels=['LOW','MEDIUM','HIGH','CRITICAL']).astype('string').fillna('REVIEW REQUIRED')
    company_priority.value_counts().rename_axis('priority').reset_index(name='companies').to_csv(out/'company_priority_aggregate.csv',index=False)
    # No company names, IDs or raw GCPs are exported.
    summary={
      'as_of':'2026-10-20','raw_gtin_rows':len(a),'raw_subscription_rows':len(s),
      'raw_gtin_distinct_gcp':int(a.gcp.nunique()),'raw_subscription_distinct_gcp':int(s.gcp.nunique()),
      'sentinel_gcp_zero_rows':int((a.gcp=='0').sum()+(s.gcp=='0').sum()),
      'ambiguous_nonzero_gcps':len(ambiguous),
      'missing_registration_parsed':int(s.gcp_registered_date_parsed.isna().sum()),
      'missing_expiry_parsed':int(s.subscription_end_date_parsed.isna().sum()),
      'invalid_subscription_period_rows':int((s.subscription_end_date_parsed<s.subscription_start_date_parsed).sum()),
      'model_gcps':len(m),'matched_gcps':int(matched.sum()),'subscription_only_gcps':int((m._merge=='left_only').sum()),'activity_only_gcps':int((m._merge=='right_only').sum()),
      'company_id_mismatch_gcps':int(m.identity_mismatch.sum()),'scored_gcps':int(scoreable.sum()),'review_required_gcps':int((~scoreable).sum()),
      'validated_engagement_gcps':len(valid),'quiet_dormant_never_gcps':int(valid.engagement.isin(['QUIET','DORMANT','NEVER ACTIVATED']).sum()),
      'post_expiry_evidence_gcps':int(m.post_expiry.sum()),
      'expired_gcps':int((matched & ~m.identity_mismatch & ~m.invalid_period & m.end.lt(AS_OF)).sum()),
      'companies_in_model':int(m.company_id.nunique()),
      'score_sensitivity_changed':int((scoreable & ((m.score>=50)!=((m.score-usage)>=50))).sum())
    }
    (out/'metrics.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))
    return summary

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--data-dir',type=Path,default=Path(__file__).resolve().parents[1]/'data'); p.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parents[1]/'outputs'); x=p.parse_args(); run(x.data_dir,x.output_dir)
