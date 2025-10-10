import psutil as p, time
from utils import conversor

def porcentagem():
    return p.disk_usage("/").percent

def velocidade():
    disk_io_start = p.disk_io_counters()
    t0 = time.time()
    time.sleep(0.1)
    disk_io_end = p.disk_io_counters()
    dt = max(1e-6, time.time() - t0)
    read_bytes = max(0, disk_io_end.read_bytes - disk_io_start.read_bytes)
    write_bytes = max(0, disk_io_end.write_bytes - disk_io_start.write_bytes)
    taxa_leitura_disco_mbps = conversor.bytes_para_mbps(read_bytes, dt)
    taxa_escrita_disco_mbps = conversor.bytes_para_mbps(write_bytes, dt)

    return {
        "escrita": taxa_escrita_disco_mbps,
        "leitura": taxa_leitura_disco_mbps
    }