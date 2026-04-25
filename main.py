from scraper.playwright_scraper import PlaywrightEngine
from scraper.sources.remoteok import RemoteOkSource
from config.settings import *
from storage.csv_handler import save_jobs
from storage.database import init_db
from storage.repositories.job_repo import bulk_upsert_jobs


def main():
    # create engine
    engine = PlaywrightEngine(
        headless=HEADLESS,
        proxies=PROXIES,
        user_agents=USER_AGENTS,
    )

    # start the engine
    engine.start()

    # filter enable sources from config
    enable_sources = [
        (name, data) for name, data in SOURCES.items() if data.get('enabled')
    ]

    jobs = []

    for s_title,s_data in enable_sources:
        fetched_jobs = []
        source = None
        if s_title.lower() == 'remoteok':
            source = RemoteOkSource(engine=engine,base_url=s_data['base_url'],name=s_title)

        if source:
            fetched_jobs = source.fetch()

            if fetched_jobs:
                jobs.extend(fetched_jobs)

    engine.stop()

    ## save in database

    # make sure db file exist
    init_db()

    # upset the jobs
    bulk_upsert_jobs(jobs)



if __name__ == '__main__':
    main()
