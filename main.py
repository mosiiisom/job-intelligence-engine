from scraper.playwright_scraper import PlaywrightEngine
from scraper.sources.remteok import RemoteOkSource
from config.settings import *


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
        source = RemoteOkSource(engine=engine,base_url=s_data['base_url'],name=s_title)
        fetched_jobs = source.fetch()
        if fetched_jobs:
            jobs.extend(fetched_jobs)


    print(jobs[0])

    engine.stop()

    # save in csv / json
    


if __name__ == '__main__':
    main()
