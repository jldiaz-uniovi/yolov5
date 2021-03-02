import sys
import time
from pathlib import Path
import random
from collections import Counter
import torch
import cv2

# Implementación propia de lo mínimo necesario para hacer la detección, que en realidad se
# reduce a un par de líneas: cargar el modelo, y aplicarlo sobre una imagen

# Se proporcionan dos funciones para ello, la que carga el modelo se ocupa de bajarlo
# de torch.hub si no estaba previamente descargado. La segunda (detect) usa ese modelo
# sobre una imagen y retorna el objeto de resultados (al que añade un campo .time con el
# tiempo que tomó la detección de objetos)
#
# Otras dos funciones usan el objeto de resultados para generar a partir de él una imagen
# con cajas de colores, o bien un JSON con la información sobre esas cajas.

def load_model(model_name):
    """Load the model from torch.hub

    model_name: one of "yolov5s", "yolov5m", "yolov5l", "yolov5x"
    """

    return torch.hub.load('ultralytics/yolov5', model_name, pretrained=True)


def detect(imagename, model, augment=False):
    """Applies the model on the image and returns the object with the results"""
    
    t1 = time.time()
    r= model(imagename, augment=augment)
    t2 = time.time()
    r.time = t2-t1
    r.augment = augment
    return r


def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    """Adds one bounding box with optional label to the image"""

    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

def label_image(p, results, save_dir):
    """Takes the results of the detection and draws several bounding boxes 
    with labels on the image.

    p: 
        relative path and filename of the source image
    results: 
        the object returned by detect
    save_dir: 
        name of the folder to save the labelled image
    """

    p = Path(p)
    save_dir = Path(save_dir)
    save_path = str(save_dir / p.name) 
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in results.names]

    im0 = cv2.imread(str(p))
    # im0 = results.imgs[0]
    for *xyxy, conf, clase in reversed(results.xyxy[0]):
        label = f"{results.names[int(clase)]} {conf:.2f}"
        plot_one_box(
            xyxy,
            im0,
            label=label,
            color=colors[int(clase)],
            line_thickness=1,
        )

    # Save results (image with detections)
    cv2.imwrite(save_path, im0)


def get_meta(results):
    """Extracts relevant information from the results of the detection
    and generates a Python dictionary with it.

    results:
        The result object returned by detect

    returns:
        Python dictionary
    """

    meta = {
        "meta": {
            "file": results.files[0],
            "time": results.time,
            "augment": results.augment,
        },
        "results": [],
    }
    res = []
    for *xyxy, conf, clase in results.xyxy[0]:
        label = results.names[int(clase)]
        dic = {
            "bounding_box": [int(x) for x in xyxy],
            "confidence": conf.item(),
            "label": label
        }
        meta["results"].append(dic)
        res.append(label)
    meta["_summary"] = dict(Counter(res))
    return meta


# Example of usage
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage:")
        print(f"{sys.argv[0]} filename")
        quit()
    filename = sys.argv[1]
    model = load_model("yolov5s")
    r= detect(filename, model)
    # r.print()
    # label_image(filename, r, ".")
    print(get_meta(r))