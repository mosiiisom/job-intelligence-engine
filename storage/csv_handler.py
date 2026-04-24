import csv
from typing import List
from models.job import Job
from pathlib import Path


def save_jobs(
        jobs: List[Job],
        file_path: str = "data/jobs.csv",
        mode: str = "w",
):
    if not jobs:
        print("No jobs to save")
        return

    # make sure the file path exist
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    fieldsName = list(jobs[0].to_dict().keys())

    with open(file_path, mode,newline="",encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldsName)

        # write the headers if it's a new file
        if mode == "w":
            writer.writeheader()

        for job in jobs:
            writer.writerow(job.to_dict())

    print(f"Saved {len(jobs)} jobs to {file_path}")