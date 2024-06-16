import csv
import paramiko
import secrets
import string

def gerar_senha_aleatoria(tamanho=12):
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(tamanho))

contas = ["xxx", "xxx", "xxxx", "xxxxx", "xxxx", "xxxxxxxx"]


linhas_atualizadas = []


with open('credenciais.csv', mode='r') as arquivo:
    leitor_csv = csv.DictReader(arquivo)
    linhas = list(leitor_csv)


for linha in linhas:
    hostname = linha['hostname']
    username = linha['username']
    password = linha['password']
    linha_atualizada = linha.copy() 

    client_ssh = paramiko.SSHClient()
    client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client_ssh.connect(hostname=hostname, port=22, username=username, password=password)
        linha_atualizada['status'] = 'OK'


        stdin, stdout, stderr = client_ssh.exec_command("grep 'xxxx' /etc/group")
        if stdout.channel.recv_exit_status() == 1:
            stdin, stdout, stderr = client_ssh.exec_command("groupadd xxxx && echo -e '#xxxxx\n%xxx ALL=(ALL) NOPASSWD:ALL' | tee -a /etc/sudoers")
            if stdout.channel.recv_exit_status() != 0:
                linha_atualizada['status'] = 'Erro ao criar grupo xxx'


        stdin, stdout, stderr = client_ssh.exec_command("grep 'xxxxx' /etc/group")
        if stdout.channel.recv_exit_status() == 1:
            stdin, stdout, stderr = client_ssh.exec_command("groupadd xxxx")
            if stdout.channel.recv_exit_status() != 0:
                linha_atualizada['status'] = 'Erro ao criar grupo xxxxx'


        with open('usuarios_criados.csv', mode='a', newline='') as arquivo_usuarios:
            escritor_usuarios_csv = csv.DictWriter(arquivo_usuarios, fieldnames=['ip', 'usuario', 'senha'])


            for conta in contas:
                stdin, stdout, stderr = client_ssh.exec_command(f"grep {conta} /etc/passwd")
                if stdout.channel.recv_exit_status() == 1:
                    senha = gerar_senha_aleatoria()
                    if conta == "xxxx":
                        stdin, stdout, stderr = client_ssh.exec_command(f"useradd -m {conta} -p $(echo '{senha}' | openssl passwd -1 -stdin) -G xxxx -s /bin/bash")
                    else:
                        stdin, stdout, stderr = client_ssh.exec_command(f"useradd -m {conta} -p $(echo '{senha}' | openssl passwd -1 -stdin) -G xxxx -s /bin/bash")
                    
                    if stdout.channel.recv_exit_status() == 0:
                        linha_atualizada['status'] = 'OK'
                        linhas_atualizadas.append(linha_atualizada)
                        escritor_usuarios_csv.writerow({'ip': hostname, 'usuario': conta, 'senha': senha})

                else:
                    senha = gerar_senha_aleatoria()
                    if conta == "xxxxx":
                        stdin, stdout, stderr = client_ssh.exec_command(f"echo -e '{senha}\n{senha}' | passwd {conta} && usermod -a -G xxxx {conta}")
                    else:
                        stdin, stdout, stderr = client_ssh.exec_command(f"echo -e '{senha}\n{senha}' | passwd {conta} && usermod -a -G xxxxx {conta}")
                    
                    escritor_usuarios_csv.writerow({'ip': hostname, 'usuario': conta, 'senha': senha})

    except Exception as e:
        print(f"Erro ao conectar na máquina {hostname}: {e}")
        linha_atualizada['status'] = 'Erro ao conectar na máquina'

    finally:
        client_ssh.close()
        linhas_atualizadas.append(linha_atualizada)


with open('credenciais.csv', mode='w', newline='') as arquivo:
    nomes_campos = ['hostname', 'username', 'password', 'status']
    escritor_csv = csv.DictWriter(arquivo, fieldnames=nomes_campos)
    escritor_csv.writeheader()
    escritor_csv.writerows(linhas_atualizadas)
