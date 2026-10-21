"""GS1 aggregate-only customer intelligence dashboard. No raw/company-level records."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title='GS1 | Customer Intelligence',page_icon='📊',layout='wide')
st.markdown('''<style>.block-container{padding-top:1.5rem;max-width:1200px}div[data-testid="stMetric"]{background:#f5f8fc;padding:14px;border-radius:12px}h1{font-size:2.1rem!important}</style>''',unsafe_allow_html=True)
DATA=Path(__file__).resolve().parent/'data'
@st.cache_data
def load(name):
    return pd.read_csv(DATA/f'{name}.csv')

priority=load('priority'); engagement=load('engagement'); plans=load('plans')
adoption=load('adoption'); expiry=load('expiry'); kpis=load('kpis').iloc[0]
scores=load('score_distribution')
st.title('GS1 Customer Intelligence')
st.caption('Analysis as of 20 October 2026 · Synthetic data · Aggregate-only leadership view')
st.info('A quiet GCP does not necessarily represent a dissatisfied customer. Post-expiry last-GTIN timestamps are evidence of possible post-expiry creation, not proof of unauthorized access.')
page=st.radio('Explore', ['Executive overview','Adoption & engagement','Plan fit & expiry','Renewal scoring'],horizontal=True)
if page=='Executive overview':
    a,b,c,d=st.columns(4)
    a.metric('GCPs in model',f"{int(kpis['TOTAL_GCPS']):,}")
    b.metric('Companies in model',f"{int(kpis['UNIQUE_COMPANIES']):,}")
    c.metric('Never activated (all model)',f"{int(kpis['NEVER_ACTIVATED']):,}")
    d.metric('Post-expiry evidence',f"{int(kpis['POST_EXPIRY_ACTIVITY_GCPS']):,}")
    st.subheader('Engagement distribution (matched, identity-consistent GCPs)')
    fig=px.bar(engagement,x='ENGAGEMENT_SEGMENT',y='TOTAL_GCPS',text='TOTAL_GCPS',labels={'ENGAGEMENT_SEGMENT':'Engagement','TOTAL_GCPS':'GCPs'})
    st.plotly_chart(fig,use_container_width=True)
    st.subheader('Company renewal priority')
    fig=px.bar(priority,x='CUSTOMER_PRIORITY',y='TOTAL_COMPANIES',text='TOTAL_COMPANIES',labels={'CUSTOMER_PRIORITY':'Priority','TOTAL_COMPANIES':'Companies'})
    st.plotly_chart(fig,use_container_width=True)
elif page=='Adoption & engagement':
    st.subheader('Activation within 30 days by registration cohort')
    fig=px.line(adoption,x='REGISTRATION_YEAR',y='ADOPTION_30D_PCT',markers=True,labels={'REGISTRATION_YEAR':'Registration year','ADOPTION_30D_PCT':'30-day adoption (%)'})
    st.plotly_chart(fig,use_container_width=True)
    st.caption('Older cohorts and small cohorts are omitted from this public chart. Trend is descriptive, not causal.')
    st.subheader('GTIN creation recency')
    fig=px.bar(engagement,x='ENGAGEMENT_SEGMENT',y='TOTAL_GCPS',color='ENGAGEMENT_SEGMENT',labels={'ENGAGEMENT_SEGMENT':'Segment','TOTAL_GCPS':'GCPs'})
    st.plotly_chart(fig,use_container_width=True)
elif page=='Plan fit & expiry':
    st.subheader('Median and 90th percentile GTINs by plan')
    fig=px.bar(plans.melt(id_vars=['PLAN'],value_vars=['MEDIAN_GTINS','P90_GTINS'],var_name='Statistic',value_name='GTINs'),x='PLAN',y='GTINs',color='Statistic',barmode='group')
    st.plotly_chart(fig,use_container_width=True)
    st.caption('Without plan entitlement and pricing data, plan mismatch and remaining GCP capacity cannot be confirmed.')
    st.subheader('Post-expiry creation evidence')
    a,b=st.columns(2)
    a.metric('Post-expiry evidence, all plans',f"{int(kpis['POST_EXPIRY_ACTIVITY_GCPS']):,}")
    b.metric('Expired GCPs, all model',f"{int(kpis['EXPIRED_GCPS']):,}")
    fig=px.bar(expiry,x='PLAN',y=['EXPIRED_GCPS','POST_EXPIRY_ACTIVITY_GCPS'],barmode='group',labels={'value':'GCPs','variable':'Status'})
    st.plotly_chart(fig,use_container_width=True)
    st.caption('Only plan groups with at least 10 expired GCPs are shown; small groups are suppressed. Overall KPIs use the full model.')
else:
    st.subheader('Company renewal priority distribution')
    fig=px.bar(priority,x='CUSTOMER_PRIORITY',y='TOTAL_COMPANIES',text='TOTAL_COMPANIES')
    st.plotly_chart(fig,use_container_width=True)
    st.subheader('GCP-level score validation')
    st.dataframe(scores,hide_index=True,use_container_width=True)
    st.caption('37,410 scored GCPs; 67 require review. Removing usage weighting changed 1,087 high-priority classifications (2.9% of scored GCPs). Scores are prioritization heuristics, not churn probabilities.')
st.divider()
st.caption('Source: validated Snowflake aggregate exports. No GCP, company IDs, names, or raw records are shipped with this app.')
