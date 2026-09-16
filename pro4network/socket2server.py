# 서버 서비스는 계속 유지
import socket
import sys

# HOST = '192.168.0.32'   # '127.0.0.1', 'localhost' 
HOST = ''   # 사용 가능한 주소 모두 가능
PORT = 7788
serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    serversock.bind((HOST, PORT))
    serversock.listen(5)
    print('서버(무한 루핑) 서비스 중 ...')

    while True:
        conn, addr = serversock.accept()
        print('client info : ', addr[0], ' ', addr[1])
        print(conn.recv(1024).decode())   # 수신 메세제 출력
        # 메세지 송신 to client
        conn.send(('from server : ' + str(addr[1]) + ' 행운을 빌께').encode('utf_8'))
except Exception as e:
    print('err : ', e)
    sys.exit()
finally:
    conn.close()
    serversock.close()