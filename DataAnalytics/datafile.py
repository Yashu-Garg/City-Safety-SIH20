import pandas as pd
import os

def yashu(yas,gender):
    path= os.path.dirname(os.path.realpath(__file__)) + '\data.csv'

    data = pd.read_csv(path, index_col=['DISTRICT'])
    text='''GOVERNMENT OF INDIA,
               You are about to enter an area which according to our records proven to be unsafe for you.
               If you face problem you can contact to the given numbers.
               Click on the given link if you are in emergency'''
    num=''
    if gender=='F':
        num='Women’s helpline – 9947000100,Police line for robbery/ crime etc –100 '
    else:
        num='Police line for robbery/ crime etc –100'
    danger=data.loc[yas,'DANGER']
    return {'loc':data.loc[yas,:],"danger":danger,"msg":text,"number":num}

def getdistrict():
    path = os.path.dirname(os.path.realpath(__file__)) + '\data.csv'
    d1=pd.read_csv(path)
    col_one_list = d1['DISTRICT'].tolist()
    return col_one_list
