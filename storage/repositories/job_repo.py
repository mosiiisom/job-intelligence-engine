from typing import List
from models.job import Job
from storage.database import get_connection


def bulk_upsert_jobs(jobs: List[Job]):
    conn = get_connection()
    curr = conn.cursor()

    data = [
        (
            job.title,
            job.company,
            job.location,
            job.url,
            job.source,
            job.posted_at,
            job.work_type,
            job.employment_type,
            ",".join(job.tags),
        )
        for job in jobs
    ]

    curr.executemany("""
            INSERT INTO jobs (
                title,company,location,url,source,posted_at,work_type,employment_type,tags
                )
                VALUES (?,?,?,?,?,?,?,?,?)
                ON CONFLICT (url) DO UPDATE SET
                    title=excluded.title,
                    company=excluded.company,
                    location=excluded.location,
                    posted_at=excluded.posted_at,
                    work_type=excluded.work_type,
                    employment_type=excluded.employment_type,
                    tags=excluded.tags
            """, data)

    conn.commit()
    conn.close()
