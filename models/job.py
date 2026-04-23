from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Job:
    title: str
    company: str
    location: str
    url: str
    source: str
    posted_date: Optional[str] = None
    work_type: str = "remote"
    employment_type: str = "full-time"
    tags: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "url": self.url,
            "source": self.source,
            "posted_date": self.posted_date,
            "work_type": self.work_type,
            "employment_type": self.employment_type,
            "tags": ",".join(self.tags)
        }
