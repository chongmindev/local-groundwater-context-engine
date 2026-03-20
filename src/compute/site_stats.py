from src.access.get_measurements import get_measurements_by_site
from datetime import datetime, timedelta

EXPECTED_PER_YEAR = 12

def parse_date(msmt_date):
    return datetime.strptime(msmt_date, "%Y-%m-%dT%H:%M:%S")

def compute_site_stats(site_code):
    rows = get_measurements_by_site(site_code)
    parsed = [(parse_date(d), gwe) for d, gwe in rows if gwe is not None]
    today = datetime.today()
    recent_cutoff = today - timedelta(days=365)
    past_cutoff = today - timedelta(days=365*2)
    recent = [gwe for d, gwe in parsed if d >= recent_cutoff]
    past = [gwe for d, gwe in parsed if past_cutoff <= d < recent_cutoff]
    confidence = min(len(recent), len(past)) / EXPECTED_PER_YEAR

    if len(recent) == 0 or len(past) == 0:
        return None, confidence
    recent_avg = sum(recent)/len(recent)
    past_avg = sum(past)/len(past)
    score = (recent_avg - past_avg)

    print(recent)
    print(past)
    print(score, confidence)

    return score, confidence

if __name__ == "__main__":
    compute_site_stats("320000N1140000W001")
    compute_site_stats("325536N1170608W001")