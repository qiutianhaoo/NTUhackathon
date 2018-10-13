import csv, io

def load(string, system):
    if string == "":
        return ""
    result = ""
    tempsys = decompose_system(system)
    for i in string:
        if i in tempsys:
            result += i
    result = parse(result, system)
    return result

def decompose_system(system):
    lst = []
    for i in system:
        for j in i:
            if j not in lst:
                lst.append(j)
    return lst

def parse(string, system):
    result = []
    while len(string) > 1:
        i = 0
        symb = string[i]
        new = list(filter(lambda x: x[0] == symb, system))
        while len(new) > 1:
            i += 1
            symb += string[i]
            new = list(filter(lambda x: x[:len(symb) + 1] == symb, system))
        if len(new) == 1:
            result.append(new[0])
            string = string[len(new[0]):]
        elif len(new) == 0:
            result.append(symb[:-1])
            string = string[len(symb[:-1]):]
    if string:
        result.append(string)
    return result

def read_csv(fname):
    new = []
    with open(fname, encoding = 'utf-8') as f:
        for row in csv.reader(f):
            new.append(row)
    return new

def make_letter_key_dic(src):
    dic = {}
    for i in range(len(src)):
        dic[src[i]] = i
    return dic

table = read_csv("data/Phonetic_notation_2.csv")[1:]

def transcribe(word, src, dst, *pool):
    if len(pool) == 0:
        pool = make_letter_key_dic(list(map(lambda x: x[src], table)))
    else:
        pool = pool[0]
    lst = load(word,pool)
    dic = {}
    for i in range(len(table)):
        dic[i] = table[i]
    lst = list(map(lambda x: dic[pool[x]][dst], lst))
    result = ""
    for i in lst:
        result += i
    return result

#src, dts key: 0 = uk, 1 = us, 2 = klattese, 3 = sampa, 4 = arpabet\

#eg transcribe_all("UK_IPA.csv", 0, 2, "Klattese.csv") will transcribe UK IPA entries in a single column
# file in the same folder into Klattese entries to another file "Klattese.csv".
# do transcribe_all("ELP.csv", 3, 0, "ELP_IPA.csv")

# will print out and skip words that cannot be transcribed because input is invalid

#transcribe_all("Words_IPA.csv", 0, 2, "Words_Klattese.csv")
#transcribe_all("Nonwords_IPA.csv", 0, 2, "Nonwords_Klattese.csv")

def transcribe_all(fname, src, dst, output_name):
    pool = make_letter_key_dic(list(map(lambda x: x[src], table)))
    file = read_csv(fname)
    result = []
    for i in file:
        if len(i) == 0:
            w = ""
            result.append([w])
            continue
        if i[0] == "NULL":
            w = ""
            result.append([w])
            continue
        try:
            w = transcribe(i[0], src, dst, pool)
        except:
            print(i[0])
        result.append([w])
    ofile = io.open(output_name,'w', newline='',encoding='utf-32')
    with ofile:
        writer = csv.writer(ofile, delimiter = ",")
        writer.writerows(result)
    ofile.close()

def nphon(fname, outfile):
    words = read_csv(fname)
    key = table
    pool = make_letter_key_dic(list(map(lambda x: x[0], key)))
    output = []
    for i in words:
        line = [i[0], len(load(i[0], pool))]
        output.append(line)
    ofile = io.open(outfile, 'w', newline='',encoding='utf-32')
    with ofile:
        writer = csv.writer(ofile, delimiter = ",")
        writer.writerows(output)
    ofile.close()

def count_symbol(symb):
    words = read_csv("Klattese.csv")
    key = table
    pool = make_letter_key_dic(list(map(lambda x: x[2], key)))
    count = 0
    for i in words:
        if len(i) == 0:
            continue
        w = load(i[0], pool)
        count += w.count(symb)
    return count
