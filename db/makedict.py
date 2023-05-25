#!/usr/bin/python

import requests

def goforward(s, i, text):
    for k in range(i+1, len(text) - len(s) - 1):
        if text[k:k+len(s)] == s:
            return k
    return -1

# feed in a saved html page of the results from https://www.fernbahn.de/datenbank/suche/
# searching for type ICE and the current year
def get_allnumbers():
    with open("liste23.html", "r") as file:
        liste = file.read()
    p = 0
    nrs = []
    while p != -1:
        p = goforward("ICE<", p, liste)
        if p == -1:break
        p = goforward("<td", p, liste)
        if p == -1:break
        p = goforward(">", p, liste)
        if p == -1:break
        p2 = goforward("<", p, liste)
        if p2 == -1:break
        nrs.append(int(liste[p+1:p2]))
    return nrs
    

alldict = {}
allnumbers = get_allnumbers() # list(range(1, 1732)) + [1980, 9510] + list(range(9550, 9599)) + list(range(52980, 52991))

for i in range(100000): # avoid doubles found in allnumbers
    if i not in allnumbers:
        continue
    
    nr = str(i)
    k = 0
    i_done = 0
    while i_done < allnumbers.count(i):
        if k == 15: # irgendwann reichts
            print(f"nothing found for {i}")
            break
        k += 1
        zugid = "20230" + str(k) + "00000"[:-len(nr)] + nr; # Jahr+01+Zugnummer(5 stell.)
        db_url = "https://www.fernbahn.de/datenbank/suche/?zug_id=" + zugid;

        geterror = 1
        while geterror:
            try:
                contents = requests.get(db_url).content.decode('utf-8')
                geterror = 0
            except:
                print("error while getting data")
                time.sleep(0.3)
        if "Es konnten keine Datensätze mit Ihren Suchparametern gefunden werden." in contents:
            print(f"     no search results for {zugid}")
            continue

        off = goforward("ICE-Typ", 0, contents)
        typoff = goforward("ICE", off, contents)
        typend = goforward("<", typoff, contents)
        if off == -1 or typoff == -1 or typend == -1:
            print(f"     could not find type ({zugid})")
            continue
        typ = contents[typoff:typend]
        if i not in alldict:
            alldict[i] = typ
            print(f"{nr}.{k}\t{typ}")
        else:
            alldict[i] += ";\n" + typ
            print(" " * len(nr) + f".{k}\t{typ}")
        i_done += 1

with open("icedict23.txt", "w") as file:
    file.write(alldict.__repr__())
