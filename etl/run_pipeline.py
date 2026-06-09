from etl.extract_jobs import fetch_jobs
from etl.transform_jobs import extract_skills
from etl.load_jobs import load_job

df = fetch_jobs()

print(f"Fetched {len(df)} jobs")

for _, row in df.iterrows():

    job = row.to_dict()

    job["skills"] = extract_skills(
        str(job.get("description", ""))
    )

    load_job(job)

print("Pipeline completed.")