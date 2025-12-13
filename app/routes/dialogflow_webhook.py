from flask import Blueprint, request, jsonify
from app.utils import crear_peticion
import random


dialogflow_webhook_bp = Blueprint('dialogflow_webhook', __name__)


INTENTS = ["bienvenida", "cambiar_campo", "cita_AEAT_Presencial", "cita_AEAT_Virtual", "confirmar_datos", "confirmar_no", "confirmar_si", "tramite_certificado_empadronamiento", "tramite_cita_AEAT", "tramite_tarjeta_SACYL"]
TRAMITES = {"Certificado de empadronamiento":1, "Cita AEAT":2, "Tarjeta Sanitaria SACYL":3}
#DELETE si sobra
CERTIFICADO_EMPADRONAMIENTO = {"tramite":"", "nombre":"", "apellidos":"", "dni_pasaporte":"", "telefono":"", "motivo":""}
CITA_AEAT = {"tramite":"", "dni":"", "nombre":"", "servicio":"", "tipo":"", "oficina":"", "dia":"", "hora":"", "email":""}
TARJETA_SACYL = {"tramite":"", "motivo":"", "nombre":"", "primer_apellido":"", "nacimiento":"", "centro_salud":"", "localidad":"", "calle":"", "numero":"", "piso":"", "puerta":""}

@dialogflow_webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    print(req) #DELETE
    intent = req["queryResult"]["intent"]["displayName"]
    params = req["queryResult"]["parameters"]
    res={}

    if intent == INTENTS[7]: #Certificado de empadronamiento
        if req["allRequiredParamspresent"]:
            
            res = {
                "fulfillmentMessages":[
                    {
                        "text": {
                            "text": [
                                f"""<speak>Por favor, confírmeme los datos. <break time=450ms/> 
                                    Nombre: {params["nombre"]} {params["apellidos"]}. <break time=250ms/>
                                    Número de identificación: {params["dni_pasaporte"]}. <break time=300ms/>
                                    Teléfono: {params["telefono"]}. <break time=200ms/>
                                <emphasis>¿Son correctos?</emphasis></speak>"""
                            ]
                        }
                    }
                ],
                "outputContexts": [
                    {
                        "name": f"{req["session"]}/contexts/esperando_confirmacion",
                        "lifespanCount":5,
                        "parameters": certificado_empadronamiento
                    }
                ]
            }

    elif intent == INTENTS[8]: #Cita AEAT
        if req["allRequiredParamspresent"]:
            
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
        if req["allRequiredParamspresent"]:
            
            res = {
                "fulfillmentMessages":[
                    {
                        "text": {
                            "text": [
                                f"""<speak>Por favor, confírmeme los datos. <break time=450ms/> 
                                    Nombre: {params["nombre"]} {params["primer_apellido"]}. <break time=250ms/>
                                    Fecha de nacimiento: {params["nacimiento"]}. <break time=300ms/>
                                    Centro de salud: {params["centro_salud"]}. <break time=200ms/>
                                    Dirección: {params["calle"]}, {params["numero"]} {params["piso"]} {params["puerta"]}, <break time=250ms/> {params["localidad"]}.
                                <emphasis>¿Son correctos?</emphasis></speak>"""
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
        if req["allRequiredParamspresent"]:
            
            res = {
                "fulfillmentMessages":[
                    {
                        "text": {
                            "text": [
                                f"""<speak>Por favor, confírmeme los datos. <break time=450ms/> 
                                    Nombre: {params["nombre"]}. <break time=250ms/>
                                    Número de identificación: {params["dni"]}. <break time=300ms/>
                                    Servicio: {params["servicio"]}. <break time=200ms/>
                                    Oficina: {params["oficina"]}. <break time=350ms/>
                                    Agendada para el día {params["dia"]} a las {params["hora"]}. <break time=300ms/>
                                <emphasis>¿Son correctos?</emphasis></speak>"""
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
        if req["allRequiredParamspresent"]:
            
            res = {
                "fulfillmentMessages":[
                    {
                        "text": {
                            "text": [
                                f"""<speak>Por favor, confírmeme los datos. <break time=450ms/> 
                                    Nombre: {params["nombre"]}. <break time=250ms/>
                                    Número de identificación: {params["dni"]}. <break time=300ms/>
                                    Servicio: {params["servicio"]}. <break time=200ms/>
                                    Email: {params["email"]}. <break time=350ms/>
                                <emphasis>¿Son correctos?</emphasis></speak>"""
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
        if params["tramite"]:
            crear_peticion(telefono=tel, idTramite=TRAMITES[params["tramite"]], informacion=params)

    #TODO Falta logica de datos incorrectos

    return jsonify(res)