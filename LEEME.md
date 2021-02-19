# Versión "server" con Flask

Una vez instalado Yolov5 y comprobándose que funciona mediante el script `test.py` o `detect.py`,
es necesario seguir los siguientes pasos para la versión "server":

1. Instalar flask (`pip install flask`) en el mismo entorno de desarrollo
2. Crear carpetas `server/uploads` y `server/detections` donde van quedando las imágenes que se suben vía Web y los resultados de las detecciones
3. Lanzar el servidor de desarrollo con `FLASK_APP=server.py flask run`

Conectando un navegador al servidor `:5000/detect` sale un formulario para subir un fichero. Tras unos instantes aparecerá el resultado del etiquetado.

## Cómo funciona

El servidor flask importa la función `detect()` de `my_detect.py` que básicamente es un _fork_ del `detect.py` que viene con Yolov5 siendo la única diferencia que se ha eliminado la variable global `opt` a través de la que recibía opciones varias, y se ha sustituido por parámetros para la función `detect()`, la mayoría con valores por defecto salvo el primero que es la ruta al archivo a detectar. 

Los valores por defecto de esa función hacen que use un modelo de tamaño mediano (yolov5m), que genere una imagen con rectángulos etiquetados (en vez de una versión solo texto), que lo deje en la carpeta, que use CPU en vez de GPU, que normalice la imagen a un ancho de 640, y otros valores de umbrales que no sé bien a qué se refieren.

## TO-DO

* La función `detect()` carga el modelo cada vez que se la invoca. Se podría hacer que el modelo lo cargue Flask al arrancar y se lo pase como parámetro para ganar tiempo.

* Debería haber una ruta Flask que devuelva el resultado del etiquetado en JSON, en vez de en una imagen. Eso implica modificar `detect()` para que pueda retornar el tensor de resultados, y los nombres de las etiquetas en el modelo. Flask podría componer un JSON con eso.

* La función `detect()` se podría modificar para que reciba directamente la imagen (que se la pasaría Flask según la recibe del usuario), evitando tener que usar un fichero como intermediario. También podría devolver directamente la imagen.

* El cliente podría ser más listo, usando JS, y hacer que sea él quien dibuja las cajas con el JSON recibido. Eso permitiría además mejoras en la GUI, como que al mover el ratón se ilumine sólo la caja señalada y se oculten las demás, por ejemplo.

