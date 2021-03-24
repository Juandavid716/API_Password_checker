from app.database import create_connection
import app.main
from collections import Counter


def get_repeated(list_x):
    frequency={} 
    for i in list_x:
        frequency[i]=list_x.count(i)
    
    return  frequency

def update_4D_5D(list_s,  num, name_table, con, total, new_total):
    cur = con.cursor() 
    for key in list_s.keys():
    
        if num == 0:
            p = "["+','.join(str(v) for v in key)+"]"
        else:
            p = "".join(str(x) for x in key)
            ''.join(map(str,p))

        vals = cur.execute("SELECT probability FROM {} WHERE dimension=?".format(name_table), (p, )).fetchone()
        if vals:
            old_probability = vals[0]
      
            new_probability = float(old_probability)* total / (total + new_total) + float(list_s[key]) / (total + new_total)
           
            cur.execute(" UPDATE {} SET probability = ? WHERE dimension =?".format(name_table),(new_probability,p))
            print("omg")
            con.commit()
        else:
            new_probability = float(list_s[key]) / (total + new_total)
            print("done")
            cur.execute("INSERT OR IGNORE INTO {} (dimension, probability) VALUES (?, ?)".format(name_table),(p,new_probability))
            con.commit()

def update_dimensions(list_dimension, name_table, con ,total, new_total):
    cur = con.cursor() 
    for p in list_dimension:
        vals = cur.execute("SELECT probability FROM {} WHERE dimension=?".format(name_table), (p, )).fetchone()
        if vals:
            old_probability = vals[0]
            new_probability = float(old_probability)* total / (total + new_total) + float(list_dimension[p]) / (total + new_total)
            cur.execute(" UPDATE {} SET probability = ? WHERE dimension =?".format(name_table),(new_probability,p))
            con.commit()
            
        else:
            new_probability = float(list_dimension[p]) / (total + new_total)
            
            cur.execute("INSERT OR IGNORE INTO {} (dimension, probability) VALUES (?, ?)".format(name_table),(p,new_probability))
            con.commit()

def update_data(file, total):
    con = create_connection(r'./databases/test.db')
    cur = con.cursor() 

    data = main.get_list(file)
    new_total = len(data)
    list_prefix, list_without_prefix = main.get_prefix(data)
    print("done list prefix")
    list_suffix, list_baseword = main.get_suffix(list_without_prefix)
    print("done list suffix")
    list_shift = main.shift_pattern(list_baseword)
    print("done list shift")
    list_133t, list_baseword = main.get_133t_transformation(list_baseword)
    print("done listb")
    #Frequencies
    prefix = get_repeated(list_prefix)
    suffix = get_repeated(list_suffix)
    bw = get_repeated(list_baseword)
    shift= dict(Counter(tuple(x) for x in list_shift))
    t133 = dict(Counter(tuple(x) for x in list_133t))

    print("done frequencies")

    # Update each dimension with new probability, passing as parameters: original list, name table, connection, length of original dataset -> total, new_total = total + lenngth of new dataset
    update_dimensions(prefix, "prefix_table",con, total, new_total)
    update_dimensions(suffix, "suffix_table",con, total, new_total)
    update_dimensions(bw, "baseword_table",con, total, new_total)
    update_4D_5D(shift,0,"shift_table", con, total, new_total)   
    update_4D_5D(t133,1,"table_133t", con, total, new_total)
    


