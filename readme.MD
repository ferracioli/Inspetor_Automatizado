<!-- Para abrir o markdown: control + shift + v -->
Este código acessa modelos de LLM disponíveis no Open Router, e deixa o agente sendo executado em uma janela separada. A cada X segundos(definido em 300 como padrão), ele verifica novos códigos no repositório apresentado no config.py, indicando sugestões de melhorias relacionadas a segurança, legibilidade e documentação.Etapas:

1) No primeiro acesso, instale as bibliotecas necessárias
`pip install -r requirements.txt`

2) Caso os parâmetros estejam em config.py:
`python main.py`

3) Selecione "iniciar monitoramento" e deixe ele agindo de maneira passiva

4) Caso queira, é possível passar os parâmetros manualmente:
`python main.py --repo /caminho/para/repositorio --interval 300`