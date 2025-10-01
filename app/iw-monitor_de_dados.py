import psutil as p
import datetime
import time, os, platform, getpass, socket
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

def _ensure_maquina_and_get_id(db, hostname, usuario):
    empresa_id = 1
    with db.cursor(buffered=True) as c:
        c.execute("""
            SELECT idMaquina
            FROM infrawatch.maquina
            WHERE hostname = %s AND usuario = %s
            ORDER BY idMaquina DESC
            LIMIT 1
        """, (hostname, usuario))
        row = c.fetchone()
        if row:
            return row[0]
        c.execute("""
            INSERT INTO infrawatch.maquina (hostname, usuario, empresa_idEmpresa)
            VALUES (%s, %s, %s)
        """, (hostname, usuario, empresa_id))
        db.commit()
        return c.lastrowid

def converter_bytes_para_gigabytes(bytes_value):
    return round(bytes_value / (1024**3), 2)

def inserir_porcentagem_cpu(host, usuario, porcentagem, memoria, maquina_cpu,
                            disk_percent, disk_read_mb_s, disk_write_mb_s,
                            net_sent_kbps, net_recv_kbps,
                            swap_percent, uptime_segundos, processos,
                            cpu_freq_mhz, cpu_temp_c, load_avg_1min, data_hora):

    try:
        db = connect(**config)
        if db.is_connected():
            print('Conectado ao MySQL')

            fkMaquina = _ensure_maquina_and_get_id(db, host, usuario)

            try:
                ip = socket.gethostbyname(host)
            except Exception:
                ip = None

            with db.cursor() as cursor:
                query = """
                    INSERT INTO infrawatch.componentes (
                        idMaquina, hostname, ip,
                        porcentagem, memoria, maquina_cpu,
                        disk_percent, disk_read_mb_s, disk_write_mb_s,
                        net_sent_kbps, net_recv_kbps,
                        swap_percent, uptime_segundos, processos,
                        cpu_freq_mhz, cpu_temp_c, load_avg_1min, data_hora
                    ) VALUES (
                        %s, %s, %s,
                        %s, %s, %s,
                        %s, %s, %s,
                        %s, %s,
                        %s, %s, %s,
                        %s, %s, %s, %s
                    )
                """
                value = (
                    fkMaquina, host, ip,
                    porcentagem, memoria, maquina_cpu,
                    disk_percent, disk_read_mb_s, disk_write_mb_s,
                    net_sent_kbps, net_recv_kbps,
                    swap_percent, uptime_segundos, processos,
                    cpu_freq_mhz, cpu_temp_c, load_avg_1min, data_hora
                )
                cursor.execute(query, value)
                db.commit()
                print(cursor.rowcount, "registro inserido")
            
            db.close()
    
    except Error as e:
        print('Erro ao conectar com MySQL -', e) 

for i in range(20):
    disk_io_start = p.disk_io_counters()
    net_io_start = p.net_io_counters()
    t0 = time.time()

    porcentagem = p.cpu_percent(interval=1, percpu=False)

    disk_io_end = p.disk_io_counters()
    net_io_end = p.net_io_counters()
    dt = max(1e-6, time.time() - t0)

    memoria = p.virtual_memory().percent
    maquina_cpu = converter_bytes_para_gigabytes(p.virtual_memory().used)
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    disk_percent = p.disk_usage("/").percent
    read_bytes = max(0, disk_io_end.read_bytes - disk_io_start.read_bytes)
    write_bytes = max(0, disk_io_end.write_bytes - disk_io_start.write_bytes)
    disk_read_mb_s = round(read_bytes / dt / (1024**2), 3)
    disk_write_mb_s = round(write_bytes / dt / (1024**2), 3)

    sent_bytes = max(0, net_io_end.bytes_sent - net_io_start.bytes_sent)
    recv_bytes = max(0, net_io_end.bytes_recv - net_io_start.bytes_recv)
    net_sent_kbps = round((sent_bytes * 8) / dt / 1024, 2)
    net_recv_kbps = round((recv_bytes * 8) / dt / 1024, 2)

    swap_percent = p.swap_memory().percent
    uptime_segundos = int(time.time() - p.boot_time())
    processos = len(p.pids())

    try:
        freq = p.cpu_freq()
        cpu_freq_mhz = round(freq.current, 2) if freq else None
    except Exception:
        cpu_freq_mhz = None

    cpu_temp_c = None
    try:
        temps = p.sensors_temperatures()
        if temps:
            vals = []
            for arr in temps.values():
                for entry in arr:
                    if entry.current is not None:
                        vals.append(entry.current)
            if vals:
                cpu_temp_c = round(sum(vals) / len(vals), 2)
    except Exception:
        cpu_temp_c = None

    load_avg_1min = None
    try:
        load_avg_1min = round(os.getloadavg()[0], 2)
    except Exception:
        load_avg_1min = None

    host = platform.node()
    usuario = getpass.getuser()

    print(f"Porcentagem de uso {porcentagem}%")
    inserir_porcentagem_cpu(
        host, usuario, porcentagem, memoria, maquina_cpu,
        disk_percent, disk_read_mb_s, disk_write_mb_s,
        net_sent_kbps, net_recv_kbps,
        swap_percent, uptime_segundos, processos,
        cpu_freq_mhz, cpu_temp_c, load_avg_1min, data_hora
    )
