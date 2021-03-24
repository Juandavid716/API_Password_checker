from collections import Counter
from app.database import create_connection
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
    value = cur.execute(query).fetchone()
    
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
       baseword_transfomed, list_index = transform_133t(baseword)
       list_133t.append(list_index)
       list_new_basewords.append(baseword_transfomed.lower())
    return list_133t, list_new_basewords


def main(password):
    #Connection
    start = timeit.default_timer()
    con = create_connection(r'./app/databases/test.db')
    cur = con.cursor() 
    name_file = "./app/generated_pass.txt"
    # Hash section - check if a txt from passwords has been changed. If it has been changed, it's necessary to find again L1 and L2 values. 
    
    create_table_hash(con)

    #dataset
    list = get_list(name_file)
    length = len(list)
    length_hash_table = get_record(cur,"SELECT COUNT(*) FROM hash_table")
    last_record = get_record(cur,"SELECT * FROM hash_table ORDER BY ROWID DESC LIMIT 1")
    number_hash = get_hash(name_file)
    create_size(con,length)
    if length_hash_table == 0 or number_hash != last_record:
        
        #Create tables
        create_table("prefix_table", cur)
        create_table("suffix_table", cur)
        create_table("baseword_table", cur)
        create_table("shift_table", cur)
        create_table("table_133t", cur)
        
        print("Tables created")
        # Get lists
        
        list_prefix, list_without_prefix = get_prefix(list)
        print("prefix list created")
        list_suffix, list_baseword = get_suffix(list_without_prefix)
        print("suffix list created")
        list_shift = shift_pattern(list_baseword)
        print("shift list created")
        list_133t, list_baseword = get_133t_transformation(list_baseword)
        print("133t list created")

        # # 5D MODEL
        # print("Prefix list",list_prefix)
        # print("Base word list",list_baseword)
        # print("Suffix list", list_suffix)
        # print("shift pattern list", list_shift)
        # print("133t list",list_133t)

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
        cur.executemany("""INSERT INTO  prefix_table (dimension,probability) VALUES (?,?)""", zip(list_prefix,list_prob_prefix))
        cur.executemany("""INSERT INTO  suffix_table (dimension,probability) VALUES (?,?)""", zip(list_suffix,list_prob_suffix))
        cur.executemany("""INSERT INTO  baseword_table (dimension,probability) VALUES (?,?)""", zip(list_baseword,list_prob_basew))
        cur.executemany("""INSERT INTO  shift_table (dimension,probability) VALUES (?,?)""", zip(list_shift,list_prob_shift))
        cur.executemany("""INSERT INTO  table_133t (dimension,probability) VALUES (?,?)""", zip(list_133t,list_prob_133t))
        con.commit()

        print("insertions created")

    # Update section
    new_list = get_list("./app/passwords.txt")
    lg_new_list= len(new_list)


    if(lg_new_list>0):
        
        # get total size from original dataset.
        total = get_record(cur,"SELECT * FROM length_table ORDER BY ROWID DESC LIMIT 1")
        print(total)
        #Update the dataset
        update.update_data("./app/passwords.txt",total)

        #Update size 
        new_total = total + lg_new_list
        cur.execute("INSERT OR IGNORE INTO length_table (length_t) VALUES (?)",(new_total,))
        con.commit()
        # Delete all elements from file with new passwords
        file = open('./app/passwords.txt','w')
        file.close()
        


    # Get probabilities sorted by highest probability
    prefix_probabilities = cur.execute("SELECT * FROM prefix_table ORDER BY CAST(probability as FLOAT) DESC ").fetchall()
    suffix_probabilities = cur.execute("SELECT * FROM suffix_table ORDER BY CAST(probability as FLOAT) DESC ").fetchall()
    baseword_probabilities = cur.execute("SELECT * FROM baseword_table ORDER BY CAST(probability as FLOAT) DESC ").fetchall()
    shift_probabilities = cur.execute("SELECT * FROM shift_table ORDER BY CAST(probability as FLOAT)  DESC ").fetchall()
    t133_probabilities = cur.execute("SELECT * FROM table_133t ORDER BY CAST(probability as FLOAT)  DESC ").fetchall()

    print("probabilities calculated")
    
    P1 = get_probability_sorted(prefix_probabilities)
    P2 = get_probability_sorted(suffix_probabilities)
    P3 = get_probability_sorted(baseword_probabilities)
    P4 = get_probability_sorted(shift_probabilities)
    P5 = get_probability_sorted(t133_probabilities)

    print("Prob ordered")
    # P = List of lists 
    P = [P1,P2,P3,P4,P5]
    LP = [len(P1),len(P2),len(P3),len(P4),len(P5)]
    minimum = np.min(LP)
    dimensiones=5
    b= minimum.item()
    gamma= (b+1) / b
    p=P1[4]*P2[2]*P3[2]*P4[2]*P5[6]
    
    if length_hash_table == 0 or number_hash != last_record or lg_new_list>0:
        write_L1_L2(P,dimensiones, gamma,b,p )
        cur.execute('INSERT INTO hash_table VALUES(?)', [number_hash])
        con.commit()
    
    print("Reading L1 and L2 values ...")  
    L1, L2 = read_L1_L2()
    R = rank_estimation(L1,L2,password,con, b)

    if R == -5:
        print("None")
    elif R == 0:
        print("Equals to 0")
    else:
      numbits=np.ceil(np.log2(R))
      print("Bits number", numbits)
      print("With an enumeration of", int(2**(numbits)), " candidates passwords is possible to recover this password ")

    stop = timeit.default_timer()

    print('Time: ', stop - start)

    return int(2**(numbits))



if __name__ == "__main__":
    main()
    