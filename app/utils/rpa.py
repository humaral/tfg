# Autor: Hugo Martín Alonso
# Fecha: 18-11-2025
# Descripción: Script para ejecutar los trámites en la página web correspondiente

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


def rpa_certificado_empadronamiento(informacion):

    #NOTE mirar de abrir en nueva pestaña
    driver = webdriver.Chrome()

    driver.get("https://www.valladolid.es/es/temas/hacemos/padron-habitantes/solicitud-volante-certificado-empadronamiento-certificado-c")

    driver.find_element(By.ID, "principal.gr_datos.nombre").send_keys(informacion["nombre"])
    driver.find_element(By.ID, "principal.gr_datos.apellidos").send_keys(informacion["apellidos"])
    driver.find_element(By.ID, "principal.gr_datos.dni_nie").send_keys(informacion["dni"])
    driver.find_element(By.ID, "principal.gr_datos.telefono").send_keys(informacion["telefono"])
    driver.find_element(By.ID, "principal.gr_datos.email").send_keys(informacion["email"])
    driver.find_element(By.ID, "principal.gr_datos.motivo").send_keys(informacion["motivo"])

    old_url = driver.current_url

    try:
        WebDriverWait(driver, 60).until(
            expected_conditions.url_changes(old_url)
        )
    except:
        pass
    finally:
        driver.quit()
    return