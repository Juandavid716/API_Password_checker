from app.Esrank import main2

def keyBoard(word):
    for w in word:
        if not (w.isdigit() or w.isalpha() or isSymbol(w)):
            return False
    return True

def isSymbol(c):
    return (c in "!~@#$%^&*()_+?><.,;:'{}[]=-|\/ ") or (c=='"')

def isShifted(c):
    if c.isalpha():
        return c.isupper()
    return False

def unShiftLetter(c):
    if c.isalpha():
        return c.lower()

def unShiftWord(word):
    p=""
    lst=[]
    for i in range(len(word)):
        if isShifted(word[i]):
            p=p+unShiftLetter(word[i])
            if i>len(word)//2:
                lst.append(i-len(word))
            else:
                lst.append(i)
        else:
            p=p+word[i]
    return p,(str(lst))

def transform_133t(word):
    index_133t=[]
    if "0" in word:
        word=word.replace("0","o")
        index_133t.append(1)
    if "1" in word:
        word=word.replace("1","i")
        index_133t.append(12)
    elif "!" in word:
        word=word.replace("!","i")
        index_133t.append(13)
    if "@" in word:
        word=word.replace("@","a")
        index_133t.append(2)
    elif "4" in word:
        word=word.replace("4","a")
        index_133t.append(3)
    if "3" in word:
        word=word.replace("3","e")
        index_133t.append(6)
    if "$" in word:
        word=word.replace("$","s")
        index_133t.append(4)
    elif "5" in word:
        word=word.replace("5","s")
        index_133t.append(5)
    if "2" in word:
        word=word.replace("2","z")
        index_133t.append(11)
    if "%" in word:
        word=word.replace("%","x")
        index_133t.append(14)
    if "7" in word:
        word=word.replace("7","t")
        index_133t.append(10)
    elif "+" in word:
        word=word.replace("+","t")
        index_133t.append(9)
    if "9" in word:
        word=word.replace("9","g")
        index_133t.append(8)
    elif "6" in word:
        word=word.replace("6","g")
        index_133t.append(7)
    return word,str(list(sorted(index_133t)))

def condition(prob):
    
    if prob == None:
       result = 0
    else:
        result = prob[0]
    return result



def rank_estimation(L1, L2, password,con, b):
    cur = con.cursor() 
    
    first=True
    last=True
    f=len(password)
    l=-1
    if (password.isascii()): 
        for i in range(len(password)):
            if (not (password[i].isdigit() or isSymbol(password[i]) )) and (first==True):
                f=i
                first=False
            if (not (password[-(i+1)].isdigit() or  isSymbol(password[-(i+1)]))) and (last==True):
                l=-(i+1)
                last=False
        if f==len(password):
            p=password[0:f]
            maxProb=0
            for i in range(0,len(p)+1):
                for j in range(i,len(p)+1):
                    P1=p[:i]
                    unLeetP2=p[i:j]
                    P3=p[j:]
                    pp1_result=cur.execute("SELECT probability FROM prefix_table WHERE dimension = ?", (P1,)).fetchone()
                    pp2_result=cur.execute("SELECT probability FROM baseword_table WHERE dimension = ?", (unLeetP2,)).fetchone()
                    pp3_result=cur.execute("SELECT probability FROM suffix_table WHERE dimension = ?", (P3,)).fetchone()
                    pp1 = condition(pp1_result)
                    pp2 = condition(pp2_result)
                    pp3 = condition(pp3_result)
                
                    if (pp1!=None and pp2!=None and pp3!=None ):
                        if float(pp1)*float(pp2)*float(pp3)>maxProb:
                            maxProb=float(pp1)*float(pp2)*float(pp3)
                            print(maxProb)
                            
            pos1="[]"
            pos2="[]"
            if maxProb>0:
                pp4_result=cur.execute("SELECT probability FROM shift_table WHERE dimension = ?", (pos1,)).fetchone()
                pp5_result=cur.execute("SELECT probability FROM table_133t WHERE dimension = ?", (pos2,)).fetchone()

                pp4 = condition(pp4_result)
                
                pp5 = condition(pp5_result)
                prob=maxProb*float(pp4)*float(pp5)
                L=main2(L1,L2,prob,14)
                L=sum(L)/2
            else:
                L=-5
        else:
            if f!=0:
                P1=password[0:f]
                if l!=-1:
                    P2=password[f:l+1]
                    P3=password[l+1:]
                else:
                    P2=password[f:]
                    P3=""
            else:
                P1=""
                if l!=-1:
                    P2=password[f:l+1]
                    P3=password[l+1:]
                else:
                    P2=password[f:]
                    P3=""
            
            unShiftP2,pos1=unShiftWord(P2)
            unLeetP2,pos2=transform_133t(unShiftP2)
            pos1 = str(pos1).replace(' ','')
            
            pp1_result=cur.execute("SELECT probability FROM prefix_table WHERE dimension = ?", (P1,)).fetchone()
            pp2_result=cur.execute("SELECT probability FROM baseword_table WHERE dimension = ?", (unLeetP2,)).fetchone()
            pp3_result=cur.execute("SELECT probability FROM suffix_table WHERE dimension = ?", (P3,)).fetchone()
            pp4_result=cur.execute("SELECT probability FROM shift_table WHERE dimension = ?", (pos1,)).fetchone()
            pp5_result=cur.execute("SELECT probability FROM table_133t WHERE dimension = ?", (pos2,)).fetchone()
            pp1 = condition(pp1_result)
            pp2 = condition(pp2_result)
            pp3 = condition(pp3_result)
            pp4 = condition(pp4_result)
            pp5 = condition(pp5_result)
          

            if (pp1!=None and pp2!=None and pp3!=None and pp4!=None and pp5!=None):
                prob=float(pp1)*float(pp2)*float(pp3)*float(pp4)*float(pp5)
               
                L=main2(L1,L2,prob,b)
             
                L=sum(L)/2
                
            else:
                L=-5

    return L