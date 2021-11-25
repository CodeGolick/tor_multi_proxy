import os
import time
import threading
import subprocess
import requests

from stem import Signal
from stem.control import Controller

class Tor():
    """Tor proxies"""
    def __init__(self, tor_path, min_port, max_port):
        self.path = tor_path
        self.max_port = max_port
        self.min_port = min_port
        self.cur_used_ports = []

    def start_ports(self):
        os.system('taskkill /f /im tor.exe')
        curpath = os.getcwd()
        self.tor_ports = []
        for x in range(self.min_port, self.max_port,2):
            self.tor_ports.append(x)

        for each_port in self.tor_ports:
            with open(self.path + '\\' + 'torrc.1', 'w', encoding='UTF-8') as file:
                file.write(f"SocksPort {str(each_port)}\n")
                file.write(f"ControlPort {str(each_port + 1)}\n")
                file.write(f"DataDirectory {self.path}{str(self.tor_ports.index(each_port)+1)}")

            threading.Thread(target=self.start_proc).start()
            time.sleep(1)

    def start_proc(self):
        subprocess.run(f'tor -f {self.path}\\torrc.1', shell=False)

    def set_port_used(self, port):
        self.cur_used_ports.append(port)

    def set_port_unused(self, port):
        self.cur_used_ports.remove(port)

    def get_free_proxy(self):
        for port in self.tor_ports:
            if port not in self.cur_used_ports:
                proxies = {
                    'http':  f'socks5://127.0.0.1:{str(port)}',
                    'https': f'socks5://127.0.0.1:{str(port)}'
                }
                self.set_port_used(port)
                return {'proxies':proxies,'port':port}
        return None

    def get_proxy(self,port):
        proxies = {
            'http':  f'socks5://127.0.0.1:{str(port)}',
            'https': f'socks5://127.0.0.1:{str(port)}'
        }
        return proxies

    def get_ip(self,port):
        req = requests.get('https://api.ipify.org?format=json', proxies = self.get_proxy(port))
        return str(req.json()['ip'])

    def change_ip(self,port):
        old_ip = self.get_ip(port)
        cur_ip = old_ip

        while old_ip == cur_ip:
            with Controller.from_port(port = port+1) as controller:
                controller.authenticate()
                controller.signal(Signal.NEWNYM)
            cur_ip = self.get_ip(port)

        self.set_port_unused(port)



# tor = Tor(
#     tor_path='C:\\tor\\Browser\\TorBrowser\\Data\\Tor', 
#     min_port = 9052, 
#     max_port = 9055
# )

# tor.start_ports()


# def func(tor):
#     proxy_data=tor.get_free_proxy()

#     if proxy_data != None:
#         proxies =  proxy_data['proxies']
#         port = proxy_data['port']
#         # code
#         print(tor.get_ip(port))
#         tor.change_ip(port)
#     else:
#         print('No free tor proxy')


# for x in range(0,2)
#     threading.Thread(target=func,args=[tor]).start()
