import psutil as p
from utils import conversor

def porcentagem():
    return p.virtual_memory().percent

def gigabytes():
    return conversor.bytes_para_gb(p.virtual_memory().used)