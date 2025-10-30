import psutil as p

def porcentagem():
    return p.cpu_percent(interval=0.2, percpu=False)

def frequencia():
    try:
        freq = p.cpu_freq()
        cpu_freq_mhz = round(freq.current, 2) if freq else 'null'
    except Exception:
        cpu_freq_mhz = 'null'

    return cpu_freq_mhz

def temperatura():
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
        cpu_temp_c = 'null'
    if(cpu_temp_c is None):
        return 'null'
    else:
        return cpu_temp_c