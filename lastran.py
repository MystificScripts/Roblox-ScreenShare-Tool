import os, re, json, time,sys
from colorama import Fore, Style, init
import ctypes

init(autoreset=True)

# Check if the script is running with administrative privileges
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def rn():
    pfc = "C:\\Windows\\Prefetch"
    return {re.sub(r"\.pf$", "", f, flags=re.IGNORECASE) for f in os.listdir(pfc) if f.endswith(".pf")}

def hld():
    rec = rn()
    
    with open("blacklist.json", "r") as jf:
        data = json.load(jf)
    
    bl = data.get("blacklisted_words", [])
    
    nbp = []
    bkp = []
    
    for p in rec:
        blkd = any(w.lower() in p.lower() for w in bl)
        if blkd:
            bkp.append(p)
        else:
            nbp.append(p)
    
    for i, p in enumerate(nbp, 1):
        print(f"{i}. {p}")
    
    if bkp:
        print(Fore.RED + "Recently Run Blacklisted Programs:")
        for i, p in enumerate(bkp, len(nbp) + 1):
            for w in bl:
                if w.lower() in p.lower():
                    p = p.replace(w, Fore.YELLOW + w + Style.RESET_ALL)
            print(f"{i}. {p}")
    
    if not rec:
        print("No recently run programs found.")
    
    time.sleep(25)

hld()
