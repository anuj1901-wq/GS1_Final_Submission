from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from analyze import dates
import pandas as pd

def test_mixed_dates():
    x=dates(pd.Series(['28-08-2024','2/11/2015','2026-10-20','not-a-date']))
    assert str(x.iloc[0].date())=='2024-08-28'
    assert str(x.iloc[1].date())=='2015-11-02'
    assert str(x.iloc[2].date())=='2026-10-20'
    assert pd.isna(x.iloc[3])
