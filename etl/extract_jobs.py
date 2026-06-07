import requests
import pandas as pd

URL = "https://www.arbeitnow.com/api/job-board-api"


def fetch_jobs():
    response = requests.get(URL)

    if response.status_code != 200:
        raise Exception("Failed to fetch jobs")

    jobs = response.json()["data"]

    records = []

    for job in jobs:
        records.append({
            "title": job.get("title"),
            "company": job.get("company_name"),
            "location": job.get("location"),
            "description": job.get("description"),
            "job_url": job.get("url"),
            "date_posted": job.get("created_at"),
            "employment_type": ",".join(job.get("job_types", [])),
            "source": "ArbeitNow"
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    df = fetch_jobs()

    print(df.head())
    print(f"\nFetched {len(df)} jobs")