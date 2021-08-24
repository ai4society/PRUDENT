import pandas as pd 
import streamlit
import pandas as pd 
import numpy as np
import pickle as pkl
import nltk
nltk.download('punkt')
import random
from collections import defaultdict

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

gloabl_df = pd.read_csv('./data/unspsc_dataset.csv')

#added RL Epsilon Decay (Random selection)

def extract_query(query, dir_df, dir_name):
    if dir_name == 'unspsc':
        dir_df = pd.read_csv("./data/unspsc_dataset.csv")
        c1 = " ".join(dir_df['Commodity Title'].values.tolist())
        c2 = " ".join(dir_df['Family Title'].values.tolist())
        c3 = " ".join(dir_df['Class Title'].values.tolist())
        c4 = " ".join(dir_df['Segment Title'].values.tolist())
        c5 = "" + c1 +" "+ c2 +" "+ c3 +" "+ c4
        temp = nltk.word_tokenize(c5)
        temp = [word.lower() for word in temp if len(word)>2 and word!= 'and' and word!='other']
        temp = " ".join(temp)

    elif dir_name == 'icd10':
        dir_df = pkl.load(open("./data/icd10_dict1.pkl","rb"))
        check  = ""
        for i in dir_df.keys():
            check = check + i + " "
            temp = dir_df[i][1]
            try:
                temp.keys()
                for j in temp.keys():
                    check = check + j + " "
                    temp2 = dir_df[i][1][j][1]
                    try:
                        temp2.keys()
                        for k in temp2.keys():
                            check = check + k + " "
                            temp3 = dir_df[i][1][j][1][k][1]
                            try:
                                temp3.keys()
                                for l in temp3.keys():
                                    check = check + l + " "
                            except AttributeError:
                                check = check + temp3 + " "
                                continue
                    except AttributeError:
                        check = check + temp2 + " "
                        continue
            except AttributeError:
                check = check + temp + " "
                continue
        
        temp = nltk.word_tokenize(check)
        temp = [word.lower() for word in temp if len(word)>2 and word!= 'and' and word!='other']
        temp = " ".join(temp)
    
    tkquery = nltk.word_tokenize(query)
    tkquery = [i.lower() for i in tkquery if i!='want' and i!='query' and i!='code' and i!='the' and i!='about' and i!='code' and i!='tell' and i!='for'and i!='more' and len(i)>2 and i!='info' and i!= 'and' and i!= 'other'and i!='know' and i!='information']
    tkquery = list(set(tkquery))
    match = list()
    for i in tkquery:
        if(temp.lower().count(i.lower())>0):
            match.append(i.lower())
    send = list()
    for i in nltk.word_tokenize(query):
        if(i.lower() in match):
            send.append(i.lower())
    if(len(send)>1):
        return " ".join(send)
    elif(len(send)==1):
        return send[0]
    else:
        return ""

