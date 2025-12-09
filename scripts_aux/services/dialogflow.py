import os, tempfile, json
from google.cloud import dialogflow_v2, texttospeech
from dotenv import load_dotenv

if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
    load_dotenv()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("DIALOGFLOW_CREDENTIALS")
credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
with open(credentials) as f:
    PROJECT_ID = json.load(f)["project_id"]

dialogflow_client = dialogflow_v2.SessionsClient()


def enviar_texto(session_id, user_text=None, bienvenida=False):
     
    session = dialogflow_client.session_path(PROJECT_ID, session_id)

    audio_config = dialogflow_v2.OutputAudioConfig(
        audio_encoding=dialogflow_v2.OutputAudioEncoding.OUTPUT_AUDIO_ENCODING_LINEAR_16,
        sample_rate_hertz = 16000    
    )
    
    if bienvenida:
        event_input = dialogflow_v2.EventInput(name="WELCOME", language_code="es")
        query_input = dialogflow_v2.QueryInput(event=event_input)
    elif user_text:
        text_input = dialogflow_v2.TextInput(text=user_text, language_code="es")
        query_input = dialogflow_v2.QueryInput(text=text_input)
    else:
        return 

    response = dialogflow_client.detect_intent(request={"session":session, "query_input":query_input, "output_audio_config":audio_config})
    texto = response.query_result.fulfillment_text
    audio = response.output_audio
    return texto, audio


