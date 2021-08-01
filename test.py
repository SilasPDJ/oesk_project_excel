from default.webdriver_utilities.wbs import WDShorcuts as W
from default.webdriver_utilities.pre_drivers import pgdas_driver
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep

driver = pgdas_driver()
weblink = 'https://portal.gissonline.com.br/login/index.html'
with open('pgdas_fiscal_oesk/data_clients_files/giss_passwords.txt') as f:
    __senhas = f.read().split(',')


driver.get(weblink)
cont_senha = 0

_logar = '127571'  # constr
# _logar = '168632'


while True:
    # TxtIdent
    driver.find_element_by_xpath('//input[@name="TxtIdent"]').send_keys(_logar)
    driver.find_element_by_xpath(
        '//input[@name="TxtSenha"]').send_keys(__senhas[cont_senha])
    print(f'Senha: {__senhas[cont_senha]}', end=' ')
    cont_senha += 1
    driver.find_element_by_link_text("Acessar").click()
    try:
        WebDriverWait(driver, 5).until(expected_conditions.alert_is_present(),
                                       'Timed out waiting for PA creation ' +
                                       'confirmation popup to appear.')
        alert = driver.switch_to.alert
        alert.accept()
        print("estou no try")
        driver.execute_script("window.history.go(-1)")
    except TimeoutException:
        print("no alert, sem alerta, exceptado")
        break

    try:
        iframe = driver.find_element_by_xpath(
            "//iframe[@name='header']")
        driver.switch_to.frame(iframe)
    except NoSuchElementException:
        driver.execute_script(
            "window.location.href=('/tomador/tomador.asp');")


try:
    driver.find_element_by_xpath(
        "//img[contains(@src,'images/bt_menu__05_off.jpg')]").click()
except (NoSuchElementException, ElementNotInteractableException) as e:
    print(e)

    def constr_civil():
        print('teste')

    constr_civil()
