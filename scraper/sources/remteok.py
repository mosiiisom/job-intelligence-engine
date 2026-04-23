from datetime import datetime
from typing import List
from models.job import Job
from scraper.playwright_scraper import PlaywrightEngine
from scraper.sources.base import BaseJobSource

class RemoteOkSource(BaseJobSource):
    def __init__(self,engine: PlaywrightEngine = None):
        self.engine = engine if engine else PlaywrightEngine()
        self.url = "https://remoteok.com"
        self.name = "RemoteOk"

    def fetch(self) -> List[Job]:
        page = self.engine.get_page(self.url)

        jobs_element = page.query_selector_all("tr.job")

        jobs = []

        for job_el in jobs_element:
            try:
                job = self._parse_job(job_el)
                if job is not None:
                    jobs.append(job)
            except Exception as e:
                print(f"parse error (e)")


        return jobs

    def _parse_job(self, job_el):
        title_el = job_el.query_selector("h2")
        company_el = job_el.query_selector("h3")
        location_el = job_el.query_selector(".location")
        link_el = job_el.query_selector("a.preventLink")
        time_el = job_el.query_selector("time")
        employment_els = job_el.query_selector_all(".location")
        tags_els = job_el.query_selector_all(".tags")

        if not title_el or not company_el:
            return None

        title = title_el.inner_text().strip()
        company = company_el.inner_text().strip()
        location = location_el.inner_text().strip() if location_el else "Remote"
        posted_date = time_el.get_attribute("datetime").strip()

        relative_link = link_el.get_attribute("href") if link_el else None
        url = f"https://remoteok.com{relative_link}" if relative_link else None

        part_time = False
        for employment_el in employment_els:
            part_time = "part time" in employment_el.inner_text().lower().strip()
            if part_time:
                break

        tags = []
        for tag_el in tags_els:
            tags.append(tag_el.query_selector("h3").inner_text().strip())

        return Job(
            title=title,
            company=company,
            location=location,
            url=url,
            source=self.name,
            posted_date=posted_date,
            work_type="remote",
            employment_type="part-time" if part_time else "full-time",
            tags=tags
        )




