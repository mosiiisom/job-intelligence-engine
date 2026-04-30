import pytest

from storage.repositories.job_queries import get_all_jobs, filter_jobs, search_jobs
from tests.test_storage.test_repositories.helpers import create_test_jobs, seed_jobs, create_test_job


# ==================== Core Behavior Tests ====================

def test_get_all_jobs_returns_limited_results(db_connection):
    jobs = create_test_jobs(20)
    seed_jobs(db_connection, jobs)

    result = get_all_jobs(limit=5)

    assert len(result) == 5


def test_filter_jobs_by_company(db_connection):
    jobs = [
        create_test_job(company="Amazon"),
        create_test_job(company="Apple"),
        create_test_job(company="NVIDIA"),
        create_test_job(company="Microsoft"),
        create_test_job(company="Meta"),
    ]

    seed_jobs(db_connection, jobs)

    result = filter_jobs(companies=["Amazon"])

    assert all(job["company"] == "Amazon" for job in result)
    assert len(result) == 1


def test_filter_jobs_by_tags(db_connection):
    jobs = [
        create_test_job(tags=["python", "fastapi"]),
        create_test_job(tags=["javascript", "react", "nextjs"]),
        create_test_job(tags=["swift", "ios"]),
    ]

    seed_jobs(db_connection, jobs)

    result = filter_jobs(tags=["python"])

    assert len(result) == 1
    assert all(job["tags"] and "python" in job["tags"] for job in result)


@pytest.mark.parametrize(
    "jobs,search_key,expected_len", [
        (
                [
                    create_test_job(title="Python Backend Developer", company="Google"),
                    create_test_job(title="PHP Backend Developer", tags=["php", "laravel"]),
                    create_test_job(title="QA Engineer", tags=["python"], company="Stripe"),
                    create_test_job(title="Web Developer", tags=["python", "django"]),
                ],
                "python",
                3
        ),
        (
                [
                    create_test_job(title="Legal Data Analyst Junior Vaga Afirmativa para PCD", company="FSE"),
                    create_test_job(title="Manager client Support", tags=["manager", "training"]),
                    create_test_job(title="Senior Data Analyst", tags=["data", "test"], company="Stripe"),
                    create_test_job(title="Backend Engineer", tags=["python", "django", "backend"]),
                    create_test_job(title="Senior Software Engineer", tags=["nodejs", "sql", "backend"]),
                ],
                "backend",
                2
        ),
        (
                [
                    create_test_job(title="Python Developer"),
                    create_test_job(title="python engineer"),
                    create_test_job(title="Java Developer"),
                ],
                "PYTHON",
                2
        ),
        (
                [
                    create_test_job(title="Engineer", company="Amazon"),
                    create_test_job(title="Developer", company="Google"),
                    create_test_job(title="Manager", company="Amazon"),
                ],
                "Amazon",
                2
        ),
        (
                [
                    create_test_job(title="Dev", location="Berlin"),
                    create_test_job(title="QA", location="Remote"),
                    create_test_job(title="Backend", location="Berlin"),
                ],
                "Berlin",
                2
        ),
        (
                [
                    create_test_job(title="Senior Backend Engineer"),
                    create_test_job(title="Backend Developer"),
                    create_test_job(title="Frontend Engineer"),
                ],
                "Back",
                2
        ),
        (
                [
                    create_test_job(title="iOS Developer"),
                    create_test_job(title="Android Developer"),
                ],
                "python",
                0
        ),
    ]
)
def test_search_jobs(db_connection, jobs, search_key, expected_len):
    seed_jobs(db_connection, jobs)

    results = search_jobs(search_key)

    assert len(results) == expected_len


def test_search_with_no_results(db_connection):
    jobs = [
        create_test_job(title="Legal Data Analyst Junior Vaga Afirmativa para PCD", company="FSE"),
        create_test_job(title="Manager client Support", tags=["manager", "training"]),
        create_test_job(title="Senior Data Analyst", tags=["data", "test"], company="Stripe"),
        create_test_job(title="Backend Engineer", tags=["python", "django", "backend"]),
        create_test_job(title="Senior Software Engineer", tags=["nodejs", "sql", "backend"]),
    ]

    seed_jobs(db_connection, jobs)

    result = search_jobs("meta")

    assert len(result) == 0


def test_get_all_jobs_orders_by_posted_at_desc(db_connection):
    jobs = [
        create_test_job(title="Old", posted_at="2024-01-01T00:00:00Z"),
        create_test_job(title="New", posted_at="2026-01-01T00:00:00Z"),
    ]

    seed_jobs(db_connection, jobs)

    result = get_all_jobs(limit=2)

    assert result[0]["title"] == "New"
    assert result[1]["title"] == "Old"


def test_filter_jobs_multiple_conditions(db_connection):
    jobs = [
        create_test_job(company="Amazon", location="Berlin", tags=["python"]),
        create_test_job(company="Amazon", location="Remote", tags=["java"]),
        create_test_job(company="Google", location="Berlin", tags=["python"]),
    ]

    seed_jobs(db_connection, jobs)

    result = filter_jobs(
        companies=["Amazon"],
        locations=["Berlin"],
        tags=["python"]
    )

    assert len(result) == 1
    assert result[0]["company"] == "Amazon"
    assert result[0]["location"] == "Berlin"


def test_search_jobs_respects_limit(db_connection):
    jobs = create_test_jobs(10)
    seed_jobs(db_connection, jobs)

    result = search_jobs("Engineer", limit=3)

    assert len(result) == 3


def test_filter_jobs_multiple_tags_or_logic(db_connection):
    jobs = [
        create_test_job(tags=["python"]),
        create_test_job(tags=["django"]),
        create_test_job(tags=["java"]),
    ]

    seed_jobs(db_connection, jobs)

    result = filter_jobs(tags=["python", "django"])

    assert len(result) == 2

def test_filter_jobs_no_filters_returns_all(db_connection):
    jobs = create_test_jobs(5)
    seed_jobs(db_connection, jobs)

    result = filter_jobs()

    assert len(result) == 5


# ==================== Edge Case Tests ====================


def test_filter_jobs_ignores_null_tags(db_connection):
    jobs = [
        create_test_job(tags=None),
        create_test_job(tags=["python"]),
    ]
    seed_jobs(db_connection, jobs)

    result = filter_jobs(tags=["python"])

    assert len(result) == 1

def test_filter_jobs_tag_partial_match(db_connection):
    jobs = [
        create_test_job(tags=["python"]),
        create_test_job(tags=["cpython"]),
    ]
    seed_jobs(db_connection, jobs)

    result = filter_jobs(tags=["python"])

    assert len(result) == 2


def test_search_jobs_with_special_characters(db_connection):
    jobs = [
        create_test_job(title="100% Remote Engineer"),
        create_test_job(title="Backend_Engineer"),
    ]
    seed_jobs(db_connection, jobs)

    result = search_jobs("%")

    assert len(result) >= 1

def test_get_all_jobs_limit_zero(db_connection):
    jobs = create_test_jobs(5)
    seed_jobs(db_connection, jobs)

    result = get_all_jobs(limit=0)

    assert result == []

def test_get_all_jobs_limit_exceeds_data(db_connection):
    jobs = create_test_jobs(3)
    seed_jobs(db_connection, jobs)

    result = get_all_jobs(limit=10)

    assert len(result) == 3

def test_search_jobs_sql_injection_attempt(db_connection):
    jobs = create_test_jobs(3)
    seed_jobs(db_connection, jobs)

    result = search_jobs("' OR 1=1 --")

    assert isinstance(result, list)