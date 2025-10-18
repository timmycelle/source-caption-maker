import argparse
import os
import json
import subprocess
import platform
import sys
import shutil
from datetime import datetime, timezone
# ^ all standard python libs

parser=argparse.ArgumentParser()

# config
parser.add_argument("--mod","-m",required=True,type=str,help="Mod Folder - Specifies which mod folder to process from the `in/` directory")
parser.add_argument("--game-path","-p",type=str,help="Game Path - Path to Source game installation (for caption compilation)")
# watcha wan't, peasant?
parser.add_argument("--subtitles","-s",action="store_true",help="Convert subtitles of provided mod")
parser.add_argument("--captions","-c",action="store_true",help="Convert captions of provided mod")
# info & misc
parser.add_argument("--clear","-cls",action="store_true",help="Clear console history before starting")
parser.add_argument("--langs","-l",action="store_true",help="Print all supported languages")
parser.add_argument("--verbose","-v",action="store_true",help="Print additional processing information")
parser.add_argument("--delete-output","-do",action="store_true",help="Clear output folder writing output (Proceed with caution!)")
parser.add_argument("--open-output","-oo",action="store_true",help="Open output folder when finished")
parser.add_argument("--copy-output","-co",type=str,help="Copy output folder to specified location when finished")
parser.add_argument("--tim","-t",action="store_true",help="Open Steam profile of project author (timmycelle)")

args=parser.parse_args()

if args.clear:
    subprocess.run("cls"if os.name=="nt"else"clear",shell=True)
    print(" ".join(sys.argv))

if args.tim: # opens steam profile of timmycelle
    import webbrowser
    webbrowser.open_new_tab("https://www.steamcommunity.com/id/timmycelle")

class bcolors: # formatting
    INFO="\033[38;2;135;175;215m"
    VINFO="\033[38;2;135;155;215m"
    WARNING="\033[93m"
    FAIL='\033[91m'
    BOLD="\033[1m"
    ENDC="\033[0m"

def quot(string: str):
    if " " in string:
        return f"\"{string}\""
    else:
        return string
def vprint(content): # if user enabled verbose, this will print
    if args.verbose:
        print(content)
def jsonLoad(filename: str):
    with open(filename, "r", encoding="utf-8") as fdata:
        return json.load(fdata)
def fileLoad(filename: str):
    with open(filename, "r", encoding="utf-8") as fdata:
        return fdata.read()
def fileWrite(filename: str, what: str):
    with open(filename, "w", encoding="utf-16") as fdata:
        fdata.write(what)
        return True

ver="1.0.1" # version
sep="-----------------------------------------" # seperator
seplong=f"{sep}----------------------------"
startmsg=f"timmycelle | source-caption-maker | {ver}" # script info
url="https://github.com/timmycelle/source-caption-maker" # project repo url

# print start info
print(sep)
print(bcolors.BOLD + startmsg + bcolors.ENDC)
vprint(bcolors.VINFO + url + bcolors.ENDC)
print(sep)

didudosum=False # did you actually do something or are you just pretending?!
preparing=False
comp=False
types=[]

lang_list=["brazilian","bulgarian","czech","danish","dutch","english","finnish","french","german","greek","hungarian","italian","japanese","korean","koreana","latam","norwegian","polish","portuguese","romanian","russian","schinese","spanish","swedish","tchinese","thai","turkish","ukrainian"]
if args.langs: print(bcolors.INFO + f"supported languages{lang_list}" + bcolors.ENDC)

# checks if all arguments and config files are valid before continuing
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    p_file=os.path.dirname(sys.argv[0]) # pyinstaller exe process
else:
    p_file=os.path.dirname(__file__) # normal python process
p_modin=os.path.join(p_file, "in", args.mod)
p_modout=os.path.join(p_file, "out", args.mod)
vprint(bcolors.ENDC + bcolors.VINFO + f"checking if modin[ {quot(p_modin)} ] exists...")
if not os.path.exists(p_modin):
    print(bcolors.FAIL + f"mod[ {quot(p_modin)} ] doesn't exist!")
    print("won't continue." + bcolors.ENDC)
else:
    print(bcolors.INFO + f"mod[ {args.mod} ]" + bcolors.ENDC)
    vprint(bcolors.VINFO + f"modin[ {quot(p_modin)} ]")
    vprint(f"modout[ {quot(p_modout)} ]" + bcolors.ENDC)
    p_gamepath=args.game_path
    if args.game_path:
        if not os.path.exists(p_gamepath):
            print(bcolors.FAIL + f"gamepath[ {quot(p_gamepath)} ] not found!")
            print("Won't continue." + bcolors.ENDC)
        else: # prepares stuff
            p_captioncomp=os.path.join(p_gamepath, "bin", "captioncompiler.exe")

            print(bcolors.INFO + f"gamepath[ {quot(p_gamepath)} ]" + bcolors.ENDC)
            vprint(bcolors.VINFO + f"captioncomp[ {quot(p_captioncomp)} ]" + bcolors.ENDC)

    if args.subtitles or args.captions:
        preparing=True
        if args.subtitles:
            types.append("subtitles")
        if args.captions:
            types.append("closecaption")
