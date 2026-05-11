# Autor: Hugo Martín Alonso
# Fecha: 05/12/2025
# Descripción: Funciones para normalizar textos y que el stt de vosk reconozca bien números y letras.


NUMEROS = {
    "cero":"0","uno":"1", "un":"1", "dos":"2","tres":"3","cuatro":"4","cinco":"5",
    "seis":"6","siete":"7","ocho":"8","nueve":"9"
}

LETRAS = {
    "a":"A", "be":"B", "ce":"C", "e":"E", "efe":"F", "ge":"G", "hache":"H", "i":"I", "jota":"J",
    "ca":"K", "ka":"K", "ele":"L", "eme":"M", "ene":"N", "eñe":"Ñ", "o":"O", "pe":"P", "cu":"Q", "erre":"R", "ese":"S",
    "te":"T", "u":"U", "uve":"V", "uve doble":"W", "equis":"X", "i griega":"Y", "ceta":"Z", 
    "b":"B", "c":"C", "f":"F", "g":"G", "h":"H", "j":"J", "k":"K", "l":"L", "m":"M", "n":"N",
    "ñ":"Ñ", "p":"P", "q":"Q", "r":"R", "s":"S", "t":"T", "v":"V", "w":"W", "x":"X", "y":"Y", "z":"Z"
}

def transcribir_numeros_letras(texto):
    words = texto.lower().split()
    result = []
    buffer = ""

    for w in words:
        if w in NUMEROS:
            buffer += NUMEROS[w]
        elif w in LETRAS:
            buffer += LETRAS[w]
        elif w.isdigit():
            buffer += w
        else:
            if buffer:
                result.append(buffer)
                buffer = ""
            result.append(w)

    if buffer:
        result.append(buffer)

    return " ".join(result)