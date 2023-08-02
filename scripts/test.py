import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# continuar a desenvolver a def real_path, p/ driver
from selenium.webdriver.chrome.service import Service

SERVICE = Service()
# SERVICE = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(
#     service=SERVICE)
# driver.get("https://wwww.google.com.br")

print(sys.argv, len(sys.argv))
