
from collections import Counter
from app.settings import create_connection
from app.create_tables import create_table
from app.create_tables import create_table_hash
from app.create_tables import create_size
from app.Esrank import get_L1_L2
from app.hash import get_hash
from app.rank import transform_133t
from app.rank import rank_estimation
import app.update
import numpy as np 
import copy
import ast 
import timeit

def  write_L1_L2(P,dimensiones, gamma,b,p ):
    L1, L2 = get_L1_L2(P,dimensiones, gamma,b,p )
    f=open("./app/training.txt","w")
    f.write(str(L1)+"\n")
    f.write(str(L2))
    f.close()

def read_L1_L2():
    data = []
    with open("./app/training.txt") as fname:
        lines = fname.readlines()
        for line in lines:
            data.append(line.strip('\n'))
    res = ast.literal_eval(data[0]) 
    res2 = ast.literal_eval(data[1]) 
    return res,res2
    
def get_record(cur,query):
    cur.execute(query)
    value = cur.fetchone()
    
    if value == None:
        value = 0
    else:
        value = value[0]
    return value

# Get the list of passwords from the file
def get_list(name_file):
 data = []
 with open(name_file) as fname:
    lines = fname.readlines()
    for line in lines:
        data.append(line.strip('\n'))
 return data

# Get the prefix for each password and return two list: List of prefix and list of password without prefix
def get_prefix(password_list):
    list_prefix = []
    list_password_without_prefix = []
    for password in password_list:
        prefix = ""
        for letter in password:
            if letter.isalpha() is False:
              prefix = prefix + letter
            else:
              break

        if prefix == password:
            prefix = ""
        #print("Password is {} and prefix is {}".format(password,prefix))

        password_without_prefix = password[ len(prefix) : len(password)]
        list_password_without_prefix.append(password_without_prefix)
        list_prefix.append(prefix)
    
    return list_prefix, list_password_without_prefix;

# Get the suffix for each password and return two list: List of suffix and list of basewords
def get_suffix(password_list):
    list_suffix = []
    list_baseword = []
    for password in password_list:
        suffix = ""
        password_reverse = password[::-1]
     
        for letter in password_reverse:
            if letter.isalpha() is False:
              suffix = suffix + letter
            else:
              break
               
        if suffix == password_reverse:
            suffix = ""
        
        suffix_reverse = suffix[::-1]
        #print("Password is {} and suffix is {}".format(password,suffix))
        password_without_suffix = password[ 0 : len(password)-len(suffix_reverse)]
        list_baseword.append(password_without_suffix)
        list_suffix.append(suffix_reverse)
    
    return list_suffix, list_baseword;

# Get shift pattern from basewords
def shift_pattern(baseword_list):
    list_shift = []
    for baseword in baseword_list:
        shift = []
        shift_negative = []
        cont = -1
        cont_r = -1
        length = len(baseword)
        for index in range(0, length):
           letter = baseword[index]
           
           if letter.isupper(): 
             if index < length // 2:
                shift.append(index)
             else:
                 shift.append(index-length)
                 cont_r -= 1
                 
        list_shift.append(shift)

    return list_shift

# Get probability from lists of dimensions (prefix, baseword, suffix)
def get_probability(frequency,length):
    list_probabilities = []

    for index in frequency:
        result = frequency[index] / length
        list_probabilities.append(result)

    return list_probabilities

#Get probability order by desc
def get_probability_sorted(name_list):
    list = []
    for row in name_list:
        list.append(float(row[1]))
    
    return list


# Count every time an element appear

def get_frequency(list, length):
    frequency={} 
    dimensions = []

    # Count number of times that a prefix is repeated
    for i in list:
        frequency[i]=list.count(i)
    
    
    for key in frequency.keys():
        dimensions.append(key)

    return dimensions, get_probability(frequency, length)

#Get probability from lists shift pattern dimension
def get_frequency_shift(list_s, length, num):
    list_probabilities = []
    list_copy = dict(Counter(tuple(x) for x in list_s))
    dimensions = []

    for key in list_copy.keys():

        if num == 0:
            values = "["+','.join(str(v) for v in key)+"]"
        else:
            values = "".join(str(x) for x in key)
            ''.join(map(str,values))
        dimensions.append(values)

    return dimensions, get_probability(list_copy,length)



