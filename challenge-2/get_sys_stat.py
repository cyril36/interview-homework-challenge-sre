#!/usr/bin/env python3

import argparse
import psutil, sys, time

def to_gb(bytes):
    return round(bytes / 1024*1024*1024, 2)

def check_disk():
    for p in psutil.disk_partitions():
        try:
            u = psutil.disk_usage(p.mountpoint)
        except Exception as e:
            print(f"Error on {p.mountpoint}: {e}")
            continue
        print(f"{p.device} Total: {to_gb(u.total)} GB | Used: {to_gb(u.used)} GB | Free: {to_gb(u.free)} GB | {u.percent}%")

def check_cpu():
    print(f"Cores: {psutil.cpu_count()}")
    print(f"CPU usage: {psutil.cpu_percent(interval=1)}%")
    freq = psutil.cpu_freq()
    if freq:
        print(f"Frequency: {freq.current}")

def check_ports():
    try:
        connections = psutil.net_connections(kind="inet")
    except psutil.AccessDenied as e:
        print(f"Error: {e}. Try running with sudo.")
        return
    listening = [c for c in connections if c.status == psutil.CONN_LISTEN]
    exist = False
    def get_port(x):
        return x.laddr.port

    for c in sorted(listening, key=get_port):
        if not exist:
            print("Listening ports :")
            print("address:port")
            exist=True
        print(f"{c.laddr.ip}:{c.laddr.port}")
    if not exist:
        print("No listening ports.")

def check_ram():
    m = psutil.virtual_memory()
    print(f"Total: {to_gb(m.total)} GB")
    print(f"Used: {to_gb(m.used)} GB ({m.percent}%)")
    print(f"Available: {to_gb(m.available)} GB")

def check_overview():
    print("\n--- Top 10 processes (by CPU) ---")
    for p in psutil.process_iter():
        try:
            p.cpu_percent()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    procs.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
    for i in range(0, 10):
        cpu = procs[i]['cpu_percent'] or 0.0
        print(f"PID {procs[i]['pid']} CPU {cpu}%  {procs[i]['name']}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='myscript.py',
    )
    parser.add_argument('-d', '--disk', action='store_true', help='check disk stats')
    parser.add_argument('-c', '--cpu', action='store_true', help='check cpu stats')
    parser.add_argument('-p', '--ports', action='store_true', help='check listen ports')
    parser.add_argument('-r', '--ram', action='store_true', help='check ram stats')
    parser.add_argument('-o', '--overview', action='store_true', help='top 10 process with most CPU usage.')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    if args.disk: check_disk()
    if args.cpu: check_cpu()
    if args.ports: check_ports()
    if args.ram: check_ram()
    if args.overview: check_overview()
