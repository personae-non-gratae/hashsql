#!/usr/bin/python3

import netmiko
import nmap3
import sys

#print usage 
if len(sys.argv) != 4:
    print('Usage: ./getData.py <cidr range> <username> <path to ssh private key>')
    sys.exit(1)

nmap = nmap3.NmapScanTechniques()


def connect(address):
    #create ssh connection using provided address to a linux device using ssh key authentication
    try:
        connection = netmiko.ConnectHandler(ip = str(address), device_type = 'linux', username = sys.argv[2], use_keys = True, key_file = sys.argv[3])
        return connection
    except Exception as ex:
        print(ex)
        return 503

def main():
    #pings all hosts in subnet, for hosts that are up check if ssh is open, if it is connect and run command
    commands = input('Enter commands seperated by commas ",": ')
    commands_list = commands.split(',')
    results = nmap.nmap_ping_scan(sys.argv[1])
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
                    for cmd in range(len(commands_list)):
                        try:
                            data = ssh_connection.send_command(str(commands_list[cmd]))
                            print('Writing data')
                            f = open('data.txt', 'a')
                            f.write(str(addr))
                            f.write('\n')
                            f.write(str(commands_list[cmd]))
                            f.write('\n')
                            f.write(data)
                            f.write('\n')
                            f.write('----------------------------------------------------')
                            f.write('\n')
                            f.close()
                        except Exception as X:
                            print(X)
                            pass
                else:
                    pass

        except:
            pass


if __name__ == '__main__':
    main()
