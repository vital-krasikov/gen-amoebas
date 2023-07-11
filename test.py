# package for drawing the amoeba of a polinomial with given coefficients and monomial exponent vectors
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_poly(coefs, exponents):
    result = ""
    first = True
    for i in range(len(coefs)):
        result += ("+" if coefs[i] >= 0 and not first else "") + str(coefs[i])+"*x^"+str(exponents[i][0])+"*y^"+str(exponents[i][1])
        if first: first = False
    return result


EXPONENTS = ((1,0),(2,0),(2,1),(3,1),(0,2),(3,2),(0,3),(1,3),(1,4),(2,4))
COEFS = [-308.439,32.122,595.13,66.278,-179.985,-377.482,742.215,440.773,900.301,-871.847]

url = "http://amoebas.ru/amoeba_interactive.html"


service = Service(executable_path="C:\\Users\\Win11\\PycharmProjects\\loadAmoebas\\chromedriver\\chromedriver.exe")
driver = webdriver.Chrome(service=service)


try:
    driver.get(url=url)
    poly_input = driver.find_element(By.ID, 'fn')

    poly_input.clear()
    poly_input.send_keys(get_poly(COEFS, EXPONENTS))
    poly_input.send_keys(Keys.ENTER)

    wait = WebDriverWait(driver, 1000)
    wait.until(EC.text_to_be_present_in_element((By.ID, "status"), "Идет построение"))
    wait.until(EC.text_to_be_present_in_element((By.ID, "status"), "Построение завершено"))

    time.sleep(5)

except Exception as ex:
    print(ex)
finally:

    driver.close()
    driver.quit()