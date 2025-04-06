import socket
from typing import NoReturn

def run_tcp_server() -> NoReturn:
    HOST = 'localhost'  # Слушаем все интерфейсы: '' 
    PORT = 5140
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"TCP Server listening on {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(1024)
                if data:
                    print(f"Received TCP: {data.decode('utf-8')}")


def run_udp_server() -> NoReturn:
    HOST = 'localhost'
    PORT = 5140
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"UDP Server listening on {HOST}:{PORT}")
        
        while True:
            data, addr = s.recvfrom(1024)
            print(f"Received UDP from {addr}: {data.decode('utf-8')}")


if __name__ == "__main__":
    run_tcp_server()