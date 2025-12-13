from flask import Blueprint, request, jsonify


dialogflow_webhook_bp = Blueprint('dialogflow_webhook', __name__)


@dialogflow_webhook_bp.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    print(req)
    intent = req["queryResult"]["intent"]["displayName"]
    params = req["queryResult"]["parameters"]
    

    if intent == "tramite_certificado_empadronamiento":
        if req["allRequiredParamspresent"]:
            print("YA todos parametros, proceder comprobacion")
        #TODO crear peticion con los datos
    
    if intent == "tramite_cita_AEAT":
        if req["allRequiredParamspresent"]:
            print("YA todos parametros, proceder comprobacion")
        #TODO crear peticion con los datos

    if intent == "tramite_tarjeta_SACYL":
        if req["allRequiredParamspresent"]:
            print("YA todos parametros, proceder comprobacion")
        #TODO crear peticion con los datos

    return