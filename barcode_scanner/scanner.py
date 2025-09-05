import cv2
from zxingcpp import read_barcode

def get_barcode():

    # 0 é o dispositivo padrão de captura de imagem, caso haja algum erro alterar para 1 ou 2
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Erro ao abrir a webcam.")
        return None

    texto_lido = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Falha ao capturar frame.")
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = read_barcode(rgb)

        if result:
            codigo_lido = result.text
            print("Código:", codigo_lido)

            # desenha retangulo em volta do código detectado
            if result.position:
                pts = [
                    (result.position.top_left.x, result.position.top_left.y),
                    (result.position.top_right.x, result.position.top_right.y),
                    (result.position.bottom_right.x, result.position.bottom_right.y),
                    (result.position.bottom_left.x, result.position.bottom_left.y),
                ]

                for i in range(len(pts)):
                    pt1 = pts[i]
                    pt2 = pts[(i + 1) % len(pts)]
                    cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

                # escreve o texto acima do codigo
                cv2.putText(frame, codigo_lido, (pts[0][0], pts[0][1] - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

            # mostra o frame final por 1 segundo antes de fechar
            cv2.imshow("Leitor de Codigos", frame)
            cv2.waitKey(1000)
            break

        cv2.imshow("Leitor de Codigos", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
    return codigo_lido