if preparing:
    for typ in types:
        comp=False
        print(bcolors.ENDC + seplong + bcolors.INFO + f"\ntype[ {typ} ]")
        p_jsontype=os.path.join(p_file, p_modin, f"{typ}.json")

        if os.path.exists(p_jsontype)==False:
            print(bcolors.FAIL + f"no JSON data found for {typ}!")
            print("won't continue." + bcolors.ENDC)
        else:
            comp=True
            dataF=jsonLoad(p_jsontype) # full data
            vprint(bcolors.VINFO + f"input json[\n{dataF}\n]" + bcolors.ENDC)
            valid_lang_list=list(dataF.keys())
            if "misc" in valid_lang_list:
                valid_lang_list.remove("misc")
            print(bcolors.INFO + f"languages found with data{valid_lang_list}" + bcolors.ENDC)

            # creates "out" folder and "gameinfo.txt" if they don't exist
            p_creditsextra=os.path.join(p_file, p_modin, "credits.txt")
            p_outfolder=os.path.join(p_file, p_modout, "resource")
            p_gameinfo=os.path.join(p_file, p_modout, "gameinfo.txt")
            creditsextra=""
            if os.path.exists(p_creditsextra):
                creditsextra=fileLoad(p_creditsextra)
                vprint(bcolors.VINFO + f"found credits[ {quot(p_creditsextra)} ]!")
                vprint(f"credits[ {creditsextra} ]" + bcolors.ENDC)
            if os.path.exists(p_outfolder)==False:
                os.makedirs(p_outfolder)
            if os.path.exists(p_gameinfo)==False:
                fileWrite(p_gameinfo, """// This is a dummy GameInfo in order for captioncompiler.exe to accept the created .txt files inside "resource".
// It's safe to remove this after compiling
// Created with source-caption-maker by timmycelle

"GameInfo"
{
FileSystem
{
SearchPaths
{
game		|gameinfo_path|.
}
}
}""")
            infodate=datetime.now(timezone.utc).strftime("%Y-%m-%d")
            infotime=datetime.now(timezone.utc).strftime("%H:%M:%S")
            offset=datetime.now().astimezone().utcoffset()
            if offset is not None:
                infoutc=f"UTC+{int(offset.total_seconds()/3600)}:00"
            else:
                infoutc="UTC+0:00"
            credits=f"\n\n// Auto-generated with source-caption-maker {ver} by timmycelle\n// {url}\n\n// Generated on {infodate} at {infotime} {infoutc}\n"
            if creditsextra:
                lines=creditsextra.split("\n")
                creditsextra=""
                for line in lines:
                    creditsextra=(f"{creditsextra}// {line}\n")
                creditsextra=creditsextra.removesuffix("\n")
                credits=f"{credits}\n{creditsextra}\n"
            vprint(bcolors.VINFO + f"infodate[ {infodate} ]\ninfotime[ {infotime} ]\ninfoutc[ {infoutc} ]" + bcolors.ENDC)
            
            p_resource=os.path.join(p_file, p_modout, "resource")
            if args.delete_output:
                print(bcolors.BOLD + f"Deleting [ {quot(p_resource)} ]..." + bcolors.ENDC)
                shutil.rmtree(p_resource)
                os.mkdir(p_resource)

            print("\nConverting...\n")

            totaldurations=[]
            if comp:
                for lang in valid_lang_list: # actual convertion
                    linesOUT=[]
                    print(bcolors.ENDC + f"///--------- {typ.upper()}_{lang.upper()} ---------\\\\\\" + bcolors.INFO)
                    data=dataF[lang]
                    if "misc" in dataF.keys():
                        def jsonMerge(dict1, dict2):
                            for key, value in dict2.items():
                                if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
                                    jsonMerge(dict1[key], value)
                                else:
                                    dict1[key] = value
                        jsonMerge(data, dataF["misc"])
                    vprint(bcolors.ENDC + bcolors.VINFO + f"merged json[\n{data}\n]")
                    vprint("\nlines[")
                    acts=list(data.keys())
                    for act in acts:
                        infoact=f"----- {act} -----"
                        linesOUT.append(f"// {infoact}")
                        vprint(infoact)
                        data_act=data[act]
                        chars=list(data_act.keys())
                        for char in chars:
                            infochar=f"--- {char} ---"
                            linesOUT.append(f"// {infochar}")
                            vprint(infochar)
                            data_char=data_act[char]
                            if "lines" in data_char:
                                data_lines=data_char["lines"]
                                for line in data_lines:
                                    def value(key: str): # get keys
                                        if key in data_lines[line]:
                                            return data_lines[line][key]
                                        elif key in data_char:
                                            return data_char[key]
                                    # set and handle the keys
                                    txt=str(value("txt")).replace("\"", r"\"").replace("\n", "<cr>")
                                    name=""
                                    if not value("ndn")==False: # ndn
                                        name=f"<B>{value("dn")}<B>: " # dn
                                        if value("bold"):
                                            name=f"{name}<B>"
                                        if value("italic"):
                                            name=f"{name}<I>"
                                    codes=""
                                    clr=value("clr")
                                    playerclr=value("playerclr")
                                    if clr or playerclr:
                                        import colour
                                    if clr:
                                        clr=clr.replace(" ", "")
                                        if "#" in clr: # if "#" is in the clr key, it assumes it is a hex code and converts it back to rgb to use
                                            clrs=colour.hex2rgb(clr)
                                            clr=f"{int(clrs[0]*255)},{int(clrs[1]*255)},{int(clrs[2]*255)}"
                                        codes=f"{codes}<clr:{clr}>"
                                    if playerclr: # wip
                                        playerclr=playerclr.replace(" ", "")
                                        codes=f"{codes}<playerclr:{playerclr}>"
                                    if value("bold") and value("ndn"): # bold & ndn
                                        codes=f"{codes}<B>"
                                    if value("italic") and value("ndn"): # italic
                                        codes=f"{codes}<I>"
                                    if value("sfx"):
                                        codes=f"{codes}<sfx>"
                                    if value("norepeat"): # norepeat
                                        codes=f"{codes}<norepeat:{value("norepeat")}>"
                                    if value("len"): # len
                                        codes=f"{codes}<len:{value("len")}>"
                                    # put it all together and append it to finished lines array
                                    linenine=f"\"{char}.{line}\"\"{codes}{name}{txt}\"" # ln reference?!
                                    vprint(linenine)
                                    linesOUT.append(linenine)
                    vprint("]" + bcolors.ENDC + bcolors.INFO)
                    print(f"\nDone converting {typ} for language[ {lang} ]!")
                    linesOUT_str=""
                    p_langtxt=os.path.join(p_resource, f"{typ}_{lang}.txt")
                    p_langtxtsingle=f"{typ}_{lang}.txt"
                    for line in linesOUT:
                        linesOUT_str=f"{linesOUT_str}{line}\n"
                    linesOUT_str=linesOUT_str.removesuffix("\n")
                    # creates output files
                    OUT=f"\"lang\"\n[\n\"Language\" \"{lang}\"\n\"Tokens\"\n[\nlines\n]\n]credits"
                    OUT=OUT.replace("[", "{")
                    OUT=OUT.replace("]", "}")
                    OUT=OUT.replace("lines", linesOUT_str)
                    OUT=OUT.replace("credits", credits)
                    if fileWrite(p_langtxt, OUT):
                        didudosum=True
                        print(f"Successfully written to outtxt[ {p_langtxt} ]!\n")
                    if args.game_path and os.path.exists(p_captioncomp):
                        cmd=f"{quot(p_captioncomp)} {quot(p_langtxtsingle)} -game {quot(os.path.join(p_file, f'{p_modout}'))}"
                        if platform.system()=="Linux": # if system is linux, put "wine" at the beginning of the command
                            cmd=f"wine {cmd}"
                        vprint(bcolors.ENDC + bcolors.VINFO + f"> {cmd}\n" + bcolors.ENDC + bcolors.INFO)
                        subprocess.run(cmd)
                        print(bcolors.ENDC)
    if didudosum: # end msg
        print(bcolors.ENDC + seplong)
        print(bcolors.BOLD + f"Done! See your results in[ {quot(p_resource)} ]")
        if args.open_output:
            print(f"Opening [ {quot(p_resource)} ]...")
            if platform.system()=="Windows":
                os.startfile(p_resource)
            else:
                try:
                    subprocess.call(('xdg-open', p_resource))
                except FileNotFoundError:
                    print(bcolors.FAIL + "Error: xdg-open not found. You may need to install it." + bcolors.ENDC)
        if args.copy_output:
            p_copyresult=os.path.join(args.copy_output, "resource")
            print(f"Copying [ {quot(p_resource)} ] to [ {quot(p_copyresult)} ]...")
            if os.path.exists(p_copyresult)==False:
                os.mkdir(p_copyresult)
            shutil.copytree(p_resource, p_copyresult, dirs_exist_ok=True)
        print("\nThank ya for using the thingy" + bcolors.ENDC)
        print(":doorhandlespin:")