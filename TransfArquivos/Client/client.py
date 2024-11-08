import socket

def send_command(command, conn):
    conn.send(command.encode())
    response = conn.recv(1024).decode()
    print("Resposta do servidor:", response)

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5000))

    while True:
        command = input("Digite o comando: ")
        if command == "exit":
            send_command(command, client)
            break
        elif command.startswith("upload"):
            _, filename = command.split()
            try:
                with open(filename, "rb") as f:
                    client.send(f"upload {filename}".encode())
                    data = f.read(1024)
                    while data:
                        client.send(data)
                        data = f.read(1024)
                    client.send(b"")
                print("Arquivo enviado com sucesso.")
            except Exception as e:
                print(f"Erro: {e}")
        elif command.startswith("download"):
            _, filename = command.split()
            client.send(f"download {filename}".encode())
            with open(f"downloaded_{filename}", "wb") as f:
                while True:
                    data = client.recv(1024)
                    if data == b"EOF":
                        break
                    f.write(data)
            print("Arquivo baixado com sucesso.")
        else:
            send_command(command, client)

    client.close()

if __name__ == "__main__":
    start_client()
