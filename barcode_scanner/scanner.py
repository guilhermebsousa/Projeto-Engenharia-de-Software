import cv2
from pyzbar.pyzbar import decode
import numpy as np

def getBarcode():

    video = cv2.VideoCapture(0)
    

    while True:
        ret, frame = video.read()
        
        if not ret:
            break
        
        codigos = decode(frame)

        for codigo in codigos:
            print("Dados", codigo.data.decode("utf-8"))
            
            pts = codigo.polygon
            pts = [(p.x, p.y) for p in pts]
            cv2.polylines(frame, [np.array(pts)], True, (0,255,0), 2)
        
        
        cv2.imshow("Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q') or codigos:
            break

    video.release()
    cv2.destroyAllWindows()

    return codigos



