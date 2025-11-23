import psutil as p,datetime, time, os
from captura import cpu, disco, ram, rede
from conexao import mysql
import slack

mapeamento_alertas = {
    '1001': 'acima',  
    '1002': 'abaixo', 
    '1003': 'acima',  
    '1004': 'acima',  
    '1005': 'abaixo', 
    '1006': 'acima',  
    '1007': 'abaixo',  
    '1008': 'abaixo', 
    '1009': 'acima',  
    '1010': 'acima',  
}

print("Iniciando...")
time.sleep(2)

mac_address = rede.mac_address()

while True:
    if p.LINUX :
        os.system('clear')

    if p.WINDOWS :
        os.system('cls')
    
    data_hora = datetime.datetime.now()

    cpu_uso_porcentagem = cpu.porcentagem()
    cpu_freq_mhz = cpu.frequencia()
    cpu_temp_c = cpu.temperatura()

    ram_uso_porcentagem = ram.porcentagem()
    ram_uso_gb = ram.gigabytes()

    disco_uso_porcentagem = disco.porcentagem()
    disco_velocidade_mbps = disco.velocidade()
    disco_velocidade_escrita = disco_velocidade_mbps["escrita"]
    disco_velocidade_leitura = disco_velocidade_mbps["leitura"]

    transferencia_kbps = rede.transferencia()
    transferencia_entrada_kbps = transferencia_kbps["entrada"]
    transferencia_saida_kbps = transferencia_kbps["saida"]

    dados_maquina = {
        '1001': cpu_uso_porcentagem,
        '1002': cpu_freq_mhz,
        '1003': cpu_temp_c,
        '1004': ram_uso_porcentagem,
        '1005': ram_uso_gb,
        '1006': disco_uso_porcentagem,
        '1007': disco_velocidade_escrita,
        '1008': disco_velocidade_leitura,
        '1009': transferencia_entrada_kbps,
        '1010': transferencia_saida_kbps
    }

    parametros = slack.buscar_parametros()

    slack.verificar_parametro(parametros, dados_maquina, mapeamento_alertas)
    
    str_dados = f"'{mac_address.replace("-", "").replace(":", "")}', {cpu_uso_porcentagem}, {cpu_freq_mhz}, {cpu_temp_c}, {ram_uso_porcentagem}, {ram_uso_gb}, {disco_uso_porcentagem}, {disco_velocidade_escrita}, {disco_velocidade_leitura}, {transferencia_entrada_kbps}, {transferencia_saida_kbps}, '{data_hora}'"

    query = f"CALL inserir_captura_python({str_dados})"

    # if (True):
    if (mysql.executar(query)):
        print(f"""
            Executado: {query}

            Dados inseridos com sucesso!
              ↳ Mac Address: {mac_address}
              ↳ Uso de CPU %: {cpu_uso_porcentagem}
              ↳ Frequência de CPU: {cpu_freq_mhz}
              ↳ Temperatura de CPU: {cpu_temp_c}
              ↳ Uso de RAM %: {ram_uso_porcentagem}
              ↳ Uso de RAM GB: {ram_uso_gb  }
              ↳ Uso de Disco %: {disco_uso_porcentagem}
              ↳ Velocidade de Escrita de Disco: {disco_velocidade_escrita}
              ↳ Velocidade de Leitura de Disco: {disco_velocidade_leitura}
              ↳ Entrada de Dados pela Rede kbps: {transferencia_entrada_kbps}
              ↳ Saida de Dados pela Rede kbps: {transferencia_saida_kbps}
              ↳ Horário da Coleta: {data_hora}
        """)
    else:
        "Erro na inserção de dados no banco"
    time.sleep(2)