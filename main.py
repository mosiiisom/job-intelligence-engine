
from scraper.sources.remteok import RemoteOkSource

def main():
    source = RemoteOkSource()
    jobs = source.fetch()

    print(jobs)


if __name__ == '__main__':
    main()