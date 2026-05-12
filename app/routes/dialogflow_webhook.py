# Autor: Hugo Martín Alonso
# Fecha: 12-12-2025
# Descripción: Controlador de la ruta del webhook de Dialogflow.

from flask import Blueprint, request, jsonify
from app.utils import crear_peticion
import random, os, pandas as pd
from datetime import datetime


dialogflow_webhook_bp = Blueprint('dialogflow_webhook', __name__)


INTENTS = ["Bienvenida", "cambiar_campo", "cita_AEAT_Modalidad", "cita_AEAT_Presencial", "confirmar_si", "tramite_certificado_empadronamiento", "tramite_cita_AEAT", "tramite_tarjeta_SACYL"]


@dialogflow_webhook_bp.route('/webhook', methods=['POST'])
def webhook(): #Procesa la información recibida desde Dialogflow

    req = request.get_json()

    contexts = req["queryResult"].get("outputContexts", [])
    allParams = req["queryResult"].get("allRequiredParamsPresent", False)
    action = req["queryResult"].get("action", "")

    res={}
    
    if action == "tramite_certificado_empadronamiento.crear_peticion" and allParams: #Certificado de empadronamiento
        tel=random.randint(600000000, 999999999) #Genero un número telefónico aleatorio ya que al simularlo con discord no se obtiene este dato. Al subirlo a producción habría que sustituirlo por el número recuperado de la integración telefónica.
       
        params = recuperar_parametros(contexts, "certificado_empadronamiento")

        informacion = {
            "nombre" : params.get("nombre",""),
            "apellidos" : params.get("apellidos",""),
            "dni" : params.get("dni_pasaporte",""),
            "telefono" : params.get("telefono",""),
            "motivo" : params.get("motivo","")
        }
        crear_peticion(telefono=tel, idTramite=1, informacion=informacion)

    elif action == "tramite_cita_AEAT.crear_peticion" and allParams:
        tel=random.randint(600000000, 999999999)

        params = recuperar_parametros(contexts, "cita_aeat")
        
        informacion = {
            "dni" : params.get("dni",""),
            "nombre" : params.get("nombre",{}).get("name",""),
            "servicio" : params.get("servicio",""),
            "modalidad" : params.get("tipo",""),
            "oficina" : params.get("oficina",""),
            "dia" : datetime.fromisoformat(params.get("dia","")).strftime("%Y-%m-%d") if params.get("dia","") else "",
            "hora": formato_hora(params.get("hora","")),
            "email" : params.get("email","")
        }
        crear_peticion(telefono=tel, idTramite=2, informacion=informacion)

    elif action == "tramite_tarjeta_SACYL.crear_peticion" and allParams:
        tel=random.randint(600000000, 999999999)

        params = recuperar_parametros(contexts, "tarjeta_sacyl")

        informacion = {
            "nombre" : params.get("nombre",""),
            "apellido1" : params.get("primer_apellido",""),
            "nacimiento" : params.get("nacimiento",""),
            "motivo" : params.get("motivo",""),
            "centro_salud" : params.get("contro_salud",""),
            "localidad" : params.get("localidad",""),
            "calle" : params.get("calle",""),
            "numero" : params.get("numero",""),
            "piso" : params.get("piso",""),
            "puerta" : params.get("puerta","")
        }
        crear_peticion(telefono=tel, idTramite=3, informacion=informacion)

    elif action == "tramite_cita_AEAT.comprobar_servicio" and allParams:

        params = recuperar_parametros(contexts, "cita_aeat")

        df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/tramite2.csv"), sep=";")
        llamada = df.loc[df["servicio"] == params.get("servicio", ""), "llamada"].iloc[0]
        
        if llamada:
            res = {
                "outputContexts": [
                    {
                        "name": f"{req["session"]}/contexts/tramite_cita_aeat-modalidad",
                        "lifespanCount":5,
                        "parameters": params
                    }
                ],
                "followupEventInput": {
                    "name": "cita_aeat_modalidad",
                    "languageCode": "es-ES",
                    "parameters": params
                }
            }
        else:
            res = {
                "outputContexts": [
                    {
                        "name": f"{req["session"]}/contexts/tramite_cita_aeat-presencial",
                        "lifespanCount":5,
                        "parameters": params
                    }
                ],
                "followupEventInput": {
                    "name": "cita_aeat_presencial",
                    "languageCode": "es-ES",
                    "parameters": params
                }
            }

    elif action == "tramite_cita_AEAT.comprobar_modalidad" and allParams:

        params = recuperar_parametros(contexts, "cita_aeat")
        cita = params.get("tipo","")

        if cita == "presencial":
            res = {
                "outputContexts": [
                    {
                        "name": f"{req["session"]}/contexts/tramite_cita_aeat-presencial",
                        "lifespanCount":5,
                        "parameters": params
                    }
                ],
                "followupEventInput": {
                    "name": "cita_aeat_presencial",
                    "languageCode": "es-ES",
                    "parameters": params
                }
            }
        elif cita == "telefonica":
            res = {
                "fulfillmentMessages":[
                    {
                        "text": {
                            "text": [
                                f"""<speak>Por favor, confírmeme los datos. <break time="450ms"/> 
                                Nombre: {params.get("nombre","").get("name", "")}. <break time="250ms"/>
                                Número de identificación: {params.get("dni","")}. <break time="300ms"/>
                                Vas a realizar el servicio de {params.get("servicio", "")} de forma telefónica. <break time="200ms"/>
                                <emphasis level="moderate">¿Son correctos?</emphasis></speak>"""
                            ]
                        }
                    }
                ],
                "outputContexts": [
                    {
                        "name": f"{req["session"]}/contexts/tramite_cita_aeat-confirmar",
                        "lifespanCount":5,
                        "parameters": params
                    }
                ]
            }
        else:
            res = {
                "fulfillmentMessages":[
                    {
                        "text": {
                            "text": [
                                f"""<speak>Lo siento, no he podido identificar la modalidad de la cita. Por favor, indíqueme si desea una cita presencial o telefónica.</speak>"""
                            ]
                        }
                    }
                ]
            }

    return jsonify(res)


#Al solicitar la confirmación de los datos, la request con la que se creará la petición no incluirá los parámetros directamente, sino que habrá que recuperarlos de los contextos. 
def recuperar_parametros(contextos, contexto_objetivo):

    for c in contextos:
        if c.get("name","").endswith(contexto_objetivo):
            params = c.get("parameters", {})
    return params


#Dado que la AEAT solo permite agendar citas entre las 9:00 y las 14:00, se ajustan las horas recibidas por Dialogflow para que se correspondan con este rango, evitando tener que indicar AM o PM.
def formato_hora(hora):
    if not hora:
        return ""
    
    dt = datetime.fromisoformat(hora)
    h = dt.hour
    m = dt.minute

    if h>14:
        h = h-12
    elif h<9:
        h = h+12
    return f"{h:02d}:{m:02d}"