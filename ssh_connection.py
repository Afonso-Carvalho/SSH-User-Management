import csv
import paramiko
import secrets
import string

def gerar_senha_aleatoria(tamanho=12):
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(tamanho))

# Lista de credenciais no próprio script
credenciais = [
    {"hostname": "xxxx", "username": "xxx", "password": "xxxx"},
    {"hostname": "xxx", "username": "xxxx", "password": "xxxxx"},
]

contas = ["xxx", "xx", "xx", "xx", "xx", "xxxx"]
linhas_atualizadas = []

# Garantir que o arquivo usuarios_criados.csv tenha cabeçalho
with open('usuarios_criados.csv', mode='w', newline='') as arquivo_usuarios:
    escritor_usuarios_csv = csv.DictWriter(arquivo_usuarios, fieldnames=['ip', 'usuario', 'senha'])
    escritor_usuarios_csv.writeheader()

for credencial in credenciais:
    hostname = credencial['hostname']
    username = credencial['username']
    password = credencial['password']
    linha_atualizada = credencial.copy()

    client_ssh = paramiko.SSHClient()
    client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client_ssh.connect(hostname=hostname, port=22, username=username, password=password)
        linha_atualizada['status'] = 'OK'

        # Atualizando o arquivo sudoers
        comando_sudoers = 'echo -e "#Usuario xxxxx" | sudo tee -a /etc/sudoers.d/xxxxxx'
        stdin, stdout, stderr = client_ssh.exec_command(comando_sudoers)
        if stdout.channel.recv_exit_status() != 0:
            raise Exception(f"Falha ao atualizar sudoers: {stderr.read().decode().strip()}")

        with open('usuarios_criados.csv', mode='a', newline='') as arquivo_usuarios:
            escritor_usuarios_csv = csv.DictWriter(arquivo_usuarios, fieldnames=['ip', 'usuario', 'senha'])

            for conta in contas:
                stdin, stdout, stderr = client_ssh.exec_command(f"grep {conta} /etc/passwd")
                if stdout.channel.recv_exit_status() == 1:  # Usuário não existe
                    senha = gerar_senha_aleatoria()
                    if conta != "yyyyy":
                        client_ssh.exec_command(f'echo -e "\n{conta} ALL=(ALL) NOPASSWD:ALL" | sudo tee -a /etc/sudoers.d/xxxxxx')
                    stdin, stdout, stderr = client_ssh.exec_command(f"sudo useradd -m -p $(openssl passwd -1 {senha}) -s /bin/bash {conta}")

                    if stdout.channel.recv_exit_status() == 0:
                        escritor_usuarios_csv.writerow({'ip': hostname, 'usuario': conta, 'senha': senha})
                    else:
                        raise Exception(f"Falha ao criar usuário {conta}: {stderr.read().decode().strip()}")

                else:  # Usuário já existe, redefinir senha
                    senha = gerar_senha_aleatoria()
                    stdin, stdout, stderr = client_ssh.exec_command(f"echo -e '{senha}\n{senha}' | sudo passwd {conta}")
                    if stdout.channel.recv_exit_status() == 0:
                        escritor_usuarios_csv.writerow({'ip': hostname, 'usuario': conta, 'senha': senha})
                    else:
                        raise Exception(f"Falha ao redefinir senha do usuário {conta}: {stderr.read().decode().strip()}")

    except Exception as e:
        print(f"Erro ao conectar ou executar comandos na máquina {hostname}: {e}")
        linha_atualizada['status'] = 'Erro ao conectar ou executar comandos'

    finally:
        client_ssh.close()
        linhas_atualizadas.append(linha_atualizada)

# Salvar status atualizado em credenciais.csv
with open('credenciais.csv', mode='w', newline='') as arquivo:
    nomes_campos = ['hostname', 'username', 'password', 'status']
    escritor_csv = csv.DictWriter(arquivo, fieldnames=nomes_campos)
    escritor_csv.writeheader()
    escritor_csv.writerows(linhas_atualizadas)
