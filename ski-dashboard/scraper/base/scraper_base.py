from abc import ABC, abstractmethod
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging

from scraper.base.selenium_driver import create_driver


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """
    Abstract base class for all resort scrapers.
    """

    RESORT_NAME: str = "UNKNOWN"
    BASE_URL: str = ""
    
    def __init__(self, headless: bool = True):
        self.driver: WebDriver = create_driver(headless=False) #create_driver(headless=headless)
        self.wait = WebDriverWait(self.driver, 20)

    def open(self):
        logger.info("Opening %s (%s)", self.RESORT_NAME, self.BASE_URL)
        self.driver.get(self.BASE_URL)

    def close(self):
        logger.info("Closing browser for %s", self.RESORT_NAME)
        self.driver.quit()

    def run(self) -> dict:
        """
        Main execution entrypoint.
        """
        try:
            self.open()
            data = self.scrape()
            return data
        except Exception as e:
            logger.exception("Scraping failed for %s", self.RESORT_NAME)
            raise e
        finally:
            self.close()

    @abstractmethod
    def scrape(self) -> dict:
        """
        Implement resort-specific scraping logic.
        Must return structured data.
        """
        pass

    def wait_for_element(self, by: By, value: str):
        return self.wait.until(EC.presence_of_element_located((by, value)))
