import os, platform, random, threading

class Cache:
    def __init__(self, file_name):
        self.file_name = file_name
        self.cache = {}
        self.read_cache_file()

    def read_cache_file(self):
        with open(self.file_name, "r") as f:
            for line in f:
                var, value = line.strip().split(" ", 1)
                self.cache[var] = value

    def write_cache_file(self):
        with open(self.file_name, "w") as f:
            for var, value in self.cache.items():
                f.write(f"{var} {value}\n")

    def get(self, var):
        return self.cache.get(var)

    def set(self, var, value):
        self.cache[var] = value
        self.write_cache_file()

    def delete(self, var):
        self.cache.pop(var, None)
        self.write_cache_file()

cache = Cache("cache")
sysName = platform.system

def firstStart():
    cache = Cache("cache")
    firstStartCache = cache.get("firstStart")
    if firstStartCache == "True":
        os.system('pip install colorama paramiko mysql-connector-python')
        cache.set("firstStart", "False")
        os.system("cls")
    else:
        return

firstStart()

import paramiko
from colorama import Fore

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

class ServerList:
    def __init__(self, file_name):
        self.file_name = file_name

    def add_server(self, server_name, ip, password):
        serverss = self.get_servers()
        idd = random.randint(1111, 9999)
        with open(self.file_name, "r") as filee:
            for line in filee:
                    parts = line.strip().split(",")
                    serverss.append((parts[0], parts[1], parts[2], parts[3]))
                    existingidd = parts[0]
                    if idd == existingidd:
                        idd + 1
        with open(self.file_name, "a") as file:
            file.write(f"{idd},{server_name},{ip},{password}\n")
            print(Fore.GREEN+"  Created "+ip+" with ID "+str(idd)+"\n"+Fore.RESET)
            
    def get_server(self, idd):
        with open(self.file_name, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                if parts[1] == idd:
                    return parts[0], parts[1], parts[2], parts[3]
        return None, None, None, None

    def get_servers(self):
        servers = []
        with open(self.file_name, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                servers.append((parts[0], parts[1], parts[2], parts[3]))
        return servers

    def edit_server(self, iddin):
        servers = self.get_servers()
        new_servers = []
        found = False
        for ca, n, i, p in servers:
            if ca == iddin:
                found = True
                name = input("  New Server Name (Old "+n+" ): ")
                new_ip = input("  New Server IP (Old "+i+" ): ")
                password = input("  New Server Password: ")
                new_servers.append((iddin, name, new_ip, password))
            else:
                new_servers.append((ca, n, i, p))
        if not found:
            print(Fore.RED + "  Server ID " + iddin + " not found" + Fore.RESET)
            input("  Enter to go back")
        else:
            with open(self.file_name, "w") as file:
                for iddin, name, new_ip, password in new_servers:
                    file.write(f"{iddin},{name},{new_ip},{password}\n")
            print(Fore.GREEN + "  Edited " + iddin + " successfully\n" + Fore.RESET)
            input("  Enter to go back")

    def delete_server(self, iddin):
        servers = self.get_servers()
        new_servers = []
        deleted = False
        for idd, name, ip, password in servers:
            if idd != iddin:
                new_servers.append((idd, name, ip, password))
            else:
                deleted = True
        if deleted:
            with open(self.file_name, "w") as file:
                for idd, name, ip, password in new_servers:
                    file.write(f"{idd},{name},{ip},{password}\n")
            print(Fore.GREEN + "  Deleted Server " + iddin + " " + ip + "\n" + Fore.RESET)
        if not deleted:
            print(Fore.RED + "  Unknown Server "+iddin+Fore.RESET)

    def procrun(self, ip, name, password, commandprompt):
        try:
            ssh.connect(hostname=ip, username=name, password=password)
            stdin, stdout, stderr = ssh.exec_command(commandprompt)
            output = stdout.read().decode("utf-8")
            print(Fore.YELLOW+"  OUTPUT -> "+ip+":", output+"\n"+Fore.RESET)
            error = stderr.read().decode("utf-8")
            if error:
                print(Fore.RED+"  ERROR -> "+ip+":", error+"\n"+Fore.RESET)
        except Exception as e:
            print(Fore.RED+"  ERROR -> "+ip+":", str(e)+"\n"+Fore.RESET)

    def send_command_all(self):
        servers = self.get_servers()
        while True:
            commandprompt = input("  Command to send (q to quit): ")
            if commandprompt == "q":
                break
            with open(self.file_name, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    servers.append((parts[0], parts[1], parts[2], parts[3]))
                    name = parts[1]
                    ip = parts[2]
                    password = parts[3]
                    proc = threading.Thread(target=self.procrun(ip, name, password, commandprompt))
                    try:
                        proc.start()
                    except Exception as e:
                        print(Fore.RED+"  ERROR -> "+ip+":"+str(e)+"\n"+Fore.RESET)

    def send_command(self, idin):
        while True:
            servers = self.get_servers()
            found = False
            with open(self.file_name, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    servers.append((parts[0], parts[1], parts[2], parts[3]))
                    idd = parts[0]
                    if idin == idd:
                        found = True
            if found:
                commandprompt = input("  Command to send (q to quit): ")
                if commandprompt == "q":
                    break
                name = parts[1]
                ip = parts[2]
                password = parts[3]
                proc = threading.Thread(target=self.procrun(ip, name, password, commandprompt))
                proc.start()
            if not found:
                print(Fore.RED+"  Unknown Server ID "+idin+Fore.RESET)
                break


    def check_status(self):
      servers = self.get_servers()
      with open(self.file_name, "r") as file:
        for line in file:
          parts = line.strip().split(",")
          servers.append((parts[0], parts[1], parts[2], parts[3]))
          idd = parts[0]
          name = parts[1]
          ip = parts[2]
          password = parts[3]
          try:
            ssh.connect(hostname=ip, username=name, password=password)
            stdin, stdout, sterr = ssh.exec_command("uptime")
            output = stdout.read().decode("utf-8")
            print(Fore.GREEN+"  SUCCESS -> "+idd+" "+ip+": "+output+Fore.RESET+"\n")
          except Exception as e:
            print(Fore.RED+"  ERROR -> "+idd+" "+ip+": "+str(e)+Fore.RESET+"\n")

def main():
  while True:
    os.system("cls")
    print(Fore.RED+"""
    ██████╗ ██╗      █████╗ ███████╗███╗   ███╗██╗ ██████╗
    ██╔══██╗██║     ██╔══██╗╚══███╔╝████╗ ████║██║██╔════╝
    ██████╔╝██║     ███████║  ███╔╝ ██╔████╔██║██║██║     
    ██╔═══╝ ██║     ██╔══██║ ███╔╝  ██║╚██╔╝██║██║██║     
    ██║     ███████╗██║  ██║███████╗██║ ╚═╝ ██║██║╚██████╗
    ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝ ╚═════╝
                                                      
    Server Management Panel
    MX Marvin - 2023
    """+Fore.RESET)
    print("  1. List all servers")
    print("  2. Add server")
    print("  3. Edit server")
    print("  4. Delete server")
    print("  5. Send command server via id")
    print("  6. Send command to all servers")
    print("  7. Check servers status")
    print("  8. Exit\n")
    choice = str(input("  Enter your choice: "))
    server_list = ServerList("servers")
    if choice == "1":
        os.system("cls")
        print("  <-- List Servers -->\n")
        servers = server_list.get_servers()
        for server in servers:
          print("  "+server[0], server[1], server[2]+"\n")
        input("  Enter to go back")

    elif choice == "2":
        os.system("cls")
        print("  <-- Create Server -->\n")
        server_name = input("  Server Username: ")
        ip_address = input("  Server IP: ")
        password = input("  Server Password: ")
        server_list.add_server(server_name, ip_address, password)
        input("  Enter to go back")

    elif choice == "3":
        os.system("cls")
        print("  <-- Edit Server -->")
        servers = server_list.get_servers()
        for server in servers:
          print("  "+server[0], server[1], server[2]+"\n")
        iddin = input("  Server ID to Edit: ")
        server_list.edit_server(iddin)

    elif choice == "4":
        os.system("cls")
        print("  <-- Delete Server -->\n")
        servers = server_list.get_servers()
        for server in servers:
          print("  "+server[0], server[1], server[2]+"\n")
        iddin = input("  Server ID to Delete: ")
        server_list.delete_server(iddin)
        input("  Enter to go back")

    elif choice == "5":
        os.system("cls")
        print("  <-- Send Command -->\n")
        servers = server_list.get_servers()
        for server in servers:
          print("  "+server[0], server[1], server[2]+"\n")
        idin = input("  Server ID to send command: ")
        server_list.send_command(idin)
        input("  Enter to go back")

    elif choice == "6":
        os.system("cls")
        print("  <-- Send Command to All -->\n")
        server_list.send_command_all()
        input("  Enter to go back")
    elif choice == "7":
        os.system("cls")
        print("  <-- Server Status -->\n")
        server_list.check_status()
        input("  Enter to go back")
    elif choice == "8":
        os.system("cls")
        break
    else:
        print(Fore.RED+"  Invalid choice. Try again."+Fore.RESET)
if __name__ in "__main__":
  main()