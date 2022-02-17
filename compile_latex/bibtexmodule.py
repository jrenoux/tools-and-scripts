# -*- coding: utf-8 -*-
import sys
import codecs
import re

encoding = "ascii"

def ldist(a,b):
    m = len(a)
    n = len(b)
    d = []
    for i in range(m+1):
        r = [0]*(n+1)
        d.append(r)
        d[i][0] = i
    for j in range(0,n+1):
        d[0][j] = j

    for j in range(1,n+1):
        for i in range(1,m+1):
            if a[i-1] == b[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d_del = d[i-1][j] + 1
                d_ins = d[i][j-1] + 1
                d_sub = d[i-1][j-1] + 1
                d[i][j] = min(d_del, d_ins, d_sub)

    return d[m][n]

def splitEntries(s):
    entries = []
    current = None
    depth = 0
    for c in s:
        if current == None and c == "@":
            current = c
        elif current != None:
            current += c
            if c == "{":
                depth += 1
            if c == "}":
                depth -= 1
                if depth == 0:
                    entries.append(current)
                    current = None
    return entries

assert(ldist("ABC","ABC") == 0)
assert(ldist("ABC","ABCD") == 1)
assert(ldist("ABCD","ABC") == 1)
assert(ldist("kitten","sitting") == 3)
        
class BibtexEntry:
    def __init__(self,bibType,bibKey,bibMap):
        self.good_key_re = "[a-z\-]+[0-9]{4}[a-z][a-z\-]+"
        self.bibType = bibType
        self.bibKey = bibKey
        self.bibMap = bibMap
        if self.bibType.lower() == "@article":
            self.bibType = "@Article"
        elif self.bibType.lower() == "@inproceedings":
            self.bibType = "@InProceedings"
        elif self.bibType.lower() == "@incollection":
            self.bibType = "@InCollection"
        elif self.bibType.lower() == "@book":
            self.bibType = "@Book"
        elif self.bibType.lower() == "@phdthesis":
            self.bibType = "@PhdThesis"
        elif self.bibType.lower() == "@techreport":
            self.bibType = "@TechReport"
        elif self.bibType.lower() == "@proceedings":
            self.bibType = "@Proceedings"
        elif self.bibType.lower() == "@misc":
            self.bibType = "@Misc"
            

    def selfTest(self,additionalRequirements):
        numProblems = 0
        keyMatch = re.match(self.good_key_re, self.bibKey)
        if keyMatch == None:
            print(self.bibKey)
            numProblems += 1
            print("\tmalformed key")

        if self.bibType == "@Misc":
            if numProblems == 0:
                print(self.bibKey)
            numProblems += 1
            print("\tavoid misc type")
        
        requiredAtts = ["author", "year", "title"] + additionalRequirements

        if self.bibType == "Article":
            requiredAtts.append("journal")
            requiredAtts.append("volume")
        elif self.bibType == "InProceedings":
            requiredAtts.append("booktitle")
        elif self.bibType == "InCollection":
            requiredAtts.append("booktitle")
            requiredAtts.append("publisher")
        elif self.bibType == "Book":
            requiredAtts.append("publisher")
        elif self.bibType == "PhdThesis":
            requiredAtts.append("school")
        elif self.bibType == "TechReport":
            requiredAtts.append("institution")
        elif self.bibType == "Proceedings":
            requiredAtts.remove("author")

        for att in requiredAtts:
            if not att in self.bibMap:
                if numProblems == 0:
                    print(self.bibKey)
                numProblems += 1
                print("\tmissing " + att)
        # for att in self.bibMap:
        #     if not att in requiredAtts:
        #         print("Not required: %s" %(att))
        return numProblems
    
    def toString(self):
        remove = ["__markedentry", "file", "timestamp", "interhash", "intrahash"]
        priority = ["author", "title", "year", "journal", "booktitle", "pages"]
        s = "%s{%s,\n" %(self.bibType,self.bibKey)

        for key in priority:
            if key in self.bibMap.keys():
                line = "\t%s" %(key)
                while len(line) < 27:
                    line = line + " "
                line += "= {%s},\n" %(self.bibMap[key])
                s += line
        
        for key in self.bibMap.keys():
            if key not in priority and key not in remove:
                line = "\t%s" %(key)
                while len(line) < 27:
                    line = line + " "
                line += "= {%s},\n" %(self.bibMap[key])
                s += line
        s += "}"
        return s
       
class Library:
    def __init__(self):
        self.C = []

    def addEntry(self,e):
        self.C.append(e)

    def getAllEntries(self):
        return self.C

    def testAllEntries(self,additionalRequirements):
        numProblems = 0
        keyCounter = {}
        for e in self.C:
            if not e.bibKey in keyCounter.keys():
                keyCounter[e.bibKey] = 0
            keyCounter[e.bibKey] += 1
            numProblems += e.selfTest(additionalRequirements)
            if keyCounter[e.bibKey] == 2:
                print("Duplicate key: %s" %(e.bibKey))
                numProblems += 1
            if keyCounter[e.bibKey] >= 2:
                numProblems += 1
        print("Total number of issues found: %d" %(numProblems))
        return numProblems
        
    def getStats(self):
        years = []
        counter = {}
        for e in self.C:
            if "year" in e.bibMap.keys():
                y = e.bibMap["year"]
                if not y in years:
                    years.append(y)
                if not y in counter.keys():
                    counter[y] = 0
                counter[y] += 1
        years.sort()
        for y in years:
            print("%s: %d" %(y,counter[y]))

    def getAuthors(self):
        authorList = []
        for e in self.C:
            if "author" in e.bibMap.keys():
                authorStr = e.bibMap["author"].replace(str("\n".encode("utf-8"))," ").replace("\t"," ").replace("  "," ")
                authorStr = authorStr.replace("\\n"," ").replace("\\t"," ").replace("  "," ").replace("\\&","and").replace("\\\\","\\")
                for singleAuthor in authorStr.split(" and "):
                    if singleAuthor[0] == "{" and singleAuthor[-1] == "}" and not "\\" in singleAuthor:
                        singleAuthor = singleAuthor[1:-1]
                    if len(singleAuthor.split(",")) < 3:
                        singleAuthor = singleAuthor.strip()
                        if not singleAuthor in authorList:
                            authorList.append(singleAuthor)
                    else:
                        for singleAuthor2 in singleAuthor.split(","):
                            singleAuthor2 = singleAuthor2.strip()
                            if not singleAuthor2 in authorList:
                                authorList.append(singleAuthor2)
        authorList.sort()
        return authorList

    def getEntry(self,bibtexkey):
        for e in self.C:
            if e.bibKey == bibtexkey:
                return e
        return None

    def removeRedundantKeys(self):
        keys = []
        newC = []
        for e in self.C:
            if e.bibKey not in keys:
                keys.append(e.bibKey)
                newC.append(e)
        self.C = newC

    def saveToFile(self,fileName):
        sortable = []
        for e in self.C:
            sortable.append( (e.bibKey,e.toString()) )
        sortable.sort()
        
        f = open(fileName, "w")
        for pair in sortable:
            f.write(pair[1] +"\n")
        f.close()

    def loadFromFile(self,fileName):
        debug = False
        f = open(fileName, "r")#,encoding="utf-8")
        s = f.read()
        f.close()
        s = s.replace("\\\\","\\")

        for entry in splitEntries(s):
            entry = entry.strip()
            #print(entry)
            if entry != "" and not entry[0] == "%":
                #print(entry)
                bibType = entry.split("{")[0]
                bibKey = entry.split("{")[1].split(",")[0].strip()

        
                if debug:
                    print(bibType)
                    print(bibKey)
                
                entry = entry[len(bibType)+len(bibKey)+2:-1].strip()
                m = {}
                att = None
                val = None
                done = False
                startedWithQuotes = False
                depth = 0
                for c in entry:
                    if att == None and c not in [","]:
                        att = c
                    elif att != None and val == None:
                        if c != "=":
                            att += c
                        else:
                            if debug:
                                print("att:", att)
                            val = ""
                    elif val != None:
                        val += c
                        # Entry form: att = {val}
                        if c == "{":
                            depth += 1
                        elif c == "}":
                            depth -= 1
                            if depth == 0:
                                done = True
                        # Entry form: att = "val"
                        elif c == '"' and val.strip() == '"':
                            depth += 1
                            startedWithQuotes = True
                        elif c == '"' and depth == 1 and startedWithQuotes:
                            depth -= 1
                            done = True
                            startedWithQuotes = False
                        # Entry form: att = val
                        elif c == "," and depth == 0:
                            val = val[0:-1]
                            done = True
                    if done:
                        att = str(att.strip()).lower()
                        # att = str(att.strip().encode("utf-8"))[2:-1].strip().lower() 
                        # val = str(val.strip().encode("utf-8"))[2:-1].strip()[1:-1]
                        val = val.strip()
                        if val[0] == "{" or val [0] == '"':
                            val = str(val.strip()[1:-1])
                        val = val.replace("\\n","\n").replace("\\t","\t")
                        if att != "abstract":
                            val = val.replace("\n"," ").replace("  "," ")
                            while "  " in val:
                                val = val.replace("  "," ")
                        m[att] = val

                        if debug:
                            print("%s <- %s"%(att,val))
                        att = None
                        val = None
                        done = False
                        depth = 0
                        startedWithQuotes = False


                bibEntry = BibtexEntry(bibType,bibKey,m)
                if debug:
                    print(bibEntry.toString())
                    exit()
                self.addEntry(bibEntry)
