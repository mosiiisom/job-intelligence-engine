
from abc import ABC, abstractmethod
from typing import List
from models.job import Job

class BaseJobSource(ABC):
    @abstractmethod
    def fetch(self) -> List[Job]:
        """
        Fetch Jobs from the source and return the Jobs List
        :return:
        """
        pass