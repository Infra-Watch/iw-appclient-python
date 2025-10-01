import psutil as p
from mysql.connector import connect, Error
from dotenv import load_dotenv
import os

load_dotenv()

config = {
    'user': os.getenv("user"),
    'password': os.getenv("password"),
    'host': os.getenv("host"),
    'database': os.getenv("database"),
    'port': int(os.getenv("port", "3307"))
}

def selecionar_porcentagem_cpu():
    try:
        db = connect(**config)
        if db.is_connected():
            db_info = db.server_info
            print('Connected to MySQL server version -', db_info)
            
            with db.cursor(dictionary=True) as cursor:
                query = "SELECT * FROM infrawatch.componentes;"
                cursor.execute(query)
                resultado = cursor.fetchall() 
                
            cursor.close()
            db.close()
            return resultado
    
    except Error as e:
        print('Error to connect with MySQL -', e) 


def selecionar_timestamp_cpu():
    try:
        db = connect(**config)
        if db.is_connected():
            with db.cursor() as c:
                c.execute("""
                    SELECT lc.data_hora,
                           lc.hostname AS host,
                           m.usuario,
                           lc.porcentagem
                    FROM infrawatch.componentes lc
                    JOIN infrawatch.maquina m ON m.idMaquina = lc.idMaquina
                    ORDER BY lc.data_hora DESC
                """)
                for data_hora, host, usuario, cpu in c.fetchall():
                    print(f"{data_hora} | {host}/{usuario} | CPU {cpu}%")
            db.close()
    except Error as e:
        print("Erro na consulta:", e)


def selecionar_timestamp_memoria():
    try:
        db = connect(**config)
        if db.is_connected():
            with db.cursor() as c:
                c.execute("""
                    SELECT lc.data_hora,
                           lc.hostname AS host,
                           m.usuario,
                           lc.memoria,
                           lc.maquina_cpu
                    FROM infrawatch.componentes lc
                    JOIN infrawatch.maquina m ON m.idMaquina = lc.idMaquina
                    ORDER BY lc.data_hora DESC
                """)
                for data_hora, host, usuario, mem, ram_gb in c.fetchall():
                    print(f"{data_hora} | {host}/{usuario} | MEM {mem}% | RAM {ram_gb} GB")
            db.close()
    except Error as e:
        print("Erro na consulta:", e)


def selecionar_timestamp_disco():
    try:
        db = connect(**config)
        if db.is_connected():
            with db.cursor() as c:
                c.execute("""
                    SELECT lc.data_hora,
                           lc.hostname AS host,
                           m.usuario,
                           lc.disk_percent,
                           lc.disk_read_mb_s,
                           lc.disk_write_mb_s
                    FROM infrawatch.componentes lc
                    JOIN infrawatch.maquina m ON m.idMaquina = lc.idMaquina
                    ORDER BY lc.data_hora DESC
                """)
                for data_hora, host, usuario, dperc, rmbs, wmbs in c.fetchall():
                    print(f"{data_hora} | {host}/{usuario} | DISK {dperc}% | R {rmbs} MB/s | W {wmbs} MB/s")
            db.close()
    except Error as e:
        print("Erro na consulta:", e)


def selecionar_timestamp_rede():
    try:
        db = connect(**config)
        if db.is_connected():
            with db.cursor() as c:
                c.execute("""
                    SELECT lc.data_hora,
                           lc.hostname AS host,
                           m.usuario,
                           lc.net_sent_kbps,
                           lc.net_recv_kbps
                    FROM infrawatch.componentes lc
                    JOIN infrawatch.maquina m ON m.idMaquina = lc.idMaquina
                    ORDER BY lc.data_hora DESC
                """)
                for data_hora, host, usuario, up, down in c.fetchall():
                    print(f"{data_hora} | {host}/{usuario} | NET ↑{up} kbps ↓{down} kbps")
            db.close()
    except Error as e:
        print("Erro na consulta:", e)


def selecionar_timestamp_swap():
    try:
        db = connect(**config)
        if db.is_connected():
            with db.cursor() as c:
                c.execute("""
                    SELECT lc.data_hora,
                           lc.hostname AS host,
                           m.usuario,
                           lc.swap_percent
                    FROM infrawatch.componentes lc
                    JOIN infrawatch.maquina m ON m.idMaquina = lc.idMaquina
                    ORDER BY lc.data_hora DESC
                """)
                for data_hora, host, usuario, swap_p in c.fetchall():
                    print(f"{data_hora} | {host}/{usuario} | SWAP {swap_p}%")
            db.close()
    except Error as e:
        print("Erro na consulta:", e)


def selecionar_timestamp_uptime_processos():
    try:
        db = connect(**config)
        if db.is_connected():
            with db.cursor() as c:
                c.execute("""
                    SELECT lc.data_hora,
                           lc.hostname AS host,
                           m.usuario,
                           lc.uptime_segundos,
                           lc.processos
                    FROM infrawatch.componentes lc
                    JOIN infrawatch.maquina m ON m.idMaquina = lc.idMaquina
                    ORDER BY lc.data_hora DESC
                """)
                for data_hora, host, usuario, up, procs in c.fetchall():
                    print(f"{data_hora} | {host}/{usuario} | UPTIME {up}s | PROC {procs}")
            db.close()
    except Error as e:
        print("Erro na consulta:", e)


def selecionar_timestamp_freq_temp_load():
    try:
        db = connect(**config)
        if db.is_connected():
            with db.cursor() as c:
                c.execute("""
                    SELECT lc.data_hora,
                           lc.hostname AS host,
                           m.usuario,
                           lc.cpu_freq_mhz,
                           lc.cpu_temp_c,
                           lc.load_avg_1min
                    FROM infrawatch.componentes lc
                    JOIN infrawatch.maquina m ON m.idMaquina = lc.idMaquina
                    ORDER BY lc.data_hora DESC
                """)
                for data_hora, host, usuario, freq, temp, load1 in c.fetchall():
                    print(f"{data_hora} | {host}/{usuario} | FREQ {freq} MHz | TEMP {temp} °C | LOAD1 {load1}")
            db.close()
    except Error as e:
        print("Erro na consulta:", e)


def menu_consulta():
    while True:
        print("\n=== INFRAWATCH ===")
        print("\n=== MENU DE CONSULTA ===")
        print("1 - Ver uso de CPU")
        print("2 - Ver uso de Memória RAM")
        print("3 - Ver uso do Disco (taxa e %)")
        print("4 - Ver uso da Rede (upload/download)")
        print("5 - Ver uso de Memória Swap")
        print("6 - Ver Tempo ligado (uptime) e Processos")
        print("7 - Ver Frequência, Temperatura e Carga da CPU")
        print("0 - Sair")
        opc = input("Opção: ").strip()
        match opc:
            case "1":
                selecionar_timestamp_cpu()
            case "2":
                selecionar_timestamp_memoria()
            case "3":
                selecionar_timestamp_disco()
            case "4":
                selecionar_timestamp_rede()
            case "5":
                selecionar_timestamp_swap()
            case "6":
                selecionar_timestamp_uptime_processos()
            case "7":
                selecionar_timestamp_freq_temp_load()
            case "0":
                print("Saindo...")
                break
            case _:
                print("Opção inválida.")

if __name__ == "__main__":
    menu_consulta()
