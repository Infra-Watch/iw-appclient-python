import psutil as p, time
from utils import conversor

def transferencia():
    net_io_start = p.net_io_counters()
    t0 = time.time()
    time.sleep(0.1)
    net_io_end = p.net_io_counters()
    dt = max(1e-6, time.time() - t0)
    
    sent_bytes = max(0, net_io_end.bytes_sent - net_io_start.bytes_sent)
    recv_bytes = max(0, net_io_end.bytes_recv - net_io_start.bytes_recv)
    bytes_enviados_kbps = conversor.bytes_para_kbps(sent_bytes, dt)
    bytes_recebidos_kbps = conversor.bytes_para_kbps(recv_bytes, dt)

    return {
        "saida": bytes_enviados_kbps,
        "entrada": bytes_recebidos_kbps
    }

def mac_address():
    if p.LINUX :
        mac_address = p.net_if_addrs().get('wlan0')[2][1]

    if p.WINDOWS :
        mac_address = p.net_if_addrs().get('Wi-Fi')[0][1]
    
    return mac_address 