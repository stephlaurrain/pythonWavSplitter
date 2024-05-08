import os
import sys
import gc
from main import Wavesplit
from datetime import datetime

wavesplit = Wavesplit()

class Menuitem:
    def __init__(self, command, label, nb_params=0, jsonfilename='default', ret=False):
        self.command = command
        self.label = label
        self.nb_params = nb_params        
        self.jsonfilename = jsonfilename
        self.ret = ret

root_app = os.getcwd()


def dotail(profil):

    log_filename = "{root_app}{os.path.sep}log{os.path.sep}{dnow}{profil}.log"
    os.system(f"tail -f {log_filename}")

hardgreen = "\033[32m\033[1m"
normalgreen = "\033[32m\033[2m"
normalcolor = "\033[0m"


def mencol(nb, fonc, comment):
    return f"{hardgreen}{nb} - {fonc} {normalgreen} - {comment}{normalcolor}"


def drkcol(str):
    return f"{hardgreen}{str}{normalcolor}"


def clear():
    return os.system('clear')

nb_args = len(sys.argv)

jsonfile_from_arg = "default" if (nb_args == 1) else sys.argv[1]

clear()
wavesplit = Wavesplit()

while True:
    print(drkcol("\nHi Neo, I'm your wave splitter"))
    print(drkcol("Your wish is my order\n"))
    print(drkcol("What I can do for you :\n"))
    print(drkcol("usage :\n"))
    print(drkcol("param 0 = drumkit_master path :\n"))
    print(drkcol("param 1 = drumkit_name :\n"))
    menulist = []
    menulist.append(Menuitem("split", "split files from EZdrummer", 0, "Ezdrummer"))
    menulist.append(Menuitem("split", "split files from Kult2", 0, "kult2"))    
    menulist.append(Menuitem("split", "split files from other", 0, "extractFade"))        
    menulist.append(Menuitem("clean", "delete files that has same hash into drumkit_main_path", 0, "Ezdrummer"))
    menulist.append(Menuitem("test", "test something", "default"))

    for idx, menuitem in enumerate(menulist):
        print (mencol(idx, menuitem.command, menuitem.label))
        if menuitem.ret:
            print(drkcol("#####"))

    print(drkcol("#####"))
    print(mencol("99", "exit", "exit this menu"))
    dothat = input(drkcol("\n\nReady to explode : "))

    today = datetime.now()
    dnow = today.strftime(r"%y%m%d")

    if dothat == "55":
        print(drkcol("\ntail -f default\n"))
        dotail("default")
    if dothat == "99":
        print(drkcol("\nsee you soon, Neo\n"))
        del wavesplit
        gc.collect
        quit()
    try:
        if int(dothat) < 50:
            cmdstr = "nop"

            item = menulist[int(dothat)]
            cmd = item.command
            jsonfile = item.jsonfilename
            print (cmd)
            prms = int(item.nb_params)
            prmcmdlist = []
            for i in range(prms):
                prmcmdlist.append(input(drkcol(f"enter param {i} :")))
            prm1 = "" if (len(prmcmdlist) < 1) else prmcmdlist[0]
            prm2 = "" if (len(prmcmdlist) < 2) else prmcmdlist[1]

            if wavesplit.main(cmd, jsonfile, prm1, prm2) is False:
                raise SystemError('Splitter had a problem')

    except Exception as e:
        print (e)
        print(f"\n{hardgreen}bad command (something went wrong){normalcolor}\n")
        raise
