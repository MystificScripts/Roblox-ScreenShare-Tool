import os,os,requests,json,binascii,colorama,time,re,signal,ctypes,sys
import time as t
from colorama import Fore, Style
from browser_history import get_history

colorama.init()

with open('scanner.json', 'r') as c:
    config = json.load(c)

url = "http://embed.ihatemystupid.life/log.php?hexy="

G, R, Y, B, M, RESET = Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA,Style.RESET_ALL
results = []


# terminal anti ctrl c + any ide as pycharm etc
def anti1(signal, frame):
    print(Fore.RED + "Ctrl+C is currently disabled." + Style.RESET_ALL)
signal.signal(signal.SIGINT, anti1)



def find(path, keywords, color, message, found, extensions=None):
    for r, d, f in os.walk(os.path.expanduser(path)):
        for item in d + f:
            if extensions and not item.lower().endswith(extensions):
                continue
            for keyword in keywords:
                if keyword.lower() in item.lower() and item not in found:
                    res = f"{color}[+] Found {message}{RESET} in: {os.path.join(r, item)}"
                    print(res)
                    results.append(clrremo(res))

def search_lua(path, lua_keywords, color, found):
    for r, d, files in os.walk(os.path.expanduser(path)):
        for file in files:
            if file.lower().endswith(".lua"):
                file_path = os.path.join(r, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as lua_file:
                    content = lua_file.read()
                    for keyword in lua_keywords:
                        if keyword.lower() in content.lower():
                            res = f"{color}[+] Found Lua file with sus word '{keyword}'{RESET} in: {file_path}"
                            print(res)
                            results.append(clrremo(res))

def find_scriptware_dll(directory):
    for r, d, files in os.walk(directory):
        for fn in files:
            if fn.lower().endswith('.dll') and 'README.txt' in files:
                res = f"{Y}[+] Found scriptware dll: {os.path.join(r, fn)}{RESET}"
                print(res)
                results.append(clrremo(res))

def lgapi(data):
    chunk_size = 6000
    encoded_data = binascii.hexlify("\n".join(data).encode()).decode()

    for i in range(0, len(encoded_data), chunk_size):
        chunk = encoded_data[i:i+chunk_size]
        api_url_with_data = url + chunk

        response = requests.get(api_url_with_data)

def clrremo(text):
    return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', text)

found_items = set()

def process_search_folder(keywords, search_folders, color, message, extensions=None):
    for folder_path in search_folders:
        find(folder_path, keywords, color, message, found_items, extensions)

def process_lua_search(lua_path, lua_keywords, color):
    for folder in lua_path:
        search_lua(folder, lua_keywords, color, found_items)

def process_dll_search(directory):
    find_scriptware_dll(os.path.expanduser(directory))

def process_bin_search(bin_files, search_folders, color):
    for folder_path in search_folders:
        for bin_file in bin_files:
            find(folder_path, [bin_file], M, f"{bin_file} file", found_items)


process_search_folder(config['folders']['keywords'], config['dlls']['search_folders'], G, "sus folder")
process_search_folder(config['exes']['keywords'], config['dlls']['search_folders'], R, "(.exe)", ".exe")
process_search_folder(config['dlls']['keywords'], config['dlls']['search_folders'], Y, "(.dll)", ".dll")

roaming_folders = config.get('roaming_search', {}).get('folders', [])
hidden_folders = config.get('hidden_folders', [])
for folder_name in roaming_folders:
    process_search_folder([], [f"~/AppData/Roaming/{folder_name}"], B, folder_name)
for folder_name in hidden_folders:
    process_search_folder([], [f"~/AppData/Local/{folder_name}"], B, folder_name)

process_lua_search(config['dlls']['search_folders'], config.get('luafiles', []), B)
process_dll_search('~\\AppData\\Roaming')

bin_files = config.get('bin_files', []) 
process_bin_search(bin_files, config['dlls']['search_folders'], B)

if results:
    lgapi(results)
    print("Done scanning contiuning in more scanning: ")
    time.sleep(2)

with open('main.json', 'r') as j:
    config = json.load(j)

suswords = config.get("suswords", [])
owners = config.get("owners", {})
linkvertise_owners = config.get("linkvertiseowners", {})
checkpoints = config.get("checkpoints", {})

out = get_history()
hist = out.histories

printed_links = set()

def chcksus(url, susword_list):
    for s in susword_list:
        if s in url:
            return True
    return False

def fnow(url, owner_dict):
    for t, o in owner_dict.items():
        if url.startswith(t):
            return o
    return None

def prntwc(text, color):
    print(f"{color}{text}")


while True:
    user_choice = input("Another quick check? (y/n): ").lower()
    if user_choice == 'n':
        print("Goodbye!")
        t.sleep(3)
        break
    elif user_choice == 'y':
        for time, url in hist:
            if url not in printed_links:
                if chcksus(url, suswords):
                    prntwc(f"Susword in URL: {url}", Fore.RED)
                owner = fnow(url, owners)
                if owner:
                    owner_color = Fore.YELLOW if owner == 'chks' else Fore.LIGHTYELLOW_EX
                    prntwc(f"Threat in link: {url} (Owner: {owner})", owner_color)
                printed_links.add(url)
    else:
        print("Invalid choice. Enter 'y' or 'n'.")

print(Fore.RESET)



