<h1 align="center"> SSH User Management Automation </h1>

![Badge Concluído](https://img.shields.io/static/v1?label=Status&message=Concluído&color=success&style=for-the-badge)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Paramiko](https://img.shields.io/badge/Paramiko-2C2D72?style=for-the-badge&logo=python&logoColor=white)

## :book: Resumo do projeto
Este script Python utiliza a biblioteca Paramiko para estabelecer conexões SSH seguras com uma lista de servidores e gerenciar os usuários.

## :toolbox: Tecnologias e ferramentas

- Python
- Paramiko

## :computer: Como usar

1. Instale a biblioteca Paramiko usando o pip:

```bash
pip install paramiko
```
2. Preencha o arquivo 'credenciais.csv' com as informações dos servidores (hostname, username, password).
3. Execute o script Python.

## :bulb: Funcionalidades

O script realiza as seguintes ações:

- Lê as informações dos servidores do arquivo 'credenciais.csv'.
- Estabelece uma conexão SSH com cada servidor.
- Verifica se os usuários da lista estão presentes nos servidores.
- Se um usuário não estiver presente, cria o usuário.
- Salva o status de cada operação (conexão, criação de usuário) no arquivo 'credenciais.csv'.
