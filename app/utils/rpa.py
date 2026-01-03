# Autor: Hugo Martín Alonso
# Fecha: 18-11-2025
# Descripción: Script para ejecutar los trámites en la página web correspondiente

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import pandas as pd
import os, re
from datetime import datetime

OFICINAS_AEAT = {"Administración de Medina del Campo":"Medina del Campo", "Delegación Especial de Castilla y León":"Valladolid"}

def rpa_certificado_empadronamiento(informacion):

    driver = webdriver.Chrome()
    try:
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
            print("Certifcado de empadronamiento solicitado correctamente.")
            driver.quit()
        return True
    
    except:
        driver.quit()
        return False

def rpa_cita_aeat(informacion):

    driver = webdriver.Chrome()
    try:
        driver.get("https://www2.agenciatributaria.gob.es/wlpl/TOCP-MUTE/ServiciosAsocCat")

        df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/tramite2.csv"), sep=";")
        tipo = df.loc[df["servicio"] == informacion.get("servicio",""), "tipo"].iloc[0]
        
        driver.find_element(By.XPATH, "//*[@id='acc-main']/nav/button[2]").click()

        driver.find_element(By.XPATH, f"//li[text()='{tipo}']").click()

        servicio = driver.find_element(By.NAME, informacion.get('servicio',''))
        boton_servicio = servicio.find_element(By.XPATH, ".//button")
        driver.execute_script("arguments[0].click();", boton_servicio)

        driver.find_element(By.ID, "fnif").send_keys(informacion.get("dni",""))
        driver.find_element(By.ID, "fnombre").send_keys(informacion.get("nombre",""))

        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        localidad = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, "fpropos"))
        ).find_element(By.ID, "opt-fpropos-VALLADOLID")
        driver.execute_script("arguments[0].click();", localidad)

        boton_localidad =driver.find_element(By.XPATH, "//button[text()='Aceptar']")
        driver.execute_script("arguments[0].click();", boton_localidad)

        driver.find_element(By.XPATH, "//*[@id='btnMenu']").click()

        if informacion.get("modalidad","") != "telefonica":
            input_dia = driver.find_element(By.ID, "input-date")
            driver.execute_script("arguments[0].value = arguments[1];", input_dia, informacion.get("dia",""))
            input_hora = driver.find_element(By.ID, "input-time")
            driver.execute_script("arguments[0].value = arguments[1];", input_hora, informacion.get("hora",""))
            boton_fecha = driver.find_element(By.ID, "linkAplicar")
            driver.execute_script("arguments[0].click();", boton_fecha)
        
        

        citas = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, "span.nobr"))
        )
        #FIX
        # for cita in citas:
        #     texto = cita.get_attribute("aria-selected")
        #     print("CITA DISPONIBLE:", texto)
        #     if informacion.get("modalidad","") == "telefonica":
        #         if("Te llamamos" in texto.get(["direccion"],"") ):
        #             print("VIURTUALss")
        #             print("Cita telefónica en la AEAT Asignada Correctamente.")
        #             driver.quit()
        #             return True
        #     else:
        #         direccion = OFICINAS_AEAT.get(informacion.get("oficina",""), "") in texto.get(["direccion"],"")
        #         print("DIRECCION:", direccion)
        #         fecha = re.search(r"\d{2}-\d{2}-\d{4}", texto.get(["dia"],""))
        #         print("FECHA:", fecha)
        #         if fecha:
        #             fecha = fecha.group()
        #             fecha = datetime.strptime(fecha, "%d-%m-%Y").strftime("%Y-%m-%d")
        #         hora = re.search(r"\d{2}:\d{2}", texto.get(["hora"],""))
        #         if hora:
        #             hora = hora.group()
    
        #         if direccion and fecha == informacion.get("dia","") and hora == informacion.get("hora",""):
        #             print("Cita presencial en la AEAT Asignada Correctamente.")
        #             driver.quit()
        #             return True
        
        # print("Error al asignar la cita de la AEAT")
        # driver.quit()
        # return False
    except:
        driver.quit()
        return False