import csv
import paramiko
import secrets
import string
import requests
import ipaddress
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
 
def banner():
    print("""

██╗   ██╗███████╗███████╗██████╗     ███████╗ █████╗  ██████╗████████╗ ██████╗ ██████╗ ██╗   ██╗
██║   ██║██╔════╝██╔════╝██╔══██╗    ██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝
██║   ██║███████╗█████╗  ██████╔╝    █████╗  ███████║██║        ██║   ██║   ██║██████╔╝ ╚████╔╝ 
██║   ██║╚════██║██╔══╝  ██╔══██╗    ██╔══╝  ██╔══██║██║        ██║   ██║   ██║██╔══██╗  ╚██╔╝  
╚██████╔╝███████║███████╗██║  ██║    ██║     ██║  ██║╚██████╗   ██║   ╚██████╔╝██║  ██║   ██║   
 ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
                                                                                                
                                                        ██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗  
                                                        ██║     ██║████╗  ██║██║   ██║╚██╗██╔╝  
                                                        ██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝   
                                                        ██║     ██║██║╚██╗██║██║   ██║ ██╔██╗   
                                                        ███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗  
                                                        ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝  
                                                                                                                                                                                    
                                                                            By Afonso Carvalho
                                                                            V 1.0                                                                                               
""")
    print("1- Criação Kit de contas em UMA máquina especifica\n"
          "2- Criação Kit de contas em DIVERSAS máquinas\n")

def menu_interativo():
    opcao = None
    while True:
        try:
            os.system('cls' if os.name=='nt' else 'clear')
            banner()
            opcao = int(input("Escolha umas das ações acima: "))
            if opcao < 1 or opcao > 2:
                raise ValueError()
            break
        except ValueError:
            print("Entrada inválida. Pressione Enter para continuar...")
            input()
    return opcao


def obter_credenciais_por_api(ip):
    try:
        print(f"Buscando credenciais para o IP {ip} no CyberArk...")
        response = requests.get(f"https://sua.api/credenciais?ip={ip}")
        if response.status_code == 200:
            data = response.json()
            return {"hostname": ip, "username": data['UserName'], "password": data['Content']}
        else:
            print("Erro ao buscar credenciais na API.")
            return None
    except Exception as e:
        print(f"Erro de conexão com API: {e}")
        return None

def obter_credenciais_manual(ip):
    usuario = input(f"Usuário SSH para {ip}: ")
    senha = input(f"Senha SSH para {ip}: ")
    return {"hostname": ip, "username": usuario, "password": senha}

def montar_lista_credenciais(opcao):
    lista_credenciais = []

    if opcao == 1:
        while True:
            ip = input("Digite o IP da máquina: ").strip()
            try:
                ipaddress.ip_address(ip)
                break
            except ValueError:
                print("IP inválido. Tente novamente.\n")

        modo = input("Você quer informar usuário e senha manualmente? (Y/N): ").lower()

        if modo == 'y':
            cred = obter_credenciais_manual(ip) 
        else:
            cred = obter_credenciais_por_api(ip)

        if cred:
            lista_credenciais.append(cred)

    elif opcao == 2:
        while True:
            entrada = input("Digite os IPs separados por vírgula: ")
            ip_list = []

            for ip in entrada.split(','):
                ip_list.append(ip.strip())

            try:
                for ip in ip_list:
                 ipaddress.ip_address(ip)  
                break 
            except ValueError as e:
                print(f"IP inválido encontrado: {e}. Tente novamente.\n")

        modo = input("Você quer informar usuário e senha manualmente? (Y/N): ").lower()

        for ip in ip_list:
            if modo == 'y':
                cred = obter_credenciais_manual(ip) 
            else :
                cred = obter_credenciais_por_api(ip)

            if cred:
                lista_credenciais.append(cred)

    return lista_credenciais

def gerar_senha_aleatoria(tamanho=12):
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(tamanho))

### ----------------------------------------------------------------------

def main():
    opcao = menu_interativo()
    credenciais = montar_lista_credenciais(opcao)

    while True:
        contas_input = input("Digite os nomes das contas que deseja criar, separadas por vírgula. Para usar as contas padrão, pressione ENTER: ")

        if not contas_input.strip():
            contas = ["conta1", "conta4", "conta2"]
        else:
            contas = []
            for conta in contas_input.split(","):
                conta = conta.strip()
                if conta:
                    contas.append(conta)

        print(f"\nVocê deseja criar as seguintes contas: {', '.join(contas)}")
        confirmacao = input("Confirmar? (Y/N): ").strip().lower()

        if confirmacao == 'y':
            break
        else:
            print("Vamos tentar de novo...\n")


    linhas_atualizadas = []

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

            comando_sudoers = 'echo -e "#Usuario" | sudo tee -a /etc/sudoers.d/datacenter'
            stdin, stdout, stderr = client_ssh.exec_command(comando_sudoers)
            if stdout.channel.recv_exit_status() != 0:
                raise Exception(f"Falha ao atualizar sudoers: {stderr.read().decode().strip()}")

            with open('usuarios_criados.csv', mode='a', newline='') as arquivo_usuarios:
                escritor_usuarios_csv = csv.DictWriter(arquivo_usuarios, fieldnames=['ip', 'usuario', 'senha'])

                for conta in contas:
                    stdin, stdout, stderr = client_ssh.exec_command(f"grep {conta} /etc/passwd")
                    if stdout.channel.recv_exit_status() == 1:  # Usuário não existe
                        senha = gerar_senha_aleatoria()
                        if conta != "conta2":
                            client_ssh.exec_command(f'echo -e "\n{conta} ALL=(ALL) NOPASSWD:ALL" | sudo tee -a /etc/sudoers.d/datacenter')
                        stdin, stdout, stderr = client_ssh.exec_command(f"sudo useradd -m -p $(openssl passwd -1 {senha}) -s /bin/bash {conta}")

                        if stdout.channel.recv_exit_status() == 0:
                            escritor_usuarios_csv.writerow({'ip': hostname, 'usuario': conta, 'senha': senha})
                        else:
                            raise Exception(f"Falha ao criar usuário {conta}: {stderr.read().decode().strip()}")
                    else:
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

    with open('credenciais.csv', mode='w', newline='') as arquivo:
        nomes_campos = ['hostname', 'username', 'password', 'status']
        escritor_csv = csv.DictWriter(arquivo, fieldnames=nomes_campos)
        escritor_csv.writeheader()
        escritor_csv.writerows(linhas_atualizadas)

if __name__ == "__main__":
    main()
