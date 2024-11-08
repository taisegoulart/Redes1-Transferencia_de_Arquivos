# Redes1-Transferencia_de_Arquivos
Programa simples demonstrando transferência de arquivos entre Cliente e Servidor.
Esse programa pode ser executado numa IDE como o Visual Studio (desde que se tenha permissão de administrador) ou em clientes e servidores de máquinas virtuais.

## Execute o Servidor
1. No Visual Studio, clique com o botão direito na pasta Server e peça para abrir no terminal integrado.
2. No terminal, digite `python3 server.py`para iniciar a execução do servidor.
3. O console deve exibir a mensagem "Servidor pronto e aguardando conexão...", indicando que o servidor está pronto para receber conexões.

## Execute o Cliente
1. No Visual Studio, clique com o botão direito na pasta Server e peça para abrir no terminal integrado.
2. No terminal, digite `python3 client.py`para iniciar a execução do cliente.

O cliente agora solicitará comandos para você. Digite qualquer comando, como `ls`, `mkdir`, `upload nome_do_arquivo, etc.`, e veja a resposta do servidor.

### Lista de comandos
* Comando `ls`: exibe a lista de arquivos e diretórios no servidor.
* Comando `mkdir nome_da_pasta`: cria uma nova pasta no servidor.
* Comando `upload nome_do_arquivo`: envie um arquivo do cliente para o servidor.
* Comando `download nome_do_arquivo`: faça o download de um arquivo do servidor para o cliente.
* Comando `cd nome_da_pasta` para alterar a pasta no servidor.
* Comando `rm nome_do_arquivo` para remover um arquivo específico no servidor.
* Comando `exit`: encerra a conexão com o servidor.

