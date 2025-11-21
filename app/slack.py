import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from conexao import mysql


load_dotenv()

client = WebClient(token=os.environ['TOKEN_SLACK'])
def enviar_alerta(texto):
    try:
        client.chat_postMessage(channel='#Infrawatch', text=texto, mrkdwn=True)
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Erro: {e.response['error']}")
        assert isinstance(e.response.status_code, int)
        print(f"Código de status de resposta: {e.response.status_code}")


def buscar_parametros():
    query = """
        select 	parametro.fkRecurso, parametro.valor, parametro.nivel, maquina.apelido, recurso_monitorado.descricao, registro_coleta.leitura
        from parametro
        join maquina on parametro.fkMaquina = maquina.idMaquina
        left join recurso_monitorado on parametro.fkRecurso = recurso_monitorado.idRecurso
        join registro_coleta on registro_coleta.fkRecurso = parametro.fkRecurso and registro_coleta.fkMaquina = parametro.fkMaquina and registro_coleta.fkEmpresa = parametro.fkEmpresa
        where registro_coleta.data_hora = (select max(data_hora) from registro_coleta where fkRecurso = registro_coleta.fkRecurso and fkMaquina = registro_coleta.fkMaquina and fkEmpresa = registro_coleta.fkEmpresa);
    """
    try:
        resultados = mysql.executar(query)
        print(f"{resultados}")
        if not resultados:
            return[]
        return resultados
    except Exception as e:
        print(f"Erro ao buscar parâmetros {e}")
        return[]

def verificar_parametro(parametros, dados_maquina):
    print(f"{parametros}")
    if not parametros:
        print("Parâmetros não encontrados")
        return
    alertas = []
    for parametro in parametros:
        fkRecurso = parametro[0]
        valor_parametro = parametro[1]
        nivel_parametro = parametro[2]
        apelido_maquina = parametro[3]
        descricao_recurso = parametro[4]
        valor_coletado = parametro[5]

        valor_coletado = dados_maquina.get(str(fkRecurso), 0.0)

        try:
            valor_parametro = float(valor_parametro)
            valor_coletado = float(valor_coletado)
        except ValueError:
            print(f"Valor do parâmetro '{descricao_recurso}' não pode ser convertido para float: {valor_parametro}")
            continue

        print(f"Parâmetro analisado {descricao_recurso}, valor {valor_coletado}, limite {valor_parametro}")
        if valor_coletado >= valor_parametro:
            if nivel_parametro == 1:
                alerta = f"""🔴   ALERTA CRÍTICO em *{apelido_maquina}*: 
                O recurso *{descricao_recurso}* ultrapassou o limite de criticidade 
                Valor capturado: {valor_coletado} 
                Limite criticidade: {valor_parametro}"""
                alertas.append(alerta)
            elif nivel_parametro == 2:
                alerta = f"""🟡   ALERTA em *{apelido_maquina}*: 
                O recurso *{descricao_recurso}* ultrapassou o limite de atenção 
                Valor capturado: {valor_coletado} 
                Limite atenção: {valor_parametro})"""

    if alertas:
        for alerta in alertas:
            enviar_alerta(alerta)
            print("Alertas enviados para o Slack!")
    else:
        print("Nenhum alerta gerado.")


