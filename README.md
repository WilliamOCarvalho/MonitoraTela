# Session Monitor

Este é um script Python que monitora eventos de bloqueio e desbloqueio de sessão no Windows e inicia ou encerra um programa com base nesses eventos.

O programa foi desenvolvido sob a necessidade de não esquecer de ativar ou desativar o programa Microsip (programa para chamadas Voip), ao se ausentar e retornar a base de atendimento(Suporte).

## Requisitos

- Python 3.x
- Bibliotecas `ctypes` e `tkinter`

## Instalação

1. Clone este repositório:

    ```sh
    git clone https://github.com/seuusuario/session-monitor.git
    cd session-monitor
    ```

2. Instale as dependências (se necessário):

    ```sh
    pip install -r requirements.txt
    ```

## Uso

1. Execute o script:

    ```sh
    python session_monitor.py
    ```

2. Selecione o programa que deseja monitorar.

## Funcionamento

- O script verifica se o processo está em execução.
- Inicia ou encerra o programa com base nos eventos de bloqueio e desbloqueio de sessão.

## Funções Principais

- `is_process_running(process_name)`: Verifica se o processo está em execução.
- `start_program(programa, process_name)`: Inicia o programa se não estiver em execução.
- `stop_program(process_name)`: Encerra o programa se estiver em execução.
- `session_change_callback(event_type, programa, process_name)`: Callback para tratar mudanças na sessão.
- `session_change_listener(programa, process_name)`: Monitora eventos de bloqueio e desbloqueio de sessão usando a API Wtsapi32.

## Contribuição

1. Fork este repositório.
2. Crie uma nova branch:

    ```sh
    git checkout -b minha-feature
    ```

3. Faça suas modificações e commit:

    ```sh
    git commit -m 'Minha nova feature'
    ```

4. Envie para o repositório remoto:

    ```sh
    git push origin minha-feature
    ```

5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
