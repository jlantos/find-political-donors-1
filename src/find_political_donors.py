import os
import sys
import time
import math
import numpy as np
import pylab as pl

class Item:
    CMTE_ID = ''
    ZIP_CODE = ''
    TRANSACTION_DT = ''
    TRANSACTION_AMT = 0
    OTHER_ID = ''

    def __init__(self, vCMTE_ID, vZIP_CODE, vTRANSACTION_DT, vTRANSACTION_AMT, vOTHER_ID):
        self.CMTE_ID = vCMTE_ID
        self.ZIP_CODE = vZIP_CODE
        self.TRANSACTION_DT = vTRANSACTION_DT
        self.TRANSACTION_AMT = vTRANSACTION_AMT
        self.OTHER_ID = vOTHER_ID

Items = []
datedic = {}
global Length
Length = 0

def isdt(s):
    try:
        int(s)
        if(len(s)>8):
            return False
        return True
    except ValueError:
        return False

def ReadItems():
    if len(sys.argv) < 4 : #sys.argv[0] != ./src/find_political_donors.py
        print "Error input arguments!\nUsage: python ./src/find_political_donors.py ./input/[InputFilename].txt ./output/medianvals_by_zip.txt ./output/medianvals_by_date.txt "
        os._exit(-1) 
    else:
        input_filename = sys.argv[1]
        if os.path.exists(input_filename):
            f = open(input_filename, "r")            
            count = 0
            global Length
            Length = 0
            while True:
                line = f.readline()
                if line:
                    count = count + 1
                    colum = 0
                    cmteid = ''
                    zipcode = ''
                    transactiondt = ''
                    transactionamt = 0
                    otherid = ''
                    flag = 0
                    for word in line.split('|'):
                        if colum == 0:
                            cmteid = word
                        elif colum == 10:
                            zipcode = word[:5]
                        elif colum == 13:
                            transactiondt = word
                        elif colum == 14:
                            if word == '':
                                flag = 1
                                break
                            transactionamt = float(word)
                        elif colum == 15:
                            otherid = word
                        else:
                            pass
                        

                        colum = colum + 1

                    if otherid != '' or cmteid == '' or transactiondt == '' or flag == 1 or isdt(transactiondt) == False:
                        pass
                    else:
                        Length = Length + 1
                        ite = Item(cmteid, zipcode, transactiondt, transactionamt, otherid)
                        Items.append(ite)
                        #datedic.update({Items[Length-1].TRANSACTION_DT : Items[Length-1].TRANSACTION_AMT}) 
                else:
                    break

            #print 'Useful: \t' + str(Length) + ' items.'
            #print 'Total : \t' + str(count) + ' items.'
            f.close()
        else:
            print "Input file is not exist!\nUsage: python [filename].py -i <inputFile>"
            os._exit(-1)
    

def printItems():
    for i in range(0,len(Items)):
        print ''
        print 'CMTE_ID: ' + Items[i].CMTE_ID
        print 'ZIP_CODE: ' + Items[i].ZIP_CODE
        print 'TRANSACTION_DT: ' + Items[i].TRANSACTION_DT
        print 'TRANSACTION_AMT: ' + str(Items[i].TRANSACTION_AMT)
        print 'OTHER_ID: ' + Items[i].OTHER_ID
        print ''

def print_medianvals_by_zip(f):
    dic = {}

    for i in range(0,len(Items)):  
        s =  Items[i].ZIP_CODE
        median = 0
        summ = 0
        if s not in dic.keys():
            median = int(round(Items[i].TRANSACTION_AMT))
            summ = median
            dic.update({s:[Items[i].TRANSACTION_AMT]})   
        else:
            dic[s].append(Items[i].TRANSACTION_AMT)
            dic[s].sort()
            summ = int(round(sum(dic[s])))
            if (len(dic[s])%2 == 1):
                median = dic[key][len(dic[s])-1]
            else:
                median = int(round((dic[s][len(dic[s])-2] + dic[s][len(dic[s])-1])/2.0))
                
        print Items[i].CMTE_ID + '|' + Items[i].ZIP_CODE + '|' + str(median) +'|' + str(len(dic[s])) + '|' + str(summ)
        f.write(Items[i].CMTE_ID + '|' + Items[i].ZIP_CODE + '|' + str(median) +'|' + str(len(dic[s])) + '|' + str(summ) + '\n')

def print_medianvals_by_date(f):
    #if Items[i].TRANSACTION_DT == '' or malformed: pass
    dic = {}
    for i in range(0,len(Items)):
        s = Items[i].CMTE_ID+'|'+Items[i].TRANSACTION_DT
        if s not in dic.keys():
            dic.update({s:[Items[i].TRANSACTION_AMT]})
        else:
            dic[s].append(Items[i].TRANSACTION_AMT)

    for key, v in dic.items():
        median = 0
        dic[key].sort()
        summ = int(round(sum(dic[key])))
        if (len(dic[key])%2 == 1):
            median = dic[key][len(dic[key])-1]
        else:
            median = int(round((dic[key][len(dic[key])-2] + dic[key][len(dic[key])-1])/2.0))
        print key + '|' + str(median) +'|' + str(len(dic[key])) + '|' + str(summ)
        f.write(key + '|' + str(median) +'|' + str(len(dic[key])) + '|' + str(summ) + '\n')

   
if __name__ == '__main__':
    ReadItems()
    #printItems()
    
    output_filename1 = sys.argv[2]
    f1 = open(output_filename1, "w")
    print_medianvals_by_zip(f1)
    f1.close()
    
    output_filename2 = sys.argv[3]
    f2 = open(output_filename2, "w")
    print ''
    print_medianvals_by_date(f2)
    f2.close()
    





    
