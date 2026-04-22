
from typing import List
from models.job import Job
from scraper.sources.base import BaseJobSource

class RemoteOkSource(BaseJobSource):

    def fetch(self) -> List[Job]:

        jobs = []