def match_score( query, dir_df, dir_name):
    if dir_name == 'unspsc':

        c1 = " ".join(dir_df['Commodity Title'].values.tolist())
        c2 = " ".join(dir_df['Family Title'].values.tolist())
        c3 = " ".join(dir_df['Class Title'].values.tolist())
        c4 = " ".join(dir_df['Segment Title'].values.tolist())
        c5 = "" + c1 +" "+ c2 +" "+ c3 +" "+ c4
        temp = nltk.word_tokenize(c5)
        temp = [word.lower() for word in temp if len(word)>2 and word!= 'and' and word!='other']
        temp = " ".join(temp)

    elif dir_name == 'icd10':

        check  = ""
        for i in dir_df.keys():
            check = check + i + " "
            temp = dir_df[i][1]
            try:
                temp.keys()
                for j in temp.keys():
                    check = check + j + " "
                    temp2 = dir_df[i][1][j][1]
                    try:
                        temp2.keys()
                        for k in temp2.keys():
                            check = check + k + " "
                            temp3 = dir_df[i][1][j][1][k][1]
                            try:
                                temp3.keys()
                                for l in temp3.keys():
                                    check = check + l + " "
                            except AttributeError:
                                check = check + temp3 + " "
                                continue
                    except AttributeError:
                        check = check + temp2 + " "
                        continue
            except AttributeError:
                check = check + temp + " "
                continue
        
        temp = nltk.word_tokenize(check)
        temp = [word.lower() for word in temp if len(word)>2 and word!= 'and' and word!='other']
        temp = " ".join(temp)
    
    tkquery = nltk.word_tokenize(query)
    tkquery = [i.lower() for i in tkquery if i!='want' and i!='query' and i!='code' and i!='the' and i!='about' and i!='code' and i!='tell' and i!='for'and i!='more' and len(i)>2 and i!='info' and i!= 'and' and i!= 'other'and i!='know' and i!='information']
    score = 0
    tkquery = list(set(tkquery))
    match = list()
    for i in tkquery:
        if(temp.lower().count(i.lower())>0):
            score = score + 1
            match.append(i.lower())
    send = list()
    if(dir_name=='unspsc'):
        for i in nltk.word_tokenize(query):
            if(i.lower() in match):
                send.append(i.lower())
        if(len(send)>1):
            return score, " ".join(send)
        elif(len(send)==1):
            return score, send[0]
        else:
            return score, ""
    elif(dir_name == 'icd10'):
        #return score, query.lower().replace("i want the code for ","")
        return score, " ".join(tkquery)

def query_dirFinder( query):
    dir_df1 = pd.read_csv("./data/unspsc_dataset.csv")
    check1, q1 = match_score( query, dir_df1,'unspsc')
    dir_df2 = pkl.load(open("./data/icd10_dict1.pkl","rb"))
    check2, q2 = match_score( query, dir_df2,'icd10')
    #print(check1, check2)
    #raise KeyboardInterrupt
    q = ""
    if(check1>0 and check2>0 and check1==check2):
        return "noidea", q
    elif(check1>check2):
        return "UNSPSC", q1
    elif(check2>check1):
        return "ICD-10", q2
    elif(check1>0):
        return "UNSPSC", q1
    elif(check2>0):
        return "ICD-10", q2
    else:
        return "RandomChitChat", q

def reward_func(query, dir_name):
    reward = 0
    if(dir_name=='UNSPSC'):
        dir_df = pd.read_csv("./data/unspsc_dataset.csv")
        check = match_score( query, dir_df,'unspsc')
        reward += check
    elif(dir_name=='ICD-10'):
        dir_df = pkl.load(open("./data/icd10_dict1.pkl","rb"))
        check = match_score( query, dir_df,'icd10')
        reward += check
    else:
        dir_df = pd.read_csv("./data/unspsc_dataset.csv")
        check = match_score( query, dir_df,'unspsc')
        reward -= check
        dir_df = pkl.load(open("./data/icd10_dict1.pkl","rb"))
        check = match_score( query, dir_df,'icd10')
        reward -= check

    return reward

#RL Source
def rlsource(query, flag_er):
    global global_df
    check = ''
    ep_count = 0
    epsilon = 0.9
    decay = 0.1
    temp, q = query_dirFinder( query)
    checkrw = 0
    #print(temp)
    #raise KeyboardInterrupt
    if(temp=='noidea'):
        return bcolors.OKCYAN+"Match is found in both UNSPSC and ICD-10. Please choose one or enter another query to further disambiguation", False, q
        #print("Match is found in both the directories UNSPSC and ICD10. Please choose one or enter another query to further disambiguate")
        #query = input("Enter your query:\n")
        #temp = query_dirFinder( query)
    while(check != temp):
        if(flag_er):
            print(bcolors.WARNING+ "\nEpoch - {}".format(ep_count))
            print(bcolors.WARNING+ "The epsilon value is: {}".format(epsilon))
            print()
        ep_count += 1
        thresh = random.uniform(0, 1)
        if thresh <= epsilon:
            check  = ''.join(random.choice(['UNSPSC','ICD-10','RandomChitChat']))
        else:
            check  = temp
        if check == temp:
            if(check in ['UNSPSC','ICD-10']):
                #print(check,temp)
                #raise KeyboardInterrupt
                if(check == 'UNSPSC'):
                    gloabl_df = pd.read_csv('./data/unspsc_dataset.csv')
                    #self.unspsc = True
                    #print("Yes Did it true")
                    #raise KeyboardInterrupt
                elif(check == 'ICD-10'):
                    gloabl_df = pkl.load(open('./data/icd10_dict1.pkl', "rb"))
                    #self.icd10 = True
                    #print("Yes Did it true")
                    #raise KeyboardInterrupt
                return bcolors.OKCYAN+"Information you are looking for is available in directory {}".format(check), True, q
            else:
                return bcolors.OKCYAN+"I am sorry. I do not understand.\nPlease re-enter your query.\n", False, q
        epsilon -= decay
        #check['episode_done'] = False

