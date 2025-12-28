# scraper/resorts/verbier.py
import logging
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from scraper.base.scraper_base import BaseScraper
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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

    DOMAIN = "Verbier"  # start with just Verbier

    def scrape(self):
        logger.info(f"Scraping {self.RESORT_NAME}...")

        # Step 1: Close cookie banner if it exists
        try:
            accept_btn = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.coi-banner__accept"))
            )
            accept_btn.click()
            logger.info("Cookie banner closed")

            # Step 2: Scroll to the bottom after a short delay to trigger lazy loading
            self.driver.implicitly_wait(1)  # 1-second pause
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            logger.info("Scrolled to bottom to render all elements")
            time.sleep(1)  # optional extra pause to let animations/rendering finish
        except TimeoutException:
            logger.info("No cookie banner found")

        results = []

        # Inside the loop for section_type in ["Installations", "Pistes"]:
        for section_type in ["Installations", "Pistes"]:
            try:
                # Step 2: Locate the section wrapper containing the button with the correct title
                section_xpath = (
                    f"//section[.//h2[contains(text(), '{section_type} {self.DOMAIN}')]]"
                )
                
                section_xpath = (
                    f"//section[contains(@class,'gy-gutter__item')]"
                    f"[.//button[contains(normalize-space(.), 'Pistes') and contains(normalize-space(.), '{self.DOMAIN}')]]"
                )

                
                section_elem = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, section_xpath))
                )

                # Step 3: Find the container div with all items inside this section
                container = section_elem.find_element(
                    By.CSS_SELECTOR, "div.facility-item__collapse-wrapper"
                )

                # Step 4: Loop over each lift/piste
                items = container.find_elements(By.CSS_SELECTOR, "section.facility-item")

                for item in items:
                    # Name
                    name_elem = item.find_element(By.CSS_SELECTOR, "h3.facility-item__title")
                    name = name_elem.text.strip() if name_elem else None

                    # Difficulty / slope type
                    diff_elem = item.find_elements(By.CSS_SELECTOR, "div.facility-item__subtitle")
                    difficulty = diff_elem[0].text.strip() if diff_elem else None

                    # Status
                    status_elem = item.find_elements(By.CSS_SELECTOR, "span.facility-item__status-text")
                    status_text = status_elem[0].text.strip().lower() if status_elem else None
                    status = STATUS_MAP.get(status_text, status_text)

                    results.append({
                        "domain": self.DOMAIN,
                        "category": "slopes" if section_type.lower() == "pistes" else "installations",
                        "name": name,
                        "lift_type": difficulty,
                        "status": status
                    })

            except TimeoutException:
                logger.warning(f"Section {section_type} {self.DOMAIN} not found")




        logger.info(f"Scraping finished, found {len(results)} items")
        return results
