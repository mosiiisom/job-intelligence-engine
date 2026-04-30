from models.job import Job


def create_test_job(
        title: str = "Senior Python Developer",
        company: str = "Stripe",
        location: str = "Worldwide",
        url: str = None,
        source: str = "remoteok",
        posted_at: str = "2026-04-28T10:00:00Z",
        work_type: str = "remote",
        employment_type: str = "full-time",
        tags: list = None
) -> Job:
    if url is None:
        import uuid
        url = f"https://remoteok.com/test-{uuid.uuid4().hex[:8]}"

    return Job(
        title=title,
        company=company,
        location=location,
        url=url,
        source=source,
        posted_at=posted_at,
        work_type=work_type,
        employment_type=employment_type,
        tags=tags
    )


def create_test_jobs(count: int = 3) -> list[Job]:
    return [create_test_job(title=f"Engineer {i + 1}",
                            company=f"Company {i % 4 + 1}",
                            url=f"https://remoteok.com/batch-{i}")
            for i in range(count)]


def seed_jobs(conn, jobs: list):
    from storage.repositories.job_repo import bulk_upsert_jobs
    bulk_upsert_jobs(jobs)
