# -*- coding: utf-8 -*-
import sys
import codecs
import glob
import os

from bibtexmodule import BibtexEntry
from bibtexmodule import Library

if len(sys.argv) < 3:
    print("Requires 2 arguments: Master .bib file and target .bib file.")
    exit(1)

masterBibFile = sys.argv[1]
workingBibFile = sys.argv[2]

print("Fetching references master bibliography...")
lib = Library()
lib.loadFromFile(masterBibFile)

print("Fetching references from working bibliographies...")
localLib = Library()
for fName in glob.glob("./*.bib", recursive=True):
    print("Loading local: " + fName)
    localLib.loadFromFile(fName)

#Initialize the keys with existing keys in current local bib file
keys = []    
for entry in localLib.getAllEntries():
    keys.append(entry.bibKey)

entries = []
newEntries = []
os.chdir("./")

print("Fetching missing references...")
files = glob.glob('./*.tex', recursive=True)

print(keys)

print(files)
for fName in files:
    f = open(fName,"r")
    s = f.read()
    citeStyles = ["\\cite{","\\citep{","\\citet{", "\\textcite{"]
    for style in citeStyles:
        for tmp in s.split(style)[1:]:
            for key in tmp.split("}")[0].split(","):
                key = key.strip()
                if not key in keys:
                    keys.append(key)
                    e = lib.getEntry(key)
                    if e != None:
                        entries.append(e)
                    else:
                        eLocal = localLib.getEntry(key)
                        if eLocal != None:
                            newEntries.append(eLocal)
                        else:
                            print("Key not found: %s (in master or local bib files)" %(key))
    f.close()

if entries:
    print("Appending new references to local file (%s)" %(workingBibFile))
    f = open(workingBibFile,"a")
    for e in entries:
        f.write(e.toString() +"\n")
    f.close()

if newEntries:
    print("Collecting references missing from master in missing-from-master.bib...")
    f = open("missing-from-master.bib","w")
    for e in newEntries:
        f.write(e.toString() +"\n")
    f.close()

print("All done!")
    

    
