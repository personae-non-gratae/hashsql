#!/usr/bin/python3

import netmiko
import nmap3
import sys

if len(sys.argv) != 3:
    print('Usage: ./getData.py <username> <path to ssh private key>')
    sys.exit(1)

nmap = nmap3.NmapScanTechniques()
results = nmap.nmap_ping_scan('10.0.0.0/24')

def connect(address):
    #create ssh connection usingd provided address to a linux device using ssh key authentication
    try:
        connection = netmiko.ConnectHandler(ip = str(address), device_type = 'linux', username = sys.argv[1], use_keys = True, key_file = sys.argv[2])
        return connection
    except Exception as ex:
        print(ex)
        return 503

def main():
    for addr in results:
        try:
            up = results[addr]['state']['state']
            print(addr + " : " + up)
            ssh_scan = nmap.nmap_tcp_scan(addr, args='-p 22')
            ssh_status = ssh_scan[addr]['ports'][0]['state']
            if ssh_status == "open":
                print(f"connecting to {addr}")
                ssh_connection = connect(addr)
                if ssh_connection != 503:
                    data = ssh_connection.send_command('ls -l')
                    print('Writing data')
                    f = open('data.txt', 'a')
                    f.write(str(addr))
                    f.write('\n')
                    f.write(data)
                    f.write('\n')
                    f.write('----------------------------------------------------')
                    f.write('\n')
                    f.close()
                else:
                    pass

        except:
            pass


if __name__ == '__main__':
    main()