##changed: Deleted line 3-13. (Error no file plan0.txt found).       
#Added Flag varibale: Directory found for unambiguous query. Query input is not necessary.
def full_search(data,pre1,pre2,words,d3,d2):
        #   Calculating the matches of the given words and mapping them to their corresponding matches
        for i in words:
            for j in range (0,f3):
                y = data.iloc[j][f1]
                if(y.lower().find(i)!=-1):
                    d3[i].append(j)
        #   Calculating the matches which are common for all the words by calculating count 
        d1={}
        d2=[]
        for i in d3:
            for j in d3[i]:
                if(d1.get(j)==None):
                    d1[j]=1
                else:
                    d1[j]+=1
        size=len(words)
        for i,j in d1.items():
            if(j==size):
                d2.append(i)

        #mapping
        sp1={}
        sp2={}
        sp3={}
        sp4=1
        for i in d2:
            sp1[i]=data.iloc[i][f1]
            sp2[i]=data.iloc[i][f2]
            sp3[sp4]=i
            sp4+=1
            
        if(len(d2)==1):
            print(bcolors.OKCYAN + "\nBOT: The code is: ",end="")
            print(bcolors.OKCYAN + sp2[sp3[1]])
        else:
            print(bcolors.FAIL + str(len(d2)),end=" ")
            print(bcolors.FAIL + "instances found !")
            print()
            print(bcolors.OKCYAN + "\nBOT: The possible matches for your query are")
            print()
            cc=1
            for i in d2:
                r1=sp3[cc]
                print(bcolors.OKCYAN + str(cc),end=": ")
                print(bcolors.OKCYAN + str(sp1[r1]))
                # print(r1)
                cc+=1


            print(bcolors.OKCYAN + "\nBOT: Which one do you want to select: ")
            print()
            y=int(input(bcolors.OKGREEN + "\nUSER: "))
            print(bcolors.OKCYAN + "\nBOT: The code is: ",end="")
            print(bcolors.OKCYAN + str(sp2[sp3[y]]))

print(bcolors.OKCYAN + "BOT: Hi, I'm PRUDENT 🤖, here to help you lookup for information. \n Do you want to \n 0)Exit,\n 1)query with manual data source selection (only Planning),\n 2)query with automatic data source selection (RL + Planning),\n 3)query with only RL.\n")
choice = '-1'
c2=input(bcolors.OKGREEN + "USER: ")
c2=c2.lower()

