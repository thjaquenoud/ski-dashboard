from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def create_driver(
    headless: bool = True,
    window_size: str = "1920,1080",
    user_agent: str | None = None,
    page_load_timeout: int = 30,
):
    """
    Create and return a configured Selenium Chrome WebDriver.
    """

    chrome_options = Options()

    if headless:
        chrome_options.add_argument("--headless=new")

    chrome_options.add_argument(f"--window-size={window_size}")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    if user_agent:
        chrome_options.add_argument(f"--user-agent={user_agent}")

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(page_load_timeout)

    return driver
