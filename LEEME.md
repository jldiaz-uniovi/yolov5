# Versión "server" con Flask

Una vez instalado Yolov5 y comprobándose que funciona mediante el script `test.py` o `detect.py`,
es necesario seguir los siguientes pasos para la versión "server":

1. Instalar flask (`pip install flask`) en el mismo entorno de desarrollo
2. Crear carpetas `server/uploads` y `server/detections` donde van quedando las imágenes que se suben vía Web y los resultados de las detecciones
3. Lanzar el servidor de desarrollo con `FLASK_APP=server.py flask run`
4. O el servidor de producción con ./start-gunicorn.sh (este lanza 2*cores+1 procesos)

Conectando un navegador al servidor `:5000/detect` sale un formulario para subir un fichero. Tras unos instantes aparecerá el resultado del etiquetado.

Se aconseja poner nginx como proxy reverso por delante, escuchando en el puerto 80.

## Cómo funciona

El servidor flask importa la función `detect()` de `mini_detect.py` que es una implementación mía (inspirada en lo que fui leyendo en `detect.py`, pero dejándolo en lo mínimo necesario para este caso).

Al arrancar el servidor se precargan los modelos "yolov5s" y "yolov5x" en memoria (por cada proceso, lo que requiere algo más de 4GB). Se presenta al usuario un formulario para que suba el fichero, con opciones para:

* Elegir qué modelo yolo usar en la detección
* Elegir si se quiere o no usar "augmentation" en la detección
* Elegir si se quiere el resultado en forma de imagen o de JSON


## TO-DO

* El cliente podría ser más listo, usando JS, y hacer que sea él quien dibuja las cajas con el JSON recibido. Eso permitiría además mejoras en la GUI, como que al mover el ratón se ilumine sólo la caja señalada y se oculten las demás, por ejemplo.

