import socket


target_host = input("ip adress:")
port_max = input("how many ports:")
port_max = int(port_max)
port_range = (1, port_max)

def port_scan(target_host, port_range):
    for port in range(port_range[0], port_range[1] + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_host, port))
        if result == 0:
            print(f"Port {port} is open")
        else:
            print(f"Port {port} is closed")
        sock.close()


port_scan(target_host, port_range)

