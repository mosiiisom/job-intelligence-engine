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

    # get enable sources from config
    enable_sources = [{
        source_name: source_data
    } for source_name, source_data in SOURCES.items() if source_data.get('enabled')]

    jobs = []

    for enable_s in enable_sources:
        source = RemoteOkSource(engine=engine,base_url=enable_s['base_url'],name=enable_s['name'])
        fetched_jobs = source.fetch()
        if fetched_jobs:
            jobs.extend(fetched_jobs)


    print(jobs[0])

    engine.stop()


if __name__ == '__main__':
    main()
