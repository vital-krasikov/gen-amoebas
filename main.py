from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from random import randint
import os
import glob

EXPONENTS = ((1,0),(2,0),(2,1),(3,1),(0,2),(3,2),(0,3),(1,3),(1,4),(2,4))
PATH = "C:\\Users\\Win11\\PycharmProjects\\loadAmoebas\\downloads"


def random_coefs(num):
# генерирует набор случайных коэффициентов для многочлена
    return [randint(-1000000, 1000000) / 1000. for _ in range(num)]


def get_poly(coefs, exponents):
# собирает многочлен двух переменных из коэффициентов и списка мультистепеней мономов
# возвращает: строку, содержащую запись многочлена
    result = ""
    first = True
    for i in range(len(coefs)):
        result += ("+" if coefs[i] >= 0 and not first else "") + str(coefs[i])+"*x^"+str(exponents[i][0])+"*y^"+str(exponents[i][1])
        if first: first = False
    return result


def timestamp():
    return time.strftime("%d%m%y%H%M", time.gmtime())


if not os.path.exists(PATH + "\\recent"):
    os.mkdir(PATH + "\\recent")


url = "http://amoebas.ru/amoeba_interactive.html"

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {"download.default_directory": PATH + "\\recent"})

service = Service(executable_path="C:\\Users\\Win11\\PycharmProjects\\loadAmoebas\\chromedriver\\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)


try:
    driver.get(url=url)
    coefs_list = ""

    poly_input = driver.find_element(By.ID, 'fn')

    dirname = str(EXPONENTS)[1:-1].replace(" ", "")
    if not os.path.exists(PATH + "\\" + dirname):
        os.mkdir(PATH + "\\" + dirname)

    for tries in range(2602):

        coefs = random_coefs(len(EXPONENTS))
        coefs_list += str(coefs) + "\n"

        poly_input.clear()
        poly_input.send_keys(get_poly(coefs, EXPONENTS))
        poly_input.send_keys(Keys.ENTER)

        wait = WebDriverWait(driver, 1000)
        wait.until(EC.text_to_be_present_in_element((By.ID, "status"), "Идет построение"))
        wait.until(EC.text_to_be_present_in_element((By.ID, "status"), "Построение завершено"))

        save_img = driver.find_element(By.ID, "save_plt")
        save_img.click()
        time.sleep(3)

except Exception as ex:
    print(ex)
finally:
    fname = PATH + "\\" + timestamp()

    f = open(fname, "w")
    f.write(coefs_list)
    f.close()

    list_of_files = glob.glob(PATH+"\\recent\\*.png")
    list_of_files = sorted(list_of_files, key=os.path.getctime)

    f = open(fname)
    for file in list_of_files:
        line = f.readline()
        if not line:
            break
        os.rename(file, PATH + "\\" + dirname + "\\" + line[1:-2].replace(" ", "") + ".png")
    f.close()

    driver.close()
    driver.quit()