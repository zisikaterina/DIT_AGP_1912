import os
import re
from time import time
import sys
import termcolor as tm
parentroot = 'oop-master'

def file_parser():
    starttime = time()
    print(os.getcwd())
    files=[]
    try:
        for path,_,file in os.walk(parentroot,topdown=True):
            files+=[path+'/'+l for l in file if l.endswith('.cpp') or l.endswith('.c') or l.endswith('.hpp') or l.endswith('.h')]
    except Exception:
        print('Can not open folder oop-master')
        files=list([])
        print('Elapsed time for file opening:'+str((time()-starttime)+' s'))
    return files

files=file_parser()


def filesbycategory():
    counter={'cpp': 0, 'hpp': 0, 'h': 0, 'c': 0}
    starttime=time()
    for x in files:
        if re.match('.+\.cpp', x):
            counter['cpp'] += 1
        elif x.endswith('.+\.hpp'):
            counter['hpp'] += 1
        elif x.endswith('.+\.h'):
            counter['h'] += 1
        else:
            counter['c'] += 1

    for key in counter:
        print(str(key)+'-->'+str(counter[key]))
    endtime=time()
    print('Lapsed Time:'+str(endtime-starttime)+' s')

def codelines():
    starttime=time()
    linecounter=0
    for i in files:
        with open(i,'r',encoding="utf-8",errors='ignore') as f:
            for j in f:
                if len(j.strip())!=0:
                    linecounter+=1
    tm.cprint('Lines of code:'+str(linecounter),'blue')
    tm.cprint('Elapsed Time for finding all lines of code:'+str(time()-starttime)+'\'s','yellow')

def Symbols_letters_Digits():
    parser={'characters':0,'digits':0,'symbols':0}
    patternC=re.compile('[A-Za-z]')
    patternD=re.compile('\d')
    patternS=re.compile('\W')
    if len(files)==0:
        print('No input Data!!!Please Check you file Data')
        return

    start_time=time()

    for x in files:
      with open(x,'r',encoding="utf-8",errors='ignore') as f: 
        for k in f:
            chars=len(patternC.findall(k))
            digits=len(patternD.findall(k))
            symbols=len(patternS.findall(k))
            parser['characters']+=chars
            parser['digits']+=digits
            parser['symbols']+=len(k)-(chars+digits)
    end_time=time()
    for x in parser:
        tm.cprint(f'{x}-->{parser[x]}','yellow')
    tm.cprint('=='*30,'blue')
    tm.cprint(f'Lapsed Time:{end_time-start_time} \'s','blue')
     
def equality_statements():
    starttime=time()
    counter=0
    fls=[]
    pattern=re.compile('\s+if\s*\(\s*.+\s*==\s*.+\)|^if\s*\(.+==.+\)|\s*if\s*\(\s*\w+\s*\)|if\s*\(\s*(\w|\d)+\s*\)')
    for x in files:
        with open(x,'r',encoding='utf-8',errors='ignore') as f:
            counter+=len([m for m in f if(re.match('.*if(.+==.+).*',m))])
            for k in f:
                fls+=pattern.findall(k)
    tm.cprint('Elapsed Time for finding all equality statements :'+str(time()-starttime)+'\'s','yellow')
    tm.cprint('=='*20,'yellow')
    return len(fls)

def over_12_characters():
    starttime=time()
    found=0
    pattern=re.compile('(\s*for\s*\(.+[;].+[;].+\)|\s*for\s*\(.+[:].+\)')
    for x in files:
            with open(x,'r',encoding='ISO-8859-9') as f:
               for m in f:
                   for m in [l for l in pattern.findall(m)]:
                       word=m.strip().replace(' ','')
                       word=word[4:len(word)-1]
                       word.replace(':','').replace(';','')
                       if len(word)>=12:
                           found+=1
                return found
    tm.cprint('Elapsed Time for finding for loops over 12 characters:'+str(time()-starttime)+'\'s','yellow')                     
    print(f'Total for loops with over 12 characters:{found}')
    tm.cprint('=='*20,'yellow')

def CommonVars():
    starttime=time()
    commonvars=dict({})
    unacceptable=re.compile('((const|static|static\sconst)\s+int\s+\w+\s*[=]\s*\w+\s*[;])')
    pattern=re.compile('\s*int\s+\w+[;]')
    patternA=re.compile('(\s*int\s+\w+([,]\w+)*[;])')
    patternB=re.compile('(\s*int\s+\w+([=]\w+)+[;])')
    patternC=re.compile('(\s*int\s+\w+\s*[=]\s*\w+\s*([,]\s*\w+\s*[=]\s*\w+\s*)+[;])')

    matches=[]
    for x in files:
        with open(x,'r',encoding='utf8',errors='ignore') as f:
            lines=f.readlines()
            for k in lines:
                word=k
                if word.startswith('//') or word.startswith('#'):
                    continue

                for l in unacceptable.finditer(k):
                    word=k[0:l.start()]+k[l.end():]


                for n1 in pattern.findall(word):
                   if len(n1)==0: continue
                   word=n1.replace(';','').strip()
                   spdat=re.split('\s',word)
                   if spdat[1] in commonvars:
                       commonvars[spdat[1]]+=1
                   else:
                       commonvars.update({spdat[1]:1})
                for n2 in [l[0] for l in patternA.findall(word)]:
                    word=n2.replace(';',' ').strip()
                    data2=re.split('[,\s]',word)
                    for j in data2:
                        if j.strip()=='int': 
                            continue
                        if j.strip() in commonvars:
                           commonvars[j.strip()]+=1
                        else:
                           commonvars.update({j.strip():1}) 
                for n3 in [l[0] for l in patternB.findall(word)]:
                    word=n3.strip().replace(';','')
                    data3=[x for x in re.split('[\s=]',word) if x.strip()!=';' and re.search('^\s+$',x)==None]
                    counter=0
                    for j in data3:
                       counter+=1
                       if len(data3)==int(counter):
                            continue
                       if j.strip()=='int':
                           continue
                       if j.strip() in commonvars:
                           commonvars[j.strip()]+=1
                       else:
                           commonvars.update({j.strip():1})

                for n4 in [l[0] for l in patternC.findall(k)]:
                    word=n4.strip().replace(';','')
                    
                    data4=[x.replace(' ','') for x in word.split(',')]
                    for j in data4:
                        checkstr1=word.split('=')[0]
                        checkstr=checkstr1.split(' ')[1]
                        if checkstr in commonvars:
                            commonvars[checkstr]+=1
                        else:
                            commonvars.update({checkstr:1})

    tm.cprint('Elapsed Time for finding common variables:'+str(time()-starttime)+'\'s','yellow')                
    tops=sorted(commonvars.items(),key=lambda elem:elem[1])
    print(commonvars['j'])
    for i in range(len(tops)-1,len(tops)-4,-1):
        print(f'{tops[i][0]}-->{tops[i][1]}')

def main():
 file_parser()
 print(len(files))
 filesbycategory()
 codelines()
 Symbols_letters_Digits()
 print(f'Equality Statements={equality_statements()}')
 over_12_characters()
 CommonVars()


main()



