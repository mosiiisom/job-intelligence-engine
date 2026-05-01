# ==================== Fixtures ====================
import pytest

from models.job import Job
from storage.repositories.job_repo import bulk_upsert_jobs
from tests.test_storage.test_repositories.helpers import create_test_job, create_test_jobs


# ====================== Test Helpers ======================

def get_job_count(db_connection) -> int:
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM jobs")
    row = cursor.fetchone()
    return row["count"]


def get_all_jobs(db_connection, limit=100) -> list[Job]:
    rows = db_connection.execute('SELECT * FROM jobs ORDER BY posted_at DESC LIMIT ?', (limit,)).fetchall()

    return [dict(row) for row in rows]


def get_job_by_url(db_connection, url: str) -> dict:
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT title, company, source, tags, employment_type FROM jobs WHERE url = ?",
        (url,)
    )
    return cursor.fetchone()


# ==================== Tests ====================

@pytest.mark.parametrize(
    "jobs, expected_count, check_url, expected_title",
    [
        (
                [create_test_job(title="Senior Python Developer", url="https://remoteok.com/job-1")],
                1,
                "https://remoteok.com/job-1",
                "Senior Python Developer"
        ),
        (
                [
                    create_test_job(title="Job A", url="https://example.com/1"),
                    create_test_job(title="Job B", url="https://example.com/2")
                ],
                2,
                "https://example.com/1",
                "Job A"
        )
    ],
    ids=["single_job", "multiple_jobs"]
)
def test_bulk_upsert_inserts_jobs_correctly(db_connection, jobs, expected_count, check_url, expected_title):
    bulk_upsert_jobs(jobs)

    assert get_job_count(db_connection) == expected_count

    saved = get_job_by_url(db_connection, check_url)
    assert saved is not None
    assert saved["title"] == expected_title
    assert saved["source"] == jobs[0].source


def test_bulk_upsert_updates_existing_job_on_conflict(db_connection):
    original = create_test_job(title="Old Title", url="https://remoteok.com/conflict-test")
    updated = create_test_job(
        title="New Updated Title",
        url="https://remoteok.com/conflict-test",
        employment_type="part-time",
        tags=["new", "senior", "updated"]
    )

    bulk_upsert_jobs([original])
    bulk_upsert_jobs([updated])

    saved = get_job_by_url(db_connection, updated.url)

    assert saved["title"] == "New Updated Title"
    assert saved["employment_type"] == "part-time"
    assert "updated" in saved["tags"]


# ==================== Edge Cases ====================

def test_bulk_upsert_with_empty_list_does_nothing(db_connection):
    bulk_upsert_jobs([])
    assert get_job_count(db_connection) == 0


def test_bulk_upsert_handles_empty_and_none_tags(db_connection):
    jobs = [
        create_test_job(title="No Tags 1", tags=[]),
        create_test_job(title="No Tags 2", tags=None),
    ]

    bulk_upsert_jobs(jobs)

    saved = get_all_jobs(db_connection)
    assert len(saved) == 2

    for job in saved:
        assert job.get("tags") in (None, "", "[]")


def test_bulk_upsert_large_batch(db_connection):
    jobs = create_test_jobs(500)

    bulk_upsert_jobs(jobs)

    assert get_job_count(db_connection) == 500
