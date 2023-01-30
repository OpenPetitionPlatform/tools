from selenium import webdriver
from selenium.webdriver.common.by import By
import json

BASE_URL = 'https://sev.gov.ru/feedback/new/'

XPATH_ADD_BUTTON = "//button[@class='new-feedback__btn']"
XPATH_LAST_FIELDSET = "//fieldset[@class='new-feedback__fieldset new-feedback__fieldset--coauthor'][last()]"
XPATH_SURNAME_INPUT = XPATH_LAST_FIELDSET + '//label[contains(text(), "Фамилия")]/input'
XPATH_NAME_INPUT = XPATH_LAST_FIELDSET + '//label[contains(text(), "Имя")]/input'
XPATH_PATRONYMIC_INPUT = XPATH_LAST_FIELDSET + '//label[contains(text(), "Отчество")]/input'
XPATH_EMAIL_INPUT = XPATH_LAST_FIELDSET + '//label[contains(text(), "Адрес электронной почты")]/input'

def add_author(driver, author, first):
    if not first:
        driver.find_element(By.XPATH, XPATH_ADD_BUTTON).click()

    driver.find_element(By.XPATH, XPATH_SURNAME_INPUT).send_keys(author['name'])  # workaround for name and surname are reversed
    driver.find_element(By.XPATH, XPATH_NAME_INPUT).send_keys(author['surname'])  # workaround for name and surname are reversed
    if author['patronymic'] is not None:
        driver.find_element(By.XPATH, XPATH_PATRONYMIC_INPUT).send_keys(author['patronymic'])
    driver.find_element(By.XPATH, XPATH_EMAIL_INPUT).send_keys(author['email'])

driver = webdriver.Chrome()

driver.get(BASE_URL)

input('Wait until any key pressed to import data from json file ...')

with open("data.json") as data_file:
    data = json.load(data_file)

first = True
for author in data:
    add_author(driver, author, first)
    first = False

input('Wait until any key pressed to quit from Chrome ...')
input('Are you sure? All entered data will be lost!')

driver.quit()
