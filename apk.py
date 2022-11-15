from tkinter import W
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def hacer_click(driver, localizador: tuple, tiempo_espera: int = 10) -> None:
    elemento = WebDriverWait(driver,tiempo_espera).until(
        EC.element_to_be_clickable(localizador))
    elemento.click()

def enviar_texto(driver, localizador:tuple, texto:str, tiempo_espera: int = 10) -> None:
    elemento = WebDriverWait(driver, tiempo_espera).until(
        EC.visibility_of_element_located(localizador))
    elemento.send_keys(texto)

def obtener_elementos(driver, localizador:tuple, tiempo_espera: int = 10) -> list:
    return WebDriverWait(driver, tiempo_espera).until(
        EC.visibility_of_all_elements_located(localizador))

