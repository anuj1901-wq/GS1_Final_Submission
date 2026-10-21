from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from pathlib import Path
out=Path(__file__).resolve().parent/'reports'/'CEO_Memo.pdf'
navy=colors.HexColor('#193149'); teal=colors.HexColor('#187C95'); grey=colors.HexColor('#4F5F6A')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='MemoTitleX',fontName='Helvetica-Bold',fontSize=17,leading=21,textColor=navy,spaceAfter=7))
styles.add(ParagraphStyle(name='MemoSubX',fontName='Helvetica',fontSize=9,leading=13,textColor=grey,spaceAfter=14))
styles.add(ParagraphStyle(name='MemoHeadX',fontName='Helvetica-Bold',fontSize=11,leading=14,textColor=navy,spaceBefore=12,spaceAfter=5))
styles.add(ParagraphStyle(name='MemoBodyX',fontName='Helvetica',fontSize=9.5,leading=14,spaceAfter=7))
styles.add(ParagraphStyle(name='MemoSmallX',fontName='Helvetica',fontSize=8,leading=11,textColor=grey,spaceAfter=4))
doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=47,leftMargin=47,topMargin=43,bottomMargin=42)
S=[]
def add(t,style='MemoBodyX'):S.append(Paragraph(t,styles[style]))
add('GS1 INDIA | CUSTOMER INTELLIGENCE','MemoTitleX')
add('CEO decision memo  |  20 October 2026 snapshot  |  Synthetic source extracts','MemoSubX')
add('<b>Decision in one line:</b> Pilot targeted activation and renewal outreach, while auditing a small set of post-expiry records. Do not equate GTIN-creation inactivity with lost customer value.')
add('1  Engagement opportunity is large; value loss is unproven','MemoHeadX')
add('<b>26,718 / 37,419 GCPs (71.4%)</b> in the validated matched population are quiet (4,250), dormant (18,190) or have zero recorded GTINs (4,278). GTIN creation may be episodic; previously issued barcodes can continue to deliver value. <b>Risk:</b> an untargeted retention campaign could misclassify healthy customers.')
add('2  Post-expiry creation merits focused investigation','MemoHeadX')
add('<b>14 / 1,133 expired GCPs (1.24%)</b> have a last GTIN creation date after the recorded subscription expiry. The extracts do not contain complete renewal history or access logs. <b>Risk:</b> potential entitlement control gaps, but no demonstrated unauthorized access or quantifiable leakage.')
add('3  Usage differs by plan; headroom is not measurable','MemoHeadX')
add('Median cumulative GTINs: <b>Basic 25; Premium 42; Trace 23</b>. This supports plan-level segmentation, not a claim that a GCP is near capacity. GCP allocation limits, entitlements and prices are absent. <b>Opportunity:</b> investigate high-volume accounts for appropriate plans; revenue uplift cannot yet be estimated.')
add('One recommendation | 30-day targeted pilot','MemoHeadX')
add('<b>Owner:</b> Head of Commercial, supported by Product and Data. Prioritize upcoming renewals with unobserved activation or prolonged GTIN-creation inactivity; run a comparison/holdout group; separately reconcile the 14 post-expiry cases against renewal and access records. <b>Measure:</b> incremental renewal conversion, contact cost and confirmed entitlement exceptions. <b>Value at stake:</b> not monetizable from these extracts alone; obtain plan fees and renewal outcomes first.')
S.append(Spacer(1,10))
add('Evidence note: 37,477 GCPs in cleaned model; 37,410 scoreable; 67 require review. GCP is not identical to customer/company. Duplicate GCPs, sentinel GCP 0, and inconsistent dates were flagged or quarantined. Fixed analysis date makes results reproducible.','MemoSmallX')
doc.build(S)
print(out)
