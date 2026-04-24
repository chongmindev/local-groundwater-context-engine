from src.access.get_measurements import get_measurements_by_site
from datetime import datetime, timedelta
from scipy.stats import mannwhitneyu

ACTIVE_CUTOFF = datetime(2024, 1, 1)
SGMA_DATE = datetime(2014, 9, 16)

def parse_date(msmt_date):
    return datetime.strptime(msmt_date, "%Y-%m-%dT%H:%M:%S")

def classify(change, p_value):
    if p_value < 0.05 and change > 0:
        return "🟢 Significant Increase"
    elif p_value < 0.05 and change < 0:
        return "🔴 Significant Decrease"
    else:
        return "🟡 No Significant Change"

def compute_site_stats(site_code):
    rows = get_measurements_by_site(site_code)

    parsed = [
        (parse_date(d), gwe)
        for d, gwe in rows
        if gwe is not None
    ]

    if not parsed:
        return None

    latest_date = max(d for d, _ in parsed)
    if latest_date < ACTIVE_CUTOFF:
        return None

    pre = [gwe for d, gwe in parsed if d < SGMA_DATE]
    post = [gwe for d, gwe in parsed if d >= SGMA_DATE]

    if len(pre) < 5 or len(post) < 5:
        return None

    pre_med = sum(pre)/len(pre)
    post_med = sum(post)/len(post)

    change = post_med - pre_med

    stat, p = mannwhitneyu(pre, post, alternative="two-sided")

    return {
        "change": change,
        "p_value": p
    }