while(choice!="0"):
    flag_dir = False
    flag_epoch_reward = False
    mistake = False
    name_dir = ""
    if(c2=='0'):
        break
    while(flag_dir==False):
        if(c2=='1'):
            print(bcolors.OKCYAN + "\nBOT: Please enter the name of the directory: \n 1. ICD-10 \n 2. UNSPSC")
            c3=input(bcolors.OKGREEN + "\nUSER: ")
            c3=c3.lower()
            if(c3=="1"):
                data = pd.read_csv("./data/icd10.csv") 
                name_dir = "icd10"
                break

            elif(c3=="2"):
                data = pd.read_csv("./data/unspsc_dataset.csv")
                name_dir = "unspsc"
                break
            
            else:
                print(bcolors.OKCYAN +"\nBOT: Please make a selection from the given choice.")
                c2 = '1'

        elif(c2=='2'):
        #else: #changed rl to find the directory
            if(mistake):
                mistake = False
                c2 = input(bcolors.OKGREEN + "\nUSER: ")
                c2 = c2.lower()
            else:
                print(bcolors.OKCYAN + '\nBOT: Please enter your query: ')
                c2 = input(bcolors.OKGREEN + "\nUSER: ")
                c2 = c2.lower()
            temp = rlsource(c2,flag_epoch_reward)
            print(bcolors.OKCYAN + temp[0])
            #print(f"The extracted entity is {temp[2]}\n")
            #raise KeyboardInterrupt
            if(temp[0].count("ICD-10")>0):
                data = pd.read_csv("./data/icd10.csv") 
                flag_dir = True
            elif(temp[0].count("UNSPSC")>0):
                data = pd.read_csv("./data/unspsc_dataset.csv")
                flag_dir = True
            else:
                #print("I do not understand your query.\n")
                c2 = '2'
                mistake = True
                #raise KeyboardInterrupt
        
        elif(c2=='3'):
            flag_epoch_reward = True
        #else: #changed rl to find the directory
            if(mistake):
                mistake = False
                c2 = input(bcolors.OKGREEN + "\nUSER: ")
                c2 = c2.lower()
            else:
                print(bcolors.OKCYAN + '\nBOT: Please enter your query:\n')
                c2 = input(bcolors.OKGREEN + "\nUSER: ")
                c2 = c2.lower()
            temp = rlsource(c2,flag_epoch_reward)
            print(bcolors.OKCYAN + temp[0])
            #print(f"The extracted entity is {temp[2]}\n")
            #raise KeyboardInterrupt
            if(temp[0].count("ICD-10")>0):
                data = pd.read_csv("./data/icd10.csv") 
                flag_dir = True
            elif(temp[0].count("UNSPSC")>0):
                data = pd.read_csv("./data/unspsc_dataset.csv")
                flag_dir = True
            else:
                #print("I do not understand your query.\n")
                c2 = '2'
                mistake = True
                #raise KeyboardInterrupt
        else:
            print(bcolors.OKCYAN + "\nBOT: Please choose one option from:\n Do you want to query with \n 1) manual data source selection (only Planning),\n 2) automatic data source selection (RL + Planning),\n 3) only RL.")
            c2=input(bcolors.OKGREEN + "\nUSER: ")
            c2=c2.lower()
            
    f1=-1
    f2=-1
    f3=-1

    # To distinguish the querying column and output column in case of both dataset i.e, ICD-10 and UNSPSC on the basis of dimension
    if(data.shape==(94765,4)):
        f1=3
        f2=2
        f3=94765
    else:
        f1=1
        f2=0
        f3=4302

    if(flag_dir==False):
        print(bcolors.OKCYAN + "\nBOT: Enter your query")
        x = input(bcolors.OKGREEN + "\nUSER: ")
        x = extract_query(x.lower(),1,name_dir)
        #print(x)
        #raise KeyboardInterrupt
    else:
        x = temp[2]

    # Function for searching the entire dataset
    x=x.lower()
    words = x.split(', ')
    # size=len(words)

    # To remove thestop words
    pre1 = ["due","to","and","other","specified","of","the","a","from","for","without","not"]
    pre2 = ['(',')',',','.']


    # To store the the matches  
    d2=[]
    d3 = defaultdict(list)
    full_search(data,pre1,pre2,words,d3,d2)

    print(bcolors.OKCYAN + "\nBOT: \nDo you want to \n 0)Exit,\n 1)query with manual data source selection (only Planning),\n 2)query with automatic data source selection (RL + Planning),\n 3)query with only RL.\n")
    c2 = input(bcolors.OKGREEN + "\nUSER:")

print(bcolors.OKCYAN + "\nBOT: Thank you for interacting with PRUDENT.")