import csv
import paramiko

contas = ["teste2", "teste3", "teste4"]

with open('credenciais.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    rows = list(csv_reader)

with open('credenciais.csv', mode='w', newline='') as file:
    fieldnames = ['hostname', 'username', 'password', 'status']
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)

    csv_writer.writeheader()

    for row in rows:
        hostname = row['hostname']
        username = row['username']
        password = row['password']

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh_client.connect(hostname=hostname, port=22, username=username, password=password)
            row['status'] = 'OK'

            for conta in contas:
                stdin, stdout, stderr = ssh_client.exec_command(f"cat /etc/passwd | grep {conta} ")

                if stdout.channel.recv_exit_status() == 1:
                    stdin, stdout, stderr = ssh_client.exec_command(f"useradd -m {conta} -p foda2")

                    if stdout.channel.recv_exit_status() == 0:
                        row['status'] = 'OK'
                    else:
                        row['status'] = 'Erro ao criar usuário'

        except Exception as e:
            print(f"Erro ao conectar na máquina {hostname}: {e}")
            row['status'] = 'Erro ao conectar na máquina'

        finally:
            ssh_client.close()

        csv_writer.writerow(row)
