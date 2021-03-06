def Draw_BBOX(detection, rows, cols, classes):
    score = float(detection[2])
    index = int(detection[1])
    Xstart = detection[3] * cols
    Ystart = detection[4] * rows
    Xend = detection[5] * cols
    Yend = detection[6] * rows
    label = "{} {:.2f}%" .format(classes[index],score * 100)
    cv2.putText(img, label, (int(Xstart), int(Ystart)+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
    cv2.rectangle(img, (int(Xstart), int(Ystart)), (int(Xend), int(Yend)), (0,0,255),thickness = 2)

def read_classes():
    labels = open('labels.txt').read().strip().split("\n")
    classes = [r[r.find(" ") + 1:].split(",")[0] for r in labels]
    return classes

def Inference_Time(cont, soma):
    print("cont = {}" .format(cont))
    print("Media = {:.2} segundos" .format(soma/cont))

import numpy as np 
import time
import cv2

# Lendo a rede. NOTA: Se o arquivo ".pbtxt" não vier, utilizar o arquivo "tf_text_graph_ssd.py" para gerá-lo
tensorflowNet = cv2.dnn.readNetFromTensorflow('frozen_inference_graph.pb', 'frozen_inference_graph.pbtxt')

# Lendo do arquivo de labels e transformando em um array de strings
classes = read_classes()

# soma é o total de tempo de inferencia, e cont é o numero de frames analisados
soma = cont = 0

# passando 0 como argumento, ele lê da WebCam, caso queira um vídeo, mandar o caminho para o arquivo de vídeo entre ''
cap = cv2.VideoCapture(0)


while(True):
    # Lendo Frame
    ret, img = cap.read()

    # Dimensões do Frame
    rows, cols = img.shape[:2]

    # O modelo SSD utiliza imagens de tamanho (300,300)
    blob = cv2.dnn.blobFromImage(img, size = (300,300), swapRB = True, crop = False)
    tensorflowNet.setInput(blob)

    # Passando a imagem pela rede e recebendo um output
    start = time.time()
    detections = tensorflowNet.forward()
    end =  time.time()

    soma = soma + (end-start)
    cont = cont+1

    # Passando por todos os objetos detectados e limitando o score acima de 20%
    for detection in (detections[0,0]):
        score = float(detection[2])
        if(score > 0.2):
            Draw_BBOX(detection, rows, cols, classes)
    
    cv2.imshow("Image", img)
    
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

Inference_Time(cont, soma)
cap.release()
cv2.destroyAllWindows()