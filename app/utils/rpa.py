# Autor: Hugo Martín Alonso
# Fecha: 18-11-2025
# Descripción: Script para ejecutar los trámites en la página web correspondiente

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


def rpa_certificado_empadronamiento(informacion):

    driver = webdriver.Chrome()

    driver.get("https://www.valladolid.es/es/temas/hacemos/padron-habitantes/solicitud-volante-certificado-empadronamiento-certificado-c")

    driver.find_element(By.ID, "principal.gr_datos.nombre").send_keys(informacion.get("nombre",""))
    driver.find_element(By.ID, "principal.gr_datos.apellidos").send_keys(informacion.get("apellidos",""))
    driver.find_element(By.ID, "principal.gr_datos.dni_nie").send_keys(informacion.get("dni",""))
    driver.find_element(By.ID, "principal.gr_datos.telefono").send_keys(informacion.get("telefono",""))
    driver.find_element(By.ID, "principal.gr_datos.email").send_keys(informacion.get("email",""))
    driver.find_element(By.ID, "principal.gr_datos.motivo").send_keys(informacion.get("motivo",""))

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

def rpa_cita_aeat(informacion):

    driver = webdriver.Chrome()

    driver.get("https://www2.agenciatributaria.gob.es/wlpl/TOCP-MUTE/internet/identificacion")

    driver.find_element(By.ID, "fnif").send_keys(informacion.get("dni",""))
    driver.find_element(By.ID, "fnombre").send_keys(informacion.get("nombre",""))

    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # driver.find_element(By.ID, "principal.gr_datos.dni_nie").send_keys(informacion.get("dni",""))
    # driver.find_element(By.ID, "principal.gr_datos.telefono").send_keys(informacion.get("telefono",""))
    # driver.find_element(By.ID, "principal.gr_datos.email").send_keys(informacion.get("email",""))
    # driver.find_element(By.ID, "principal.gr_datos.motivo").send_keys(informacion.get("motivo",""))

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