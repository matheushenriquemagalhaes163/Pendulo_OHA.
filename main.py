import cv2
import csv

source = cv2.VideoCapture('pendulo.mp4')

# OBTÉM FPS DO VÍDEO (FRAMES POR SEGUNDO)
fps = source.get(cv2.CAP_PROP_FPS)

# CRIA O ARQUIVO CSV PARA SALVAR OS DADOS
data = open('dados.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(data)


# LÊ O PRIMEIRO FRAME
ok, frame = source.read()
if not ok:
    print("❌ Erro ao carregar o primeiro frame do vídeo.")
    source.release()
    exit()


# SELECIONE MANUALMENTE O OBJETO A SER RASTREADO
cv2.namedWindow("Tracker", cv2.WINDOW_NORMAL)
bbox = cv2.selectROI("Tracker", frame)
color = (204, 255, 0)


# CRIA O TRACKER
tracker = cv2.TrackerCSRT_create()
tracker.init(frame, bbox)


# TEMPO INICIAL
t = 0.0


while True:
    ok, frame = source.read()
    if not ok:
        print("✅ Fim do vídeo ou erro de leitura.")
        break


    success, box = tracker.update(frame)
    if not success:
        print("⚠️ Perda de rastreamento — finalize ou selecione novamente o objeto.")
        break


    x, y, w, h = [int(v) for v in box]


    # DESENHA O RETÂNGULO DE RASTREAMENTO
    cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)


    # CALCULA O TEMPO (EM SEGUNDOS)
    t += 1 / fps


    # CALCULA A POSIÇÃO (AJUSTE ESSES VALORES CONFORME SEU SISTEMA)
    # --> MODIFIQUE OS VALORES ABAIXO DE ACORDO COM O EXPERIMENTO:
    # 0.0788 = COMPRIMENTO DO PÊNDULO (m)
    # 68 = DISTÂNCIA EM PIXELS ENTRE PONTOS DE REFERÊNCIA NO VÍDEO
    x_metros = -0.0788 * ((x + w/2) - 0.5 * 0.025) / 68


    writer.writerow([t, x_metros])


    # MOSTRA O FRAME
    cv2.imshow('Object Tracking', frame)


    # TECLA ESC (27) PARA PARAR
    if cv2.waitKey(1) & 0xFF == 27:
        break


# FINALIZA
data.close()
source.release()
cv2.destroyAllWindows()


print("✅ Rastreamento concluído e dados salvos em dados.csv")


