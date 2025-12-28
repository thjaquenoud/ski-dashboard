from scraper.resorts.verbier import VerbierScraper

if __name__ == "__main__":
    scraper = VerbierScraper(headless=True)
    data = scraper.run()
    print(data)