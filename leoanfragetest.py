# -*- coding:cp1252 -*-
import re

def suche(suchwort):
    url = "https://dict.leo.org/dictQuery/m-vocab/ende/query.xml?search="
    #x = str(suchwort)
#    print(suchwort)
    suchwort = suchwort.replace(u'\xfc','ue')
    suchwort = suchwort.replace(u'\xf6','oe')
    suchwort = suchwort.replace(u'\xe4','ae')
    url2 = url + suchwort + "&api=uni-saarland22/1"
    print(url2)

    import urllib2
    response =  urllib2.urlopen(url2)
    html = response.read()
    with open("leoausgabe.txt","w") as f:
        f.write(str(html))

    with open("leoausgabe.txt","r") as g:
        counter = 0
        for line in g:
            #counter += 1
            p = re.search(r'<word>(.*?)</word>',line)
            if p:
                #print(p.groups(0)[0])
                return p.groups(0)[0]
            #result = p.groups(1)[0]

        #print(result)
        #return result.strip('"')




    
