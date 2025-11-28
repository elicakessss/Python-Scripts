import psutil
import platform
import socket
import os
from datetime import datetime

def get_system_info():
    """
    Gather and display comprehensive system information.
    """
    print("=" * 60)
    print("SYSTEM INFORMATION".center(60))
    print("=" * 60)
    print()
    
    # Basic system info
    print("COMPUTER & OS")
    print("-" * 60)
    print(f"Computer Name:       {socket.gethostname()}")
    print(f"Operating System:    {platform.system()}")
    print(f"OS Version:          {platform.version()}")
    print(f"Platform:            {platform.platform()}")
    print(f"Architecture:        {platform.machine()}")
    print()
    
    # Processor info
    print("PROCESSOR")
    print("-" * 60)
    print(f"Processor:           {platform.processor()}")
    print(f"Physical Cores:      {psutil.cpu_count(logical=False)}")
    print(f"Logical Cores:       {psutil.cpu_count(logical=True)}")
    print(f"CPU Usage:           {psutil.cpu_percent(interval=1)}%")
    print(f"CPU Frequency:       {psutil.cpu_freq().current:.2f} MHz")
    print()
    
    # Memory info
    print("MEMORY")
    print("-" * 60)
    mem = psutil.virtual_memory()
    print(f"Total RAM:           {mem.total / (1024**3):.2f} GB")
    print(f"Available RAM:       {mem.available / (1024**3):.2f} GB")
    print(f"Used RAM:            {mem.used / (1024**3):.2f} GB")
    print(f"RAM Usage:           {mem.percent}%")
    
    swap = psutil.swap_memory()
    print(f"Total Swap:          {swap.total / (1024**3):.2f} GB")
    print(f"Swap Usage:          {swap.percent}%")
    print()
    
    # Disk info
    print("DISK STORAGE")
    print("-" * 60)
    disk = psutil.disk_usage('/')
    print(f"Total Disk:          {disk.total / (1024**3):.2f} GB")
    print(f"Used Disk:           {disk.used / (1024**3):.2f} GB")
    print(f"Free Disk:           {disk.free / (1024**3):.2f} GB")
    print(f"Disk Usage:          {disk.percent}%")
    print()
    
    # Network info
    print("NETWORK")
    print("-" * 60)
    print(f"Hostname:            {socket.gethostname()}")
    try:
        print(f"IP Address:          {socket.gethostbyname(socket.gethostname())}")
    except:
        print(f"IP Address:          Unable to retrieve")
    
    net_io = psutil.net_io_counters()
    print(f"Bytes Sent:          {net_io.bytes_sent / (1024**3):.2f} GB")
    print(f"Bytes Received:      {net_io.bytes_recv / (1024**3):.2f} GB")
    print()
    
    # System uptime
    print("SYSTEM UPTIME")
    print("-" * 60)
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"Uptime:              {days}d {hours}h {minutes}m {seconds}s")
    print(f"Boot Time:           {datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Top processes by CPU usage
    print("TOP PROCESSES (CPU USAGE)")
    print("-" * 60)
    processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), 
                      key=lambda p: p.info['cpu_percent'], reverse=True)[:5]
    for proc in processes:
        try:
            print(f"{proc.info['name']:<35} {proc.info['cpu_percent']:>6.2f}%")
        except:
            pass
    print()
    
    # Top processes by memory usage
    print("TOP PROCESSES (MEMORY USAGE)")
    print("-" * 60)
    processes = sorted(psutil.process_iter(['pid', 'name', 'memory_percent']), 
                      key=lambda p: p.info['memory_percent'], reverse=True)[:5]
    for proc in processes:
        try:
            print(f"{proc.info['name']:<35} {proc.info['memory_percent']:>6.2f}%")
        except:
            pass
    print()
    print("=" * 60)

if __name__ == "__main__":
    try:
        get_system_info()
    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nNote: You may need to install psutil:")
        print("  pip install psutil")