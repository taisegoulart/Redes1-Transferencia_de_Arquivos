import socket
import os

def handle_client(conn):
    while True:
        command = conn.recv(1024).decode()
        
        if command.startswith("cd"):
            _, path = command.split()
            try:
                os.chdir(path)
                conn.send("Diretório alterado com sucesso.".encode())
            except Exception as e:
                conn.send(f"Erro: {str(e)}".encode())
        
        elif command.startswith("mkdir"):
            _, folder_name = command.split()
            try:
                os.makedirs(folder_name, exist_ok=True)
                conn.send("Pasta criada com sucesso.".encode())
            except Exception as e:
                conn.send(f"Erro: {str(e)}".encode())
        
        elif command.startswith("upload"):
            _, filename = command.split()
            with open(filename, "wb") as f:
                data = conn.recv(1024)
                while data:
                    f.write(data)
                    data = conn.recv(1024)
            conn.send("Arquivo enviado com sucesso.".encode())
        
        elif command.startswith("download"):
            _, filename = command.split()
            if os.path.isfile(filename):
                with open(filename, "rb") as f:
                    data = f.read(1024)
                    while data:
                        conn.send(data)
                        data = f.read(1024)
                conn.send("EOF".encode())
            else:
                conn.send("Erro: Arquivo não encontrado.".encode())
        
        elif command == "ls":
            files = "; ".join(os.listdir("."))
            conn.send(files.encode())
        
        elif command.startswith("rm"):
            _, filename = command.split()
            try:
                os.remove(filename)
                conn.send("Arquivo removido com sucesso.".encode())
            except Exception as e:
                conn.send(f"Erro: {str(e)}".encode())
        
        elif command == "exit":
            conn.send("Conexão encerrada.".encode())
            break

    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))
    server.listen(5)
    print("Servidor pronto e aguardando conexão...")

    while True:
        conn, addr = server.accept()
        print(f"Conexão recebida de {addr}")
        handle_client(conn)

if __name__ == "__main__":
    start_server()