#input loop
#get msg
#get intent
#exec func
#or ask to be clear
#funcs: hi, bye, login, registration, withdrawing, depositing, check balance
#user db: name, id, amount
#               training code
#python -m rasa_nlu.train -c nlu_config.yml --data nlu.md -o models --fixed_model_name nlu --project current --verbose
#C:\Users\hp\AppData\Local\Programs\Python\Python37\python.exe -m rasa_nlu.train -c nlu_config.yml --data nlu.md -o models --fixed_model_name nlu --project current --verbose
#
from rasa_nlu.model import Interpreter
import json, shelve, random, string
interpreter = Interpreter.load("./models/current/nlu")
database=shelve.open('database3.db', flag='c',writeback=True)
cur_user=None

def chatbot(msg):
    result=interpreter.parse(message)
    return result['intent']['name'],result['intent']['confidence']
    
def id_generator(size=6, chars=string.digits):
    pin=''.join(random.choice(chars) for _ in range(size))
    if pin in database.keys():
        id_generator
    else:
        return pin

def hi():
    data=['hi','hello','greetings']
    print (random.choice(data))

def bye():
    data=['bye','farewell','toot-a-loo']
    cur_user=None
    print (random.choice(data))

def register():
    global cur_user
    global database
    name=str(input('name > '))
    pwd=str(input('password > '))
    amount=float(input('amount > '))
    ID=id_generator()
    database[ID]={'name':name,'amount':amount,'pwd':pwd}
    database.sync()
    cur_user=ID
    print ('your account is registered the id is:',ID)

def login():
    global cur_user
    global database
    ID=input('ID > ')
    pwd=input('password > ')
    if ID in database.keys():
        if database[ID]['pwd']==pwd:
            cur_user=ID
        else:
            print ('wrong password, try again!')
            login()
    else:
        print ('sorry we seem to not have that id number, register with us')
        register()

def check_balance():
    global cur_user
    global database
    if cur_user:
        print ('your current balance is:',database[cur_user]['amount'])
    else:
        login()
        
def check_id():
    global cur_user
    global database
    ID=input('ID >')
    pwd=input('password >')
    if ID in database.keys():
        if database[ID]['pwd']==pwd:
            cur_user=ID
            return True
    return False

def deposit():
    global cur_user
    global database
    if check_id():
        amount=float(input('how much would you like to deposit?'))
        database[cur_user]['amount']+=amount
        database.sync()
        print ('your new balance is:',database[cur_user]['amount'])
    else:
        print ("you used the wrong password or ID")

def withdraw():
    global cur_user
    global database
    if check_id():
        amount=float(input('how much would you like to withdraw?'))
        if database[cur_user]['amount']>amount:
            database[cur_user]['amount']-=amount
            database.sync()
            print ('your new balance is:',database[cur_user]['amount'])
        else:

            print ('sorry your balance ( ',database[cur_user]['amount'],'$ ) is not enough')
    else:
        print ("you used the wrong password or ID")

        
while True:
    message = input('sys> ')
    intent,confidence=chatbot(message)
    print (intent,confidence)
    #greet, bye, login, registration, withdrawing, depositing, check balance
    if confidence > 0.3:
        if intent=='hi':
            hi()
        elif intent=='bye':
            bye()
        elif intent=='registration':
            register()
        elif intent=='login':
            login()
        elif intent=='withdraw':
            withdraw()
        elif intent=='deposit':
            deposit()
        elif intent=='checkbalance':
            check_balance()
        else:
            print ("can you rephrase that")
    else:
        print ("can you rephrase that")
