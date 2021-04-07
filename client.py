import sys
import pprint    # Esto es para imprimir "guapo" estructuras de datos largas
import requests  # Esto es para hacer peticiones web


def enviar_peticion(nombre_fichero, model="x", augment=False, tipo="json", 
                    url="http://156.35.151.156:5000/detect"):
    """Esta función envía una petición POST al servidor Yolo en la que adjunta un fichero.

    Parámetros:
    
    - nombre_fichero: nombre del fichero a adjuntar en la petición
    - model: letra "x" o "s" según se quiera probar el modelo xlarge o el small
    - augment: True o False según se quiera o no aplicar augmentation
    - tipo: cadena "json" o "fichero" según el formato deseado de la respuesta
    - url: URL al servicio
 
    Todos los parámetros salvo el nombre del fichero son opcionales, con valores por defecto
    """

    f=open(nombre_fichero, "rb")

    # La petición es simplemente una línea. Hay que pasar 3 parámetros al post
    #
    # El primero es la URL a la que se hace el POST
    # El segundo es un diccionario `data` cuyos campos son los del FORM que
    #    espera el servidor.
    # El tercero `files` es un diccionario que lleva por claves los nombres 
    #    de los campos que espera el servidor (espera solo uno llamado "file")
    #    y los valores son parejas (nombre_fichero, handle_de_fichero_abierto)
    #
    # El método se ocupa de codificar todo eso en un cuerpo multipart-mime
    # tal como se espera en el protocolo HTTP
    data = {"model": model, "tipo": tipo}
    if augment:
       data["augment"] = "yes"
    r = requests.post(url, data=data, files={"file": (nombre_fichero,f)})

    # Retornar resultado si todo ok
    if r.status_code==200:
       return r
    else:
       print(r.status_code, r.reason)
       return None

def main():
    """El programa principal toma las opciones de línea de comandos
    y se limita a invocar al método anterior y mostrar el resultado
    si es json"""
    if len(sys.argv) < 2:
       print("Uso: {} fichero_imagen [model] [augment] [tipo-result] [url]".format(sys.argv[0]))
       print("Ejemplo: {} zidane.jpg s true json http://156.35.151.156:5000/detect".format(sys.argv[0]))
       quit()

    fichero = sys.argv[1]
    model = "x"
    augment = False
    tipo = "json"
    url = "http://156.35.151.156:5000/detect"
    if len(sys.argv) > 2:
       model = sys.argv[2]
       if model not in ["s", "x"]:
          model = "x"
    if len(sys.argv) >3:
       augment = sys.argv[3].lower() == "true"
    if len(sys.argv) > 4:
       tipo = sys.argv[4]
       if tipo.lower() not in ["imagen", "json"]:
          tipo = "json"
    if len(sys.argv) > 5:
       url = sys.argv[5]
    
    print(fichero, model, augment, tipo, url)
    respuesta = enviar_peticion(fichero, model, augment, tipo, url)

    if respuesta:
       if tipo=="json":
          pprint.pprint(respuesta.json())
       else:
          print("Recibida imagen de {} bytes".format(len(respuesta.content)))
          with open(fichero+".result", "wb") as f:
             f.write(respuesta.content)
    else:
       print("Error")

if __name__ == "__main__":
    main()

