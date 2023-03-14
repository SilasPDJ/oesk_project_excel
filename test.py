from time import sleep
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver


def create_tor_driver():
    tor_browser_path = r"A:\TOR\Browser\firefox.exe"
    try:
        service = Service(tor_browser_path)
        driver = webdriver.Firefox(service=service)
        return driver
    except Exception as e:
        print(f"Error creating Tor driver: {e}")
        return None


print("Before create_tor_driver() call")
driver = create_tor_driver()
if driver is None:
    print("Error creating Tor driver, exiting...")
else:
    print("sleep 10")
    sleep(10)
    driver.get("https://cav.receita.fazenda.gov.br/autenticacao/Login")
    print(driver.current_url)
    input("hi")
