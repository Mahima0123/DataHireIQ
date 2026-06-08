from utils.db import get_connection


def load_job(job):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO jobs (
                external_job_id,
                title,
                company,
                location,
                employment_type,
                source,
                job_url,
                description
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (external_job_id)
            DO NOTHING
            RETURNING job_id;
        """, (
            job["job_url"],
            job["title"],
            job["company"],
            job["location"],
            job["employment_type"],
            job["source"],
            job["job_url"],
            job["description"]
        ))

        result = cur.fetchone()

        if result:
            job_id = result[0]
        else:
            conn.commit()
            cur.close()
            conn.close()
            return

        for skill in job["skills"]:

            cur.execute("""
                INSERT INTO skills(skill_name)
                VALUES(%s)
                ON CONFLICT(skill_name)
                DO NOTHING;
            """, (skill,))

            cur.execute("""
                SELECT skill_id
                FROM skills
                WHERE skill_name=%s
            """, (skill,))

            skill_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO job_skills(job_id, skill_id)
                VALUES(%s,%s)
                ON CONFLICT DO NOTHING;
            """, (job_id, skill_id))

        conn.commit()

    except Exception as e:
        print("Load Error:", e)

    finally:
        cur.close()
        conn.close()