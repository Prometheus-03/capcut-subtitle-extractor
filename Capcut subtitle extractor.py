"""
The subtitles extracted will come from the first text track

If you want your subtitles to be extracted, put it in the
first text track, any other subtitles won't be extracted
"""

#imports

from json import loads
from pprint import pprint as p
from tkinter import Tk, filedialog
from time import sleep
from subprocess import Popen
from os import getenv

#timestamp generating function
def timestamp(t):
    t = t//1000
    milli = t%1000
    sec = (t//1000)%60
    mins = (t//60000)%60
    hrs = (t//3600000)%24
    return f"{hrs}:{mins:02}:{sec:02},{milli:03}"

print("Choose video project folder [popup coming]")
sleep(2)
root = Tk()
root.withdraw()
folder = filedialog.askdirectory(initialdir=getenv("localappdata")+"\\CapCut Drafts")

name = folder.split("/")[-1].lower().replace(" ", "_")

with open(folder+"/draft_content.json", encoding="utf-8") as f:
    cont = loads(f.read())
    texts = []
    #gets the first text track and extracts everything from it
    for m in cont["tracks"][::-1]:
        if m['type']=="text":
            texts.extend(m["segments"])
            break
    maps = {}
    for t in texts:
        maps[t["material_id"]] = (t["target_timerange"]["start"], t["target_timerange"]["start"] + t["target_timerange"]["duration"])
    subs = cont["materials"]["texts"]
    output = ""
    counter = 0
    for k in subs:
        if maps.get(k['id'], False):
            counter += 1
            output += f"{counter:03d}\n"
            times = maps[k["id"]]
            output += f"{timestamp(times[0])} --> {timestamp(times[1])}\n"+loads(k["content"])["text"]+"\n\n"
output = output[:-2]
with open(folder+"/"+name+".srt", "w", encoding="utf-8") as final_file:
    final_file.write(output)

import subprocess

def explorer_on_file(url):
    """ opens a windows explorer window """
    Popen(f'explorer /select,"{url}"')

explorer_on_file(folder.replace("/", "\\")+"\\"+name+".srt")
