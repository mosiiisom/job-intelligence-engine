from unittest.mock import patch, MagicMock

import pytest

from models.job import Job
from scraper.sources.remoteok import RemoteOkSource


# ==================== Fixtures ====================

@pytest.fixture()
def mock_engine():
    mock_engine = MagicMock()
    mock_engine.get_page.return_value = (MagicMock(), MagicMock())
    return mock_engine


@pytest.fixture()
def source(mock_engine):
    return RemoteOkSource(engine=mock_engine)


@pytest.fixture()
def job_el():
    return MagicMock()


@pytest.fixture
def mocked_job_element(title, company, locations, link, posted_at, tags):
    job_el = MagicMock()

    def mock_query_selector(selector):
        el = MagicMock()
        if selector == "h2":
            el.inner_text.return_value = title
        elif selector == "h3":
            el.inner_text.return_value = company
        elif selector == ".location":
            el.inner_text.return_value = locations[0] if locations else ""
        elif selector == "a.preventLink":
            el.get_attribute.return_value = link
        elif selector == "time":
            el.get_attribute.return_value = posted_at
        else:
            el.inner_text.return_value = ""
            el.get_attribute.return_value = None
        return el

    def mock_query_selector_all(selector):
        if selector == ".location":
            return [MagicMock(inner_text=lambda t=text: t) for text in locations]
        if selector == ".tag":
            return [
                MagicMock(query_selector=lambda _: MagicMock(inner_text=lambda: tag))
                for tag in tags
            ]
        return []

    job_el.query_selector.side_effect = mock_query_selector
    job_el.query_selector_all.side_effect = mock_query_selector_all

    return job_el


# ==================== Fetch ====================

def test_fetch(source, mock_engine):
    mock_job_element = MagicMock()
    mock_page = mock_engine.get_page.return_value[0]
    mock_page.query_selector_all.return_value = [mock_job_element]

    with patch.object(source, '_parse_job', return_value=Job(
            title="Senior Python Developer",
            company="TestCompany",
            location="Remote",
            url="https://remoteok.com/job/123",
            source="RemoteOk"
    )):
        jobs = source.fetch()

    assert isinstance(jobs, list)
    assert len(jobs) == 1
    assert isinstance(jobs[0], Job)
    assert jobs[0].title == "Senior Python Developer"


def test_fetch_returns_empty_list_when_get_page_fails(source, mock_engine):
    mock_engine.get_page.return_value = None

    jobs = source.fetch()

    assert jobs == []

    assert mock_engine.get_page.call_count == 1
    mock_engine.get_page.assert_called_once_with(source.url)


def test_fetch_closes_page_and_context(source, mock_engine):
    mock_page, mock_context = mock_engine.get_page.return_value
    mock_page.query_selector_all.return_value = []

    source.fetch()

    mock_page.close.assert_called_once()
    mock_context.close.assert_called_once()


# ==================== Parse ====================

@pytest.mark.parametrize(
    "title,company,locations,link,posted_at,tags,expected_location,expected_employment",
    [
        ("Senior Python Developer", "Stripe",
         ["🌏 Worldwide", "💰 Upgrade...", "⏰ Part time"],
         "/senior-python-2345", "2026-04-12T14:12:32Z", ["python", "django"],
         "worldwide", "part-time"),

        ("Crypto Trader", "Fox GLobal Assets",
         ["🌏 Worldwide", "⏰ Part time"],
         "/fox-global", "2026-04-21T08:59:17Z", ["trading"],
         "worldwide", "part-time"),
    ]

)
def test_parse_job_success(
        source,
        mocked_job_element,
        title, company, locations, link, posted_at, tags, expected_location, expected_employment
):
    job = source._parse_job(mocked_job_element)

    assert isinstance(job, Job)
    assert job.title == title
    assert job.company == company
    assert job.location == expected_location
    assert job.employment_type == expected_employment
    assert job.url == f"https://remoteok.com{link}"


def test_parse_job_returns_nothing_if_title_not_set(source, job_el):
    job_el.query_selector.return_value = None

    job = source._parse_job(job_el)

    assert job is None