### Explicação sobre o código
Link com a apresentação. [https://docs.google.com/presentation/d/1gWXakD4N4FPU1M_gxVxiBeQnFTFRNKR96y-ipVkAdrU/edit?usp=sharing]
#### Servidor:
Este código implementa um servidor de transferência de arquivos usando sockets. O servidor aceita conexões de clientes, que podem enviar comandos para realizar operações como alterar diretórios, criar pastas, enviar e receber arquivos, listar arquivos no diretório e excluir arquivos. 
- import socket: importa a biblioteca socket, usada para a comunicação em rede entre o servidor e o cliente.
- import os: importa a biblioteca os, que fornece funções para manipulação de arquivos e diretórios do sistema.
- A função handle_client lida com a conexão do cliente e executa comandos recebidos.
- command = conn.recv(1024).decode(): recebe uma mensagem do cliente de até 1024 bytes, decodifica-a de bytes para string, e armazena em command.

##### Comando cd (alteração de diretório)
        `if command.startswith("cd"):
            _, path = command.split()`
            
- Verifica se o comando recebido começa com cd, indicando uma solicitação de alteração de diretório.
- Divide command em duas partes: o comando (cd) e o path (caminho para o diretório desejado).
            `try:
                os.chdir(path)
                conn.send("Diretório alterado com sucesso.".encode())
            except Exception as e:
                conn.send(f"Erro: {str(e)}".encode())`
- Tenta alterar o diretório atual para o path especificado usando os.chdir(path).
- Se a operação for bem-sucedida, envia uma mensagem de confirmação ao cliente.

##### Comando mkdir (criação de pasta)
`
        elif command.startswith("mkdir"):
            _, folder_name = command.split()`

- Verifica se o comando é mkdir, indicando uma solicitação para criar um novo diretório.
- Divide command em duas partes: mkdir e o folder_name (nome da pasta a ser criada).
python
`            try:
                os.makedirs(folder_name, exist_ok=True)
                conn.send("Pasta criada com sucesso.".encode())
            except Exception as e:
                conn.send(f"Erro: {str(e)}".encode())`
- Tenta criar a pasta usando os.makedirs(folder_name, exist_ok=True).
- Se bem-sucedido, envia uma mensagem de confirmação ao cliente.
- Caso haja erro (por exemplo, permissões insuficientes), envia uma mensagem de erro ao cliente.

##### Comando upload (envio de arquivo)
`
        elif command.startswith("upload"):
            _, filename = command.split()`
- Verifica se o comando é upload, indicando uma solicitação para enviar um arquivo.
- Extrai o filename (nome do arquivo a ser criado no servidor).
`
            with open(filename, "wb") as f:
                data = conn.recv(1024)
                while data:
                    f.write(data)
                    data = conn.recv(1024)
            conn.send("Arquivo enviado com sucesso.".encode())`
- Abre o arquivo especificado em modo binário de escrita ("wb").
- Recebe dados em pedaços de até 1024 bytes e os grava no arquivo até que não haja mais dados para receber.
- Após finalizar a gravação, envia uma mensagem ao cliente confirmando o sucesso da operação.

##### Comando download (download de arquivo)
`
        elif command.startswith("download"):
            _, filename = command.split()`
- Verifica se o comando é download, indicando uma solicitação para baixar um arquivo.
- Extrai filename, o nome do arquivo a ser enviado ao cliente.
`
            if os.path.isfile(filename):
                with open(filename, "rb") as f:
                    data = f.read(1024)
                    while data:
                        conn.send(data)
                        data = f.read(1024)
                conn.send("EOF".encode())
            else:
                conn.send("Erro: Arquivo não encontrado.".encode())`
- Verifica se o arquivo existe com os.path.isfile(filename).
- Abre o arquivo em modo de leitura binária ("rb") e envia o conteúdo em pedaços de até 1024 bytes.
- Ao finalizar o envio, envia o marcador EOF para indicar que o arquivo terminou.
- Se o arquivo não for encontrado, envia uma mensagem de erro.
  
##### Comando ls (listar diretório)
`
        elif command == "ls":
            files = "; ".join(os.listdir("."))
            conn.send(files.encode())`
- Verifica se o comando é ls, que lista os arquivos no diretório atual do servidor.
- Usa os.listdir(".") para listar todos os arquivos e pastas no diretório.
- Concatena os nomes com ; e envia o resultado para o cliente.

##### Comando rm (remover arquivo)
`
        elif command.startswith("rm"):
            _, filename = command.split()`
- Verifica se o comando é rm, indicando uma solicitação para excluir um arquivo.
- Extrai filename, o nome do arquivo a ser removido.
`
            try:
                os.remove(filename)
                conn.send("Arquivo removido com sucesso.".encode())
            except Exception as e:
                conn.send(f"Erro: {str(e)}".encode())`
- Tenta remover o arquivo com os.remove(filename).
- Envia uma mensagem de sucesso se a operação for concluída, ou uma mensagem de erro em caso de falha.

##### Comando exit (encerrar conexão)
`
        elif command == "exit":
            conn.send("Conexão encerrada.".encode())
            break`
- Verifica se o comando é exit, indicando que o cliente deseja encerrar a conexão.
- Envia uma mensagem de confirmação ao cliente e interrompe o loop while, encerrando a função.
`
    conn.close()`
- Fecha a conexão com o cliente após o término do loop.
##### Função start_server
A função start_server configura o servidor e aguarda conexões de clientes.

`
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
- Define a função start_server.
- Cria um socket TCP/IP (stream) com socket.AF_INET (IPv4).

    server.bind(("0.0.0.0", 5000))
    server.listen(5)
    print("Servidor pronto e aguardando conexão...")
Associa o socket a todos os IPs locais (0.0.0.0) e à porta 5000.
Configura o servidor para aceitar até 5 conexões pendentes com server.listen(5).
python
Copiar código
    while True:
        conn, addr = server.accept()
        print(f"Conexão recebida de {addr}")
        handle_client(conn)
Entra em um loop que aceita novas conexões.
Quando um cliente se conecta, server.accept() retorna um novo socket conn e o endereço addr do cliente.
Inicia a função handle_client(conn) para processar comandos do cliente.
Código Principal
python
Copiar código
if __name__ == "__main__":
    start_server()
Verifica se o script está sendo executado diretamente (não importado).
Se for o caso, chama start_server() para iniciar o servidor.

Função send_command
A função send_command é usada para enviar um comando para o servidor e aguardar a resposta.

python
Copiar código
def send_command(command, conn):
    conn.send(command.encode())
    response = conn.recv(1024).decode()
    print("Resposta do servidor:", response)
def send_command(command, conn): define uma função chamada send_command que recebe dois parâmetros: command (o comando a ser enviado ao servidor) e conn (o objeto de conexão com o servidor).

conn.send(command.encode()): envia o comando para o servidor. O comando é codificado de string para bytes, pois o protocolo de rede trabalha com dados binários.

response = conn.recv(1024).decode(): recebe a resposta do servidor, que é limitada a 1024 bytes. A resposta é então decodificada de bytes para string.

print("Resposta do servidor:", response): exibe a resposta recebida do servidor no console.

Função start_client
A função start_client é responsável por iniciar o cliente, conectar-se ao servidor e interagir com o usuário, enviando comandos para o servidor conforme o usuário os digita.

python
Copiar código
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 5000))
def start_client(): define a função start_client, que irá configurar o cliente, estabelecer a conexão com o servidor e interagir com o usuário.

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM): cria um novo objeto socket do tipo TCP/IP. socket.AF_INET indica que a comunicação será feita usando o protocolo IPv4, e socket.SOCK_STREAM indica que o tipo de socket será TCP.

client.connect(("127.0.0.1", 5000)): conecta o cliente ao servidor. Neste caso, o servidor está executando na máquina local (127.0.0.1) na porta 5000.

python
Copiar código
    while True:
        command = input("Digite o comando: ")
while True: inicia um loop infinito que continuará até que o usuário decida encerrar a conexão.

command = input("Digite o comando: "): solicita que o usuário insira um comando. O comando é armazenado na variável command.

Comando exit
python
Copiar código
        if command == "exit":
            send_command(command, client)
            break
if command == "exit": verifica se o comando digitado pelo usuário é exit, indicando que o cliente deseja encerrar a conexão.

send_command(command, client): chama a função send_command para enviar o comando exit ao servidor. Isso é importante para notificar o servidor de que a conexão deve ser encerrada.

break: quebra o loop while True, encerrando a execução da função e fechando a conexão com o servidor.

Comando upload (envio de arquivo)
python
Copiar código
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
elif command.startswith("upload"): verifica se o comando começa com a palavra upload, indicando que o usuário deseja enviar um arquivo para o servidor.

_, filename = command.split(): divide o comando em duas partes. O primeiro item (upload) é descartado com _, e o segundo item é o filename, que é o nome do arquivo que será enviado.

with open(filename, "rb") as f: tenta abrir o arquivo especificado pelo usuário em modo de leitura binária ("rb"). Se o arquivo não for encontrado ou ocorrer algum erro, o código irá capturar a exceção.

client.send(f"upload {filename}".encode()): envia uma mensagem ao servidor informando que o comando upload foi executado, seguido do nome do arquivo a ser enviado.

data = f.read(1024): lê até 1024 bytes do arquivo e armazena na variável data.

while data: enquanto houver dados no arquivo para enviar, envia os dados em pacotes de 1024 bytes com client.send(data).

data = f.read(1024): lê o próximo pedaço de dados do arquivo.

client.send(b""): envia um pacote vazio para indicar o final do arquivo.

print("Arquivo enviado com sucesso."): exibe uma mensagem confirmando que o arquivo foi enviado corretamente.

except Exception as e: caso ocorra algum erro durante o envio do arquivo (como o arquivo não existir ou problemas de rede), a exceção é capturada e uma mensagem de erro é exibida.

Comando download (download de arquivo)
python
Copiar código
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
elif command.startswith("download"): verifica se o comando começa com download, indicando que o usuário deseja baixar um arquivo do servidor.

_, filename = command.split(): divide o comando e obtém o nome do arquivo que o usuário deseja baixar.

client.send(f"download {filename}".encode()): envia ao servidor a mensagem download {filename} para solicitar o arquivo.

with open(f"downloaded_{filename}", "wb") as f: abre um novo arquivo local, com o prefixo downloaded_, para salvar o arquivo baixado.

while True: inicia um loop para continuar recebendo os dados do servidor até que o arquivo esteja completo.

data = client.recv(1024): recebe até 1024 bytes de dados do servidor.

if data == b"EOF": verifica se os dados recebidos são a marcação EOF, que indica o final do arquivo.

break: interrompe o loop se a marcação EOF for recebida, indicando que o arquivo foi completamente transferido.

f.write(data): escreve os dados recebidos no arquivo local.

print("Arquivo baixado com sucesso."): exibe uma mensagem de sucesso após o download do arquivo.

Comandos gerais
python
Copiar código
        else:
            send_command(command, client)
else: para qualquer comando que não seja exit, upload ou download, o comando é enviado diretamente ao servidor utilizando a função send_command.
Fechamento da Conexão
python
Copiar código
    client.close()
client.close(): fecha a conexão com o servidor após o término da comunicação.
Código Principal
python
Copiar código
if __name__ == "__main__":
    start_client()
if name == "main": verifica se o script está sendo executado diretamente (não importado).

start_client(): chama a função start_client para iniciar o cliente, conectar-se ao servidor e permitir a interação com o usuário.



