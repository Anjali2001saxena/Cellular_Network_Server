import shelve
from message import Message
from call import Call
from server import Server, main

class User :

    def __init__(self, name, age, gender, password):
        self.name = name
        self.age = age
        self.gender = gender
        self.available = True
        self.password = password
        self.call = False
        self.message = False
        self.messages = []
        self.calls = []
        self.caller = None


def add():
    print("Enter the following details : ")
    name = input("Enter the name : ")
    age = input("Enter the age : ")
    gender = input("Enter the gender : ")
    password = input("Enter the password : ")

    user = User(name, age, gender, password)
    return user


server = Server()

print("Welcome!")

while True:
    print("1. Add user")
    print("2. Select user")
    print("3. View Profile")
    print("4. View users list")
    print("5. View message")
    print("6. Send a message")
    print("7. Make a voice call")
    print("8. Recieve a voice call")
    print("9. Exit")

    choice = int(input("Select the service : "))

    if choice == 1:
        user = add()
        main.add_user(user)
    elif choice == 2:
        global curr_user 
        curr_user = main.select_user()
    elif choice == 3 :
        main.profile(curr_user)
    elif choice == 4 :
        main.user_list()
    elif choice == 5 :
        main.recieve_message(curr_user)
    elif choice == 6 :
        main.send_message(curr_user)
    elif choice == 7 :
        main.outgoing_call(curr_user)
    elif choice == 8 :
        main.incoming_call(curr_user)
    elif choice == 9 :
        break
    else:
        print("Incorrect Choice!!")

