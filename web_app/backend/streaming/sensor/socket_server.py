import socket
import sys
import time

if len(sys.argv) < 4:
    print("WARN: Es necesario poner dos agumentos: <IP> <Port> <Centre>")
    sys.exit(0)

s = socket.socket()

s.bind((str(sys.argv[1]), int(sys.argv[2])))
s.listen(10)  # Accepts up to 10 connections.

print("Esperando conexión con cliente...")

while True:
    sc, address = s.accept()

    print("----------Conectado----------")
    print(address)
    print("------------------------------")

    filepath = '/tmp/datasets/sensor/' + sys.argv[3] + '/2018_input_sensor_stream.csv'
    
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            time.sleep(1.5)
            sc.send((line.strip() + "\n\r").encode())
            print("Line {}: {}".format(cnt, line.strip()))
            line = fp.readline()
            cnt += 1

    sc.close()
