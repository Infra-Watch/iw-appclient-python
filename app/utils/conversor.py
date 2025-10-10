def bytes_para_gb(bytes_value):
    return round(bytes_value / (1024**3), 2)

def bytes_para_mbps(bytes_value, tempo):
    return round((bytes_value * 8) / tempo / (1024**2), 6)

def bytes_para_kbps(bytes_value, tempo):
    return round((bytes_value * 8) / tempo / 1024, 6)