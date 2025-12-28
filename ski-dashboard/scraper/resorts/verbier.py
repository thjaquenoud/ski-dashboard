# scraper/resorts/verbier.py
import logging
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from scraper.base.scraper_base import BaseScraper
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from scraper.resorts.models import Installation, Slope

logger = logging.getLogger(__name__)

STATUS_MAP = {
    "ouvert": "OPEN",
    "en préparation": "PREPARING",
    "fermé": "CLOSED",
    "opened": "OPEN",
    "in-preparation": "PREPARING",
    "closed": "CLOSED"
}

class VerbierScraper(BaseScraper):
    RESORT_NAME = "Verbier"
    BASE_URL = "https://verbier4vallees.ch/fr/informations-utiles/horaires-ouvertures-live"
    DOMAIN = "Verbier"
    
    # Helper function to extract item details with similar patterns (installations/slopes)
    def _extract_item(self, item, category: str):
        """Helper to extract common fields from an item element."""
        # Name
        try:
            name_elem = item.find_element(By.CSS_SELECTOR, "h3.facility-item__title")
            name = name_elem.text.strip()
        except:
            name = ""

        # Lift type / difficulty
        try:
            type_elem = item.find_elements(By.CSS_SELECTOR, "div.facility-item__subtitle")
            lift_type = type_elem[0].text.strip() if type_elem else ""
        except:
            lift_type = ""

        # Status
        try:
            status_elem = item.find_elements(By.CSS_SELECTOR, "span.facility-item__status-text")
            status_text = status_elem[0].text.strip().lower() if status_elem else None
            status = STATUS_MAP.get(status_text, status_text)
        except:
            status = None

        # Build the right Pydantic object
        if category == "installations":
            from scraper.resorts.models import Installation
            return Installation(domain=self.DOMAIN, name=name, lift_type=lift_type, status=status)
        elif category == "slopes":
            from scraper.resorts.models import Slope
            return Slope(domain=self.DOMAIN, name=name, difficulty=lift_type, status=status)
        else:
            return None

    

    def scrape(self):
        logger.info(f"Scraping {self.RESORT_NAME}...")

        # Step 1: Close cookie banner if it exists and scroll to bottom
        try:
            accept_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.coi-banner__accept"))
            )
            accept_btn.click()
            logger.info("Cookie banner closed")

            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            logger.info("Scrolled to bottom to render all elements")
            time.sleep(1)
        except TimeoutException:
            logger.info("No cookie banner found")

        installations: list[Installation] = []
        slopes: list[Slope] = []

        # --- Scrape Installations ---
        try:
            section_xpath = f"//section[.//h2[contains(text(), 'Installations {self.DOMAIN}')]]"
            section_elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, section_xpath))
            )
            container = section_elem.find_element(By.CSS_SELECTOR, "div.facility-item__collapse-wrapper")
            items = container.find_elements(By.CSS_SELECTOR, "section.facility-item")

            installations = [self._extract_item(item, "installations") for item in items]

        except TimeoutException:
            logger.warning(f"Installations section {self.DOMAIN} not found")

        # --- Scrape Slopes ---
        try:
            section_xpath = (
                f"//section[contains(@class,'gy-gutter__item')]"
                f"[.//button[contains(normalize-space(.), 'Pistes') and contains(normalize-space(.), '{self.DOMAIN}')]]"
            )
            section_elem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, section_xpath))
            )
            container = section_elem.find_element(By.CSS_SELECTOR, "div.facility-item__collapse-wrapper")
            items = container.find_elements(By.CSS_SELECTOR, "section.facility-item")

            slopes = [self._extract_item(item, "slopes") for item in items]

        except TimeoutException:
            logger.warning(f"Slopes section {self.DOMAIN} not found")


        logger.info(f"Scraping finished, found {len(installations)} installations and {len(slopes)} slopes")
        return {
            "installations": installations,
            "slopes": slopes
        }
