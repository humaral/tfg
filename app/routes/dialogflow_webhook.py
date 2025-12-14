from flask import Blueprint, request, jsonify
from app.utils import crear_peticion
import random


dialogflow_webhook_bp = Blueprint('dialogflow_webhook', __name__)


INTENTS = ["bienvenida", "cambiar_campo", "cita_AEAT_Presencial", "cita_AEAT_Virtual", "confirmar_datos", "confirmar_no", "confirmar_si", "tramite_certificado_empadronamiento", "tramite_cita_AEAT", "tramite_tarjeta_SACYL"]


@dialogflow_webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    
    intent = req["queryResult"]["intent"]["displayName"]
    params = req["queryResult"]["parameters"]
    allParams = req["queryResult"].get("allRequiredParamsPresent", False)
    res={}

    if intent == INTENTS[7]: #Certificado de empadronamiento
        if allParams:
            
            res = {
                "fulfillmentMessages":[
                    {
                        "text": {
                            "text": [
                                f"""<speak>Por favor, confírmeme los datos. <break time="450ms"/> 
                                    Nombre: {params["nombre"]} {params["apellidos"]}. <break time="250ms"/>
                                    Número de identificación: {params["dni_pasaporte"]}. <break time="300ms"/>
                                    Teléfono: {params["telefono"]}. <break time="200ms"/>
                                <emphasis level="moderate">¿Son correctos?</emphasis></speak>"""
                            ]
                        }
                    }
                ],
                "outputContexts": [
                    {
                        "name": f"{req["session"]}/contexts/esperando_confirmacion",
                        "lifespanCount":5,
                        "parameters": params
                    }
                ]
            }

    elif intent == INTENTS[8]: #Cita AEAT
        if allParams:
            
            if params["tipo"]=="presencial":
                res = {
                    "outputContexts": [
                        {
                            "name": f"{req["session"]}/contexts/aeat_presencial",
                            "lifespanCount":5,
                            "parameters": params
                        }
                    ]
                }
            else:
                res = {
                    "outputContexts": [
                        {
                            "name": f"{req["session"]}/contexts/aeat_virutal",
                            "lifespanCount":5,
                            "parameters": params
                        }
                    ]
                }

    elif intent == INTENTS[9]: #Tarjeta sanitaria SACYL
        if allParams:
            
            res = {
                "fulfillmentMessages":[
                    {
                        "text": {
                            "text": [
                                f"""<speak>Por favor, confírmeme los datos. <break time="450ms"/> 
                                    Nombre: {params["nombre"]} {params["primer_apellido"]}. <break time="250ms"/>
                                    Fecha de nacimiento: {params["nacimiento"]}. <break time="300ms"/>
                                    Centro de salud: {params["centro_salud"]}. <break time="200ms"/>
                                    Dirección: {params["calle"]}, {params["numero"]} {params["piso"]} {params["puerta"]}, <break time="250ms"/> {params["localidad"]}.
                                <emphasis level="moderate">¿Son correctos?</emphasis></speak>"""
                            ]
                        }
                    }
                ],
                "outputContexts": [
                    {
                        "name": f"{req["session"]}/contexts/esperando_confirmacion",
                        "lifespanCount":5,
                        "parameters": params
                    }
                ]
            }

    elif intent == INTENTS[2]: #Cita AEAT Presencial
        if allParams:
            
            res = {
                "fulfillmentMessages":[
                    {
                        "text": {
                            "text": [
                                f"""<speak>Por favor, confírmeme los datos. <break time="450ms"/> 
                                    Nombre: {params["nombre"]}. <break time="250ms"/>
                                    Número de identificación: {params["dni"]}. <break time="300ms"/>
                                    Servicio: {params["servicio"]}. <break time="200ms"/>
                                    Oficina: {params["oficina"]}. <break time="350ms"/>
                                    Agendada para el día {params["dia"]} a las {params["hora"]}. <break time="300ms"/>
                                <emphasis level="moderate">¿Son correctos?</emphasis></speak>"""
                            ]
                        }
                    }
                ],
                "outputContexts": [
                    {
                        "name": f"{req["session"]}/contexts/esperando_confirmacion",
                        "lifespanCount":5,
                        "parameters": params
                    }
                ]
            }

    elif intent == INTENTS[3]: #Cita AEAT Virtual
        if allParams:
            
            res = {
                "fulfillmentMessages":[
                    {
                        "text": {
                            "text": [
                                f"""<speak>Por favor, confírmeme los datos. <break time="450ms"/> 
                                    Nombre: {params["nombre"]}. <break time="250ms"/>
                                    Número de identificación: {params["dni"]}. <break time="300ms"/>
                                    Servicio: {params["servicio"]}. <break time="200ms"/>
                                    Email: {params["email"]}. <break time="350ms"/>
                                <emphasis level="moderate">¿Son correctos?</emphasis></speak>"""
                            ]
                        }
                    }
                ],
                "outputContexts": [
                    {
                        "name": f"{req["session"]}/contexts/esperando_confirmacion",
                        "lifespanCount":5,
                        "parameters": params
                    }
                ]
            }

    elif intent == INTENTS[6]: #Datos Correctos
        tel=random.randint(600000000, 999999999) #Genero un número telefónico aleatorio ya que al simularlo con discord no se obtiene este dato. Al subirlo a producción habría que sustituirlo por el número recuperado de la integración telefónica.

        for context in req["queryResult"]["outputContexts"]:
            if context["name"] == f"{req["session"]}/contexts/esperando_confirmacion":
                parametros_confirmados = context["parameters"]

        if parametros_confirmados["tramite"] == "certificado de empadronamiento":
            informacion = {
                "nombre" : parametros_confirmados["nombre"],
                "apellidos" : parametros_confirmados["apellidos"]["name"],
                "dni" : parametros_confirmados["dni_pasaporte"],
                "telefono" : parametros_confirmados["telefono"],
                "motivo" : parametros_confirmados["motivo"]
            }
            crear_peticion(telefono=tel, idTramite=1, informacion=informacion)
        elif parametros_confirmados["tramite"] == "cita aeat":
            informacion = {
                "dni" : parametros_confirmados["dni"],
                "nombre" : parametros_confirmados["nombre"]["name"],
                "servicio" : parametros_confirmados["servicio"],
                "modalidad" : parametros_confirmados["tipo"],
                "oficina" : parametros_confirmados["oficina"],
                "dia" : parametros_confirmados["dia"],
                "hora" : parametros_confirmados["hora"],
                "email" : parametros_confirmados["email"],
            }
            crear_peticion(telefono=tel, idTramite=2, informacion=informacion)
        elif parametros_confirmados["tramite"] == "tarjeta sanitaria sacyl":
            informacion = {
                "nombre" : parametros_confirmados["nombre"],
                "apellido1" : parametros_confirmados["primer_apellido"],
                "nacimiento" : parametros_confirmados["nacimiento"],
                "motivo" : parametros_confirmados["motivo"],
                "centro_salud" : parametros_confirmados["centro_salud"],
                "localidad" : parametros_confirmados["localidad"],
                "calle" : parametros_confirmados["calle"],
                "numero" : parametros_confirmados["numero"],
                "piso" : parametros_confirmados["piso"],
                "puerta" : parametros_confirmados["puerta"]
            }
            crear_peticion(telefono=tel, idTramite=3, informacion=informacion)

    #TODO Falta logica de datos incorrectos
    return jsonify(res)