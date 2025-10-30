import psutil as p,datetime, time, os
from captura import cpu, disco, ram, rede
from conexao import mysql

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