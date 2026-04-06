from src.access.get_measurements import get_measurements_by_site
from datetime import datetime, timedelta

ACTIVE_CUTOFF = datetime(2024, 1, 1)
SGMA_DATE = datetime(2014, 9, 16)
GWE_CHANGE_THRESHOLD = 2

def parse_date(msmt_date):
    return datetime.strptime(msmt_date, "%Y-%m-%dT%H:%M:%S")

def classify_trend(site_score):
    if site_score > GWE_CHANGE_THRESHOLD:
        return "🟢 Improving"
    elif site_score < -GWE_CHANGE_THRESHOLD:
        return "🔴 Declining"
    else:
        return "🟡 Stable"

def classify_confidence(site_confidence):
    if site_confidence >= 20:
        return "🟢 High"
    elif site_confidence >= 10:
        return "🟡 Moderate"
    else:
        return "🔴 Low"

def compute_site_stats(site_code):
    rows = get_measurements_by_site(site_code)

    parsed = [
        (parse_date(d), gwe)
        for d, gwe in rows
        if gwe is not None
    ]

    if not parsed:
        return None, None

    latest_date = max(d for d, _ in parsed)
    if latest_date < ACTIVE_CUTOFF:
        return None, None

    today = latest_date

    recent_cutoff = SGMA_DATE
    past_cutoff = SGMA_DATE - timedelta(days=(today - SGMA_DATE).days)

    recent = [gwe for d, gwe in parsed if d >= recent_cutoff]
    past = [gwe for d, gwe in parsed if past_cutoff <= d < recent_cutoff]

    if len(recent) < 5 or len(past) < 5:
        return None, None

    recent_avg = sum(recent) / len(recent)
    past_avg = sum(past) / len(past)

    score = recent_avg - past_avg
    confidence = min(len(recent),len(past))

    return score, confidence

if __name__ == "__main__":
    compute_site_stats("320000N1140000W001")
    compute_site_stats("325536N1170608W001")