# Get basewords and 133_t transformations
def get_133t_transformation(list_baseword):
    list_133t = []
    list_new_basewords = []
    for baseword in list_baseword:
       if baseword.isnumeric() is True:
           baseword_transfomed = baseword
           list_index = "[]"
       else:
        baseword_transfomed, list_index = transform_133t(baseword)
       list_133t.append(list_index)
       list_new_basewords.append(baseword_transfomed.lower())
    return list_133t, list_new_basewords

def getEnumerationTime(numbits):
 intelIPC = int(2**(30))*109
 numbits = int(2**(numbits))

 res = numbits / intelIPC
 # dias
 if(res >= 31536000):
   res = res/ 31536000
   res = round(res,0) 
   res = str(res) + " a??os"
 elif(res >= 86400):
   res = res / 86400
   res = round(res,0) 
   res = str(res) + " d??as"
 elif (res > 3600):
   res = res / 3600
   res = round(res,0) 
   res = str(res) + " horas"
 elif (res > 60):
   res = res / 60
   res = round(res,0) 
   res = str(res) + " minutos"
 else:
   res = round(res,4) 
   res = str(res) + " segundos"
 return res 



def main(password):
    #Connection
    start = timeit.default_timer()
    con = create_connection()
    cur = con.cursor() 
    name_file = "./app/xd.txt"
    number_hash = get_hash(name_file)
    # Hash section - check if a txt from passwords has been changed. If it has been changed, it's necessary to find again L1 and L2 values. 

    # Environment variable -> Decide to execute the algorithm in developemnt or production mode.
    ENV="PROD"

    if ENV=="DEV":
        create_table_hash(con)

        #dataset
        list = get_list(name_file)
        length = len(list)
        length_hash_table = get_record(cur,"SELECT COUNT(*) FROM hash_table")
        
        last_record = get_record(cur,"SELECT hash_t FROM hash_table ORDER BY id DESC LIMIT 1")
        
        create_size(con,length)
        if length_hash_table == 0 or number_hash != last_record:
            
            #Create tables
            create_table("prefix_table", con)
            create_table("suffix_table", con)
            create_table("baseword_table", con)
            create_table("shift_table", con)
            create_table("table_133t", con)
            
            print("Tables created")
            # Get lists
            
            list_prefix, list_without_prefix = get_prefix(list)
            print("prefix list created")
            list_suffix, list_baseword = get_suffix(list_without_prefix)
            print("suffix list created")
            list_shift = shift_pattern(list_baseword)
            print("shift list created")
            list_133t, list_baseword = get_133t_transformation(list_baseword)
            print(list_baseword)
            print("133t list created")

            # List of probabilities
            list_prefix, list_prob_prefix =  get_frequency(list_prefix, length)
            print("prefix prob created")
            list_baseword, list_prob_basew = get_frequency(list_baseword, length)
            print("prefix base created")
            list_suffix, list_prob_suffix= get_frequency(list_suffix, length)
            print("prefix suf created")
            list_shift, list_prob_shift = get_frequency_shift(list_shift, length,0)
            print("prefix shift created")
            list_133t, list_prob_133t =  get_frequency_shift(list_133t, length,1)
            print("prefix 133t created")
            
            # Insertions list on database 
            cur.executemany("""INSERT INTO  prefix_table (dimension,probability)  VALUES (%s, %s)""", zip(list_prefix,list_prob_prefix))
            cur.executemany("""INSERT INTO  suffix_table (dimension,probability) VALUES (%s, %s)""", zip(list_suffix,list_prob_suffix))
            cur.executemany("""INSERT INTO  baseword_table (dimension,probability) VALUES (%s, %s)""", zip(list_baseword,list_prob_basew))
            cur.executemany("""INSERT INTO  shift_table (dimension,probability) VALUES (%s, %s)""", zip(list_shift,list_prob_shift))
            cur.executemany("""INSERT INTO  table_133t (dimension,probability) VALUES (%s, %s)""", zip(list_133t,list_prob_133t))
            con.commit()

            print("insertions created")

        
            
    # Update section
    name_update = "./app/passwords.txt"
    new_list = get_list(name_update)
    lg_new_list= len(new_list)


    if(lg_new_list>0):
            
            # get total size from original dataset.
            total = get_record(cur,"SELECT * FROM length_table ORDER BY length_t DESC LIMIT 1")
            #Update the dataset
            app.update.update_data(name_update,total)

            #Update size 
            new_total = total + lg_new_list
            cur.execute("INSERT  INTO length_table (length_t) VALUES ({}) ON CONFLICT (length_t) DO NOTHING".format(new_total))
            con.commit()
            # Delete all elements from file with new passwords
            file = open(name_update,'w')
            file.close()

    # Get probabilities sorted by highest probability (DEV)
    # cur.execute("SELECT * FROM prefix_table ORDER BY CAST(probability as FLOAT) DESC ")
    # prefix_probabilities = cur.fetchall() 
    # cur.execute("SELECT * FROM suffix_table ORDER BY CAST(probability as FLOAT) DESC ")
    # suffix_probabilities = cur.fetchall() 
    # cur.execute("SELECT * FROM baseword_table ORDER BY CAST(probability as FLOAT) DESC ")
    # baseword_probabilities = cur.fetchall() 
    # cur.execute("SELECT * FROM shift_table ORDER BY CAST(probability as FLOAT)  DESC ")
    # shift_probabilities =  cur.fetchall() 
    # cur.execute("SELECT * FROM table_133t ORDER BY CAST(probability as FLOAT)  DESC ")
    # t133_probabilities =  cur.fetchall() 

    # Get probabilities sorted by highest probability (PROD)
    cur.execute("SELECT COUNT(*) FROM prefix_table")
    P1 = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM suffix_table")
    P2 = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM baseword_table")
    P3 = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM shift_table")
    P4 = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM table_133t")
    P5 = cur.fetchone()[0]
   
    print("probabilities calculated")
        
    # P1 = get_probability_sorted(prefix_probabilities)
    # P2 = get_probability_sorted(suffix_probabilities)
    # P3 = get_probability_sorted(baseword_probabilities)
    # P4 = get_probability_sorted(shift_probabilities)
    # P5 = get_probability_sorted(t133_probabilities)


    print("Prob ordered")
    dimensiones=5
    #P = [P1, P2, P3, P4, P5]
    LP = [P1,P2,P3,P4,P5]
    minimum = np.min(LP)
    b= minimum.item()
    gamma= (b+1) / b
    #p=P1[4]*P2[2]*P3[2]*P4[2]*P5[1]

    #Dev Section
    if ENV=="DEV":
        write_L1_L2(P,dimensiones, gamma,b,p )
    else:
        if lg_new_list>0:
            write_L1_L2(P,dimensiones, gamma,b,p )
            cur.execute("""INSERT INTO hash_table(hash_t) VALUES (%(player)s)""", {'player': number_hash })
            con.commit()
        
    print("Reading L1 and L2 values ...")  
    L1, L2 = read_L1_L2()
    R = rank_estimation(L1,L2,password,con, b)
    numbits=0
    if R == -5:
        print("None")
                  
        numbits = 20
       
    elif R == 0:
        print("Equals to 0")
    else:
        numbits=np.ceil(np.log2(R))
        print("Bits number", numbits)
        
    value = numbits
    numbits = int(2**(numbits))
    stop = timeit.default_timer()

    time = stop - start
    print('Time: ', time)
    
    enumeration = getEnumerationTime(value)
    if(numbits <= 1073741824):
        message =u'La contrase??a es muy d??bil',"1", enumeration
      
        return message
    elif numbits > 1073741824 and numbits <= 1099511627776:
        return u"La contrase??a es d??bil", "2" , enumeration
    elif numbits > 1099511627776 and numbits <= 1152921504606846976:
        return "La contrase??a es aceptable", "3", enumeration
    elif numbits > 1152921504606846976 and numbits <= 1180591620717411303424:
        return "La contrase??a es segura", "4" , enumeration
    else:
        return "La contrase??a es muy segura", "5", enumeration
    
    
    



if __name__ == "__main__":
    main()
    