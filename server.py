import shelve
from message import Message
from call import Call
class Server:

    db = shelve.open("data")
    #messages_db = shelve.open("message")
    #calls_db = shelve.open("call")
    users = []

    def __init__(self):
        self.curr_user = None

    def find_user(self, name):
        user_db = shelve.open("user")
        for key in user_db.keys():
            user = user_db[key]
            if user.name == name:
                user_db.close()
                return user
        user_db.close()
        return None
        


    def add_user(self, user):
        user_db = shelve.open("user")
        self.users.append(user)
        key = user.name
        self.db[key] = user
        user_db[key] = user
        print("User added!!")
        user_db.close()

    def select_user(self):
        user_name = input("Enter user name : ")
        password = input("Enter password : ")

        curr_user = self.find_user(user_name)
        if curr_user.password == password :
            print("Hello " + curr_user.name)
            return curr_user
        else:
            print("User not found!!")

    def profile(self, curr_user):
        print("User Profile")
        print("Name : " + curr_user.name)
        print("Age : " + curr_user.age)
        print("Gender : " + curr_user.gender)

    def user_list(self):
        user_db = shelve.open("user")
        if len(user_db)==0 :
            print("No available users")
        else:
            for key in user_db.keys():
                user = user_db[key]
                print(user.name)
        user_db.close()

    def recieve_message(self, curr_user):
        user_db = shelve.open("user")
        messages_db = shelve.open("message")
        user = user_db[curr_user.name]
        if len(user.messages) == 0:
            print("No available messages")
        else:
            messages = messages_db[curr_user.name]
            mes_obj = messages[-1]
            print("From ", mes_obj.sender.name, ": ", mes_obj.message)

        messages_db.close()
        user_db.close()

    def send_message(self, curr_user):
        user_db = shelve.open("user")
        messages_db = shelve.open("message")
        reciever = input("Enter the reciever name : ")
        rec = self.find_user(reciever)
        if rec == None:
            print("No user found!!")
            return
        message = input("Enter the message : ")
        mes = Message(message, curr_user, rec)
        rec.message = True
        rec.messages.append(mes)
        curr_user.messages.append(mes)
        user_db[rec.name] = rec
        user_db[curr_user.name] = curr_user
        messages_db[rec.name] = rec.messages
        messages_db[curr_user.name] = curr_user.messages
        print("Message sent!!")
        messages_db.close()
        user_db.close()

    def outgoing_call(self, curr_user):
        user_db = shelve.open("user")
        calls_db = shelve.open("call")
        reciever = input("Enter the reciever name : ")
        rec = self.find_user(reciever)
        if rec == None:
            print("No user found!!")
            return
        rec.call = True
        call = Call(curr_user, rec)
        rec.calls.append(call)
        curr_user.calls.append(call)
        user_db[rec.name] = rec
        user_db[curr_user.name] = curr_user
        calls_db[rec.name] = rec.calls
        calls_db[curr_user.name] = curr_user.calls
        if rec.available == False:
            print("Busy on another call")
        else:
            curr_user.available = False
            user_db[curr_user.name] = curr_user
            rec.caller = curr_user
            user_db[rec.name] = rec
            print("Call connecting...")

        calls_db.close()
        user_db.close()

    def incoming_call(self, curr_user):
        user_db = shelve.open("user")
        calls_db = shelve.open("call")
        user = user_db[curr_user.name]
        if user.call == False:
            print("No available calls")
        else:
            if user.caller == None:
                print("No available calls")
                return
            caller = user_db[user.caller.name]
            print("Incoming call ", caller.name)
            print("1. Accept")
            print("2. Decline")
            choice = int(input("Enter the choice : "))
            if choice == 1:
                curr_user.available = False
                user_db[curr_user.name] = curr_user
                print("Call connected!!")
                decline = int(input("Press 1 to decline the call : "))
                if decline == 1:
                    caller.available = True
                    curr_user.available = True
                    self.db[caller.name] = caller
                    self.db[curr_user.name] = curr_user
                    print("Call declined!!")

            else:
                caller.available = True
                curr_user.available = True
                self.db[caller.name] = caller
                self.db[curr_user.name] = curr_user
                print("Call declined!!")

            curr_user.call = False
            user_db[curr_user.name] = curr_user
            
        calls_db.close()
        user_db.close()

main = Server()


            
        