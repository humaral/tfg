from flask import Blueprint, request, jsonify
from app.utils import crear_peticion
import random, os, pandas as pd


dialogflow_webhook_bp = Blueprint('dialogflow_webhook', __name__)


INTENTS = ["Bienvenida", "cambiar_campo", "cita_AEAT_Modalidad", "cita_AEAT_Presencial", "confirmar_si", "tramite_certificado_empadronamiento", "tramite_cita_AEAT", "tramite_tarjeta_SACYL"]


@dialogflow_webhook_bp.route('/webhook', methods=['POST'])
def webhook():

    req = request.get_json()
    
    intent = req["queryResult"]["intent"]["displayName"]
    params_intent = req["queryResult"].get("parameters", {})
    contexts = req["queryResult"].get("outputContexts", {})
    allParams = req["queryResult"].get("allRequiredParamsPresent", False)
    action = req["queryResult"].get("action", "")

    params = unificar_parametros(contexts)
    for k, v in params_intent.items():
        if v not in ("", None, []):
            params[k] = v

    res={} 



    if action == "tramite_certificado_empadronamiento.crear_peticion" and allParams: #Certificado de empadronamiento
        tel=random.randint(600000000, 999999999) #Genero un número telefónico aleatorio ya que al simularlo con discord no se obtiene este dato. Al subirlo a producción habría que sustituirlo por el número recuperado de la integración telefónica.
        print(params)
        print(req)
        #FIX no se mapean bien los parametros, probablemente la variable params es la erronea, ya que son los params del ultimo intent, que es el de confirmar y no tiene params
        informacion = {
            "nombre" : params.get("nombre",""),
            "apellidos" : params.get("apellidos",{}).get("name",""),
            "dni" : params.get("dni_pasaporte",""),
            "telefono" : params.get("telefono",""),
            "motivo" : params.get("motivo","")
        }
        crear_peticion(telefono=tel, idTramite=1, informacion=informacion)

    elif action == "tramite_cita_AEAT.crear_peticion" and allParams:
        tel=random.randint(600000000, 999999999)

        informacion = {
            "dni" : params.get("dni",""),
            "nombre" : params.get("nombre",{}).get("name",""),
            "servicio" : params.get("servicio",""),
            "modalidad" : params.get("tipo",""),
            "oficina" : params.get("oficina",""),
            "dia" : params.get("dia",""),
            "hora" : params.get("hora",""),
            "email" : params.get("email","")
        }
        crear_peticion(telefono=tel, idTramite=2, informacion=informacion)

    elif action == "tramite_tarjeta_SACYL.crear_peticion" and allParams:
        tel=random.randint(600000000, 999999999)

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





    # if intent == "tramite_certificado_empadronamiento - obtener datos": #Certificado de empadronamiento
    #     if allParams:
            
    #         res = {
    #             "fulfillmentMessages":[
    #                 {
    #                     "text": {
    #                         "text": [
    #                             f"""<speak>Por favor, confírmeme los datos. <break time="450ms"/> 
    #                                 Nombre: {params.get("nombre","")} {params.get("apellidos","")}. <break time="250ms"/>
    #                                 Número de identificación: {params.get("dni_pasaporte","")}. <break time="300ms"/>
    #                                 Teléfono: {params.get("telefono","")}. <break time="200ms"/>
    #                             <emphasis level="moderate">¿Son correctos?</emphasis></speak>"""
    #                         ]
    #                     }
    #                 }
    #             ],
    #             "followupEventInput": {
    #                 "name": "confirmar_si",
    #                 "languageCode": "es-ES",
    #                 "parameters": allParams
    #             }
    #         }

    # #FIX para activar un intent no sirve con poner un contexto, hay que añadir un evento
    # elif intent == INTENTS[6]: #Cita AEAT
    #     if allParams:

    #         df = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data/tramite2.csv"), sep=";")
    #         llamada = df.loc[df["servicio"] == params.get("servicio",""), "llamada"].iloc[0]
    #         print(params.get("servicio",""), llamada)
    #         if llamada:
    #             res = {
    #                 "outputContexts": [
    #                     {
    #                         "name": f"{req["session"]}/contexts/aeat_modalidad",
    #                         "lifespanCount":5,
    #                         "parameters": params
    #                     }
    #                 ]
    #             }
    #             print(res)
    #         else:
    #             res = {
    #                 "outputContexts": [
    #                     {
    #                         "name": f"{req["session"]}/contexts/aeat_presencial",
    #                         "lifespanCount":5,
    #                         "parameters": params
    #                     }
    #                 ]
    #             }

    # elif intent == INTENTS[7]: #Tarjeta sanitaria SACYL
    #     if allParams:
            
    #         res = {
    #             "fulfillmentMessages":[
    #                 {
    #                     "text": {
    #                         "text": [
    #                             f"""<speak>Por favor, confírmeme los datos. <break time="450ms"/> 
    #                                 Nombre: {params.get("nombre","")} {params.get("primer_apellido","")}. <break time="250ms"/>
    #                                 Fecha de nacimiento: {params.get("nacimiento","")}. <break time="300ms"/>
    #                                 Centro de salud: {params.get("centro_salud","")}. <break time="200ms"/>
    #                                 Dirección: {params.get("calle","")}, {params.get("numero","")} {params.get("piso","")} {params.get("puerta","")}, <break time="250ms"/> {params.get("localidad","")}.
    #                             <emphasis level="moderate">¿Son correctos?</emphasis></speak>"""
    #                         ]
    #                     }
    #                 }
    #             ],
    #             "outputContexts": [
    #                 {
    #                     "name": f"{req["session"]}/contexts/esperando_confirmacion",
    #                     "lifespanCount":5,
    #                     "parameters": params
    #                 }
    #             ]
    #         }

    # elif intent == INTENTS[3]: #Cita AEAT Presencial
    #     if allParams:
            
    #         res = {
    #             "fulfillmentMessages":[
    #                 {
    #                     "text": {
    #                         "text": [
    #                             f"""<speak>Por favor, confírmeme los datos. <break time="450ms"/> 
    #                                 Nombre: {params.get("nombre","")}. <break time="250ms"/>
    #                                 Número de identificación: {params.get("dni","")}. <break time="300ms"/>
    #                                 Servicio: {params.get("servicio","")}. <break time="200ms"/>
    #                                 Oficina: {params.get("oficina","")}. <break time="350ms"/>
    #                                 Agendada para el día {params.get("dia","")} a las {params.get("hora","")}. <break time="300ms"/>
    #                             <emphasis level="moderate">¿Son correctos?</emphasis></speak>"""
    #                         ]
    #                     }
    #                 }
    #             ],
    #             "outputContexts": [
    #                 {
    #                     "name": f"{req["session"]}/contexts/esperando_confirmacion",
    #                     "lifespanCount":5,
    #                     "parameters": params
    #                 }
    #             ]
    #         }

    # elif intent == INTENTS[2]: #Cita AEAT Modalidad
    #     if allParams:
    #         if params.get("modalidad","") == "presencial":
    #             res = {
    #                 "outputContexts": [
    #                     {
    #                         "name": f"{req["session"]}/contexts/aeat_presencial",
    #                         "lifespanCount":5,
    #                         "parameters": params
    #                     }
    #                 ]
    #             }
    #         else:
    #             res = {
    #                 "fulfillmentMessages":[
    #                     {
    #                         "text": {
    #                             "text": [
    #                                 f"""<speak>Por favor, confírmeme los datos. <break time="450ms"/> 
    #                                     Nombre: {params.get("nombre","")}. <break time="250ms"/>
    #                                     Número de identificación: {params.get("dni","")}. <break time="300ms"/>
    #                                     Servicio: {params.get("servicio","")}. <break time="200ms"/>
    #                                 <emphasis level="moderate">¿Son correctos?</emphasis></speak>"""
    #                             ]
    #                         }
    #                     }
    #                 ],
    #                 "outputContexts": [
    #                     {
    #                         "name": f"{req["session"]}/contexts/esperando_confirmacion",
    #                         "lifespanCount":5,
    #                         "parameters": params
    #                     }
    #                 ]
    #             }

    # #TODO ver si es posible colgar llamada
    # elif intent == INTENTS[4]: #Datos Correctos
    #     tel=random.randint(600000000, 999999999) #Genero un número telefónico aleatorio ya que al simularlo con discord no se obtiene este dato. Al subirlo a producción habría que sustituirlo por el número recuperado de la integración telefónica.

    #     for context in req["queryResult"]["outputContexts"]:
    #         if context["name"] == f"{req["session"]}/contexts/esperando_confirmacion":
    #             parametros_confirmados = context["parameters"]

    #     if parametros_confirmados.get("tramite","") == "certificado de empadronamiento":
    #         informacion = {
    #             "nombre" : parametros_confirmados.get("nombre",""),
    #             "apellidos" : parametros_confirmados.get("apellidos",{}).get("name",""),
    #             "dni" : parametros_confirmados.get("dni_pasaporte",""),
    #             "telefono" : parametros_confirmados.get("telefono",""),
    #             "motivo" : parametros_confirmados.get("motivo","")
    #         }
    #         crear_peticion(telefono=tel, idTramite=1, informacion=informacion)
    #     elif parametros_confirmados.get("tramite","") == "cita aeat":
    #         informacion = {
    #             "dni" : parametros_confirmados.get("dni",""),
    #             "nombre" : parametros_confirmados.get("nombre",{}).get("name",""),
    #             "servicio" : parametros_confirmados.get("servicio",""),
    #             "modalidad" : parametros_confirmados.get("tipo",""),
    #             "oficina" : parametros_confirmados.get("oficina",""),
    #             "dia" : parametros_confirmados.get("dia",""),
    #             "hora" : parametros_confirmados.get("hora",""),
    #             "email" : parametros_confirmados.get("email","")
    #         }
    #         crear_peticion(telefono=tel, idTramite=2, informacion=informacion)
    #     elif parametros_confirmados.get("tramite","") == "tarjeta sanitaria sacyl":
    #         informacion = {
    #             "nombre" : parametros_confirmados.get("nombre",""),
    #             "apellido1" : parametros_confirmados.get("primer_apellido",""),
    #             "nacimiento" : parametros_confirmados.get("nacimiento",""),
    #             "motivo" : parametros_confirmados.get("motivo",""),
    #             "centro_salud" : parametros_confirmados.get("contro_salud",""),
    #             "localidad" : parametros_confirmados.get("localidad",""),
    #             "calle" : parametros_confirmados.get("calle",""),
    #             "numero" : parametros_confirmados.get("numero",""),
    #             "piso" : parametros_confirmados.get("piso",""),
    #             "puerta" : parametros_confirmados.get("puerta","")
    #         }
    #         crear_peticion(telefono=tel, idTramite=3, informacion=informacion)

    #TODO Falta logica de datos incorrectos
    return jsonify(res)


def unificar_parametros(contextos):
    params = {}

    for c in contextos:
        params_contexto = c.get("parameters", {})

        for key, value in params_contexto.items():
            if key.endswith(".original") or value in ("", None, []):
                continue

            params[key] = value
    
    return params