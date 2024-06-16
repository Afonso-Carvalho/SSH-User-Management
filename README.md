<h1 align="center">SSH User Management Automation</h1>

![Badge Concluído](https://img.shields.io/static/v1?label=Status&message=Concluído&color=success&style=for-the-badge)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Paramiko](https://img.shields.io/badge/Paramiko-2C2D72?style=for-the-badge&logo=python&logoColor=white)

## :book: Resumo do projeto

Este script Python utiliza a biblioteca Paramiko para estabelecer conexões SSH seguras com uma lista de servidores e gerenciar usuários de maneira automatizada.

## :toolbox: Tecnologias e ferramentas

- Python
- Paramiko

## :computer: Como usar

1. Instale a biblioteca Paramiko usando o pip:

    ```bash
    pip install paramiko
    ```

2. Preencha o arquivo `credenciais.csv` com as informações dos servidores no seguinte formato:

    ```csv
    hostname,username,password
    servidor1,usuario1,senha1
    servidor2,usuario2,senha2
    ```

3. Execute o script Python:

    ```bash
    python script.py
    ```

## :bulb: Funcionalidades

O script realiza as seguintes ações:

- Lê as informações dos servidores a partir do arquivo `credenciais.csv`.
- Estabelece uma conexão SSH com cada servidor.
- Verifica se os grupos `xxxx` e `xxxxx` estão presentes nos servidores, criando-os se necessário.
- Verifica se os usuários especificados na lista `contas` estão presentes nos servidores:
    - Se um usuário não estiver presente, cria o usuário com uma senha gerada aleatoriamente.
    - Se um usuário estiver presente, altera a senha do usuário para uma nova senha gerada aleatoriamente.
- Salva as informações dos usuários criados (IP, usuário, senha) no arquivo `usuarios_criados.csv`.
- Atualiza o arquivo `credenciais.csv` com o status de cada operação (conexão, criação de grupo, criação de usuário).

## :scroll: Estrutura dos arquivos

- `script.py`: Script principal que realiza as operações descritas acima.
- `credenciais.csv`: Arquivo de entrada contendo as credenciais dos servidores.
- `usuarios_criados.csv`: Arquivo de saída contendo as informações dos usuários criados ou atualizados.

## :warning: Avisos

- Certifique-se de ter permissões suficientes nos servidores para criar grupos e usuários.
- As senhas geradas aleatoriamente são armazenadas em texto simples no arquivo `usuarios_criados.csv`, então trate este arquivo com cuidado para evitar vazamentos de informações sensíveis.

## :rocket: Futuras melhorias

- Implementar a criptografia das senhas no arquivo `usuarios_criados.csv`.
- Adicionar suporte para diferentes sistemas operacionais além do Linux.
- Implementar uma interface gráfica para facilitar o uso do script.

---

Feito com por [Afonso Carvalho](https://github.com/seu-usuario)
