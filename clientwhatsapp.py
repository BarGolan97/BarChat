#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
import tkinter.ttk as ttk
from tkinter.ttk import *
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from tkinter import *
import os
import pickle



USERNAME = 0
PASSWORD = 1
global your_groups
global current_group
global unreads
unreads = {}
your_groups = []


def update_curren_group():
    print (current_group)
    return current_group
#-----------------------------

# Designing window for registration

def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter details below", bg="white").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command=register_user).pack()


# Designing window for login

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command=login_verify).pack()


def Join_user(Agroup = None):




    #with open('/Users/bargolan/PycharmProjects/if/cyberfinal_project/unread.pickle', 'rb') as handle:
    #   b = pickle.load(handle)
    b = unreads
    print ('im printing the groups and masseges:\n')
    print (b)

    if Agroup:
        group_info = Agroup
    else:
        group_info = group.get()



    print('im checcking if '+group_info+ 'is in b :\n')
    if group_info in b.keys():
        messages = b[group_info]
        print(messages)
        if messages != '' :
            if type(messages) == list:
                for f in messages:
                    msg_list.insert (END,f)

            else:
                msg_list.insert(END,messages)
        else:
            pass

    try:
        join_group_screen.destroy()
        login_screen.destroy()
        main_screen.destroy()

        '''if Agroup:
            group_info = Agroup
        else:
            group_info = group.get()
            '''

        if group_info not in your_groups:
            your_groups.append(group_info)
            unreads[group_info] = []
        server_group = '#' + group_info
        print(server_group)
        client_socket.send(bytes(server_group, "utf8"))

        current_group = group_info
        file1 = open("file.txt", "w")
        file1.write(current_group)
        file1.close()

        print(your_groups, current_group)


    except:
        '''
        if Agroup:
            group_info = Agroup
        else:
            group_info = group.get()
    '''

        msg_list.delete(0, 'end')
        if group_info not in your_groups:
            your_groups.append(group_info)
            unreads[group_info] = []
        server_group = '#' + group_info
        print(server_group)
        client_socket.send(bytes(server_group, "utf8"))

        current_group = group_info
        file1 = open("file.txt", "w")
        file1.write(current_group)
        file1.close()

        print (your_groups,current_group)



#delete_join_user()



# Implementing event on register button

def register_user():
    username_info = username.get()
    password_info = password.get()
    regArry = ['register',username_info,password_info]
    data_string = pickle.dumps(regArry)
    client_socket.send(data_string)
    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()


# Implementing event on login button

def login_verify():

    username1 = username_verify.get()
    password1 = password_verify.get()
    regArry = ['signin', username1, password1]
    data_string = pickle.dumps(regArry)
    client_socket.send(data_string)
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    answer = client_socket.recv(BUFSIZ).decode("utf8")
    print ('-------------------------------------'+answer)


    if answer == "login success":
            login_sucess()

    elif answer == 'login fail' :
            password_not_recognised()
    else:
        print (answer)
        user_not_found()

# Designing popup for login success

def login_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()




# Designing popup for login invalid password

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()


# Designing popup for user not found

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Unsuccessful")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()


# Deleting popups

def delete_login_success():
    login_success_screen.destroy()
    join_group()

#def delete_join_user ():
 #   Join_user.destroy()







def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()


# Designing Main(first) window

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    Label(text="Select Your Choice", bg="white", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()

    main_screen.mainloop()


#join group screen

def join_group():

    #client_socket.send(bytes("$$$i want to know the groups", "utf8"))
    #list_of_groups = client_socket.recv(BUFSIZ).decode("utf8")

    #list_of_groups = list_of_groups.split('|')
    list_of_groups = ['main group']



    global join_group_screen
    join_group_screen = Toplevel(main_screen)
    join_group_screen.title("Join Group")
    join_group_screen.geometry("300x250")
#
    global group
    global group_entry
    group = StringVar()
#
    Label(join_group_screen, text="Please enter details below", bg="white").pack()
    Label(join_group_screen, text="").pack()
    group_lable = Label(join_group_screen, text="group name * ")
    group_lable.pack()
    group_entry = Entry(join_group_screen, textvariable=group)
    group_entry.pack()
    Label(join_group_screen, text="").pack()

# Python3 program to get selected

# value(s) from tkinter listbox

# Import tkinter


    # Create a listbox
    listbox = Listbox(join_group_screen, width=150, height=100, selectmode=SINGLE)


    a=1
    for i in list_of_groups :
        listbox.insert(a,i)
        a=a+1

    # Inserting the listbox items
    #listbox.insert(1, "group_1")
    #listbox.insert(2, "group_2")
    #listbox.insert(3, "group_3")
    #listbox.insert(4, "group_4")
    #listbox.insert(5, "group_5")


    # Function for printing the
    # selected listbox value(s)
    def selected_item(a=None):
        print ('hi')

        # Traverse the tuple returned by
        # curselection method and print
        # corresponding value(s) in the listbox

        if group_entry is None or group.get() == '' :
            for i in listbox.curselection():
                Group_choice = listbox.get(i)
            Join_user(Group_choice)

        #if listbox.curselection() != ():
        else :
            Join_user()



    # Create a button widget and
    # map the command parameter to
    # selected_item function

    btn = Button(join_group_screen, text='Press Enter', command=selected_item)
    # Placing the button and listbox
    btn.pack(side = BOTTOM)
    listbox.pack()
    join_group_screen.bind('<Return>', selected_item)




#------------------------------------------------




def sidplay_your_groups_screen():
    global your_group_screen
    your_group_screen = Toplevel(top)

    your_group_screen.title("Your current groups")
    your_group_screen.geometry("300x250")
    box = Listbox(your_group_screen, width=150, height=100, selectmode=SINGLE)
    t = 1
    for v in your_groups:
        box.insert(t,v)
        t = t+1

    def chosen_item(a=None):

        # Traverse the tuple returned by
        # curselection method and print
        # corresponding value(s) in the listbox
        for c in box.curselection():
            selection = box.get(c)
        if selection is None:
            pass
        Join_user(selection)

    bt = Button(your_group_screen, text='Press Enter', command=chosen_item)
    bt.pack(side=BOTTOM)
    box.pack()

    your_group_screen.bind('<Return>', chosen_item)








def another_join_group():

    client_socket.send(bytes("$$$i want to know the groups", "utf8"))

    list_of_groups = client_socket.recv(BUFSIZ)
    list_of_groups = pickle.loads(list_of_groups)

    global group_screen
    group_screen = Toplevel(top)
    group_screen.title("Join Group")
    group_screen.geometry("300x250")
    #
    global choice
    global choice_entry
    global lbox
    choice = tkinter.StringVar()
    #
    Label(group_screen, text="Please enter details below", bg="white").pack()
    Label(group_screen, text="").pack()
    g_lable = Label(group_screen, text="group name * ")
    g_lable.pack()
    choice_entry = tkinter.Entry(group_screen, textvariable = choice)
    choice_entry.pack()
    Label(group_screen, text="").pack()

    # Python3 program to get selected

    # value(s) from tkinter listbox

    # Import tkinter

    # Create a listbox
    lbox = Listbox(group_screen, width=150, height=100, selectmode=SINGLE)


    a = 1
    for i in list_of_groups:
        lbox.insert(a, i)
        a = a + 1

    def a_item(a=None):
        global choice
        print('hi')
        print(choice.get())
        # Traverse the tuple returned by
        # curselection method and print
        # corresponding value(s) in the listbox
        if choice_entry is None or choice.get() == '':
            for c in lbox.curselection():
                Group_choice = lbox.get(c)
            Join_user(Group_choice)

        # if listbox.curselection() != ():
        else:
            Join_user(choice.get())


    bt = Button(group_screen, text='Press Enter', command=a_item)
    bt.pack(side=BOTTOM)
    lbox.pack()

    group_screen.bind('<Return>', a_item)





Expected_PORT = 33000
HOST = str(os.system("ipconfig getifaddr en0"))[:-1]
PORT = Expected_PORT
#----Now comes the sockets part----
#HOST = input('Enter host: ')
#PORT = input('Enter port: ')
if not PORT:
    PORT = Expected_PORT
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)
try:
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)
    main_account_screen()



except:
    print ('unable to connect')
    exit()

def MAINWHATSAPP():


    def receive():
        """Handles receiving of messages."""

        while True:
            try:

                file1 = open('file.txt', 'r')
                current_group = file1.read()
                file1.close()

                msg = client_socket.recv(BUFSIZ).decode("utf8")
                splitedmsg = msg.split('|')

                print (current_group+'\n',splitedmsg[1])
                if splitedmsg[1] == current_group:
                    msg_list.insert(tkinter.END, splitedmsg[0])
                else:


                    unreads[splitedmsg[1]] = splitedmsg [0]
                    #with open('/Users/bargolan/PycharmProjects/if/cyberfinal_project/unread.pickle', 'wb') as handle:
                     #   pickle.dump(unreads, handle, protocol=pickle.HIGHEST_PROTOCOL)


            except OSError:  # Possibly client has left the chat.
                break

            except:
                time.sleep(0.1)


    def send(event=None):  # event is passed by binders.
        """Handles sending of messages."""

        msg = my_msg.get()
        my_msg.set("")  # Clears input field.
        client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            client_socket.close()
            top.quit()


    def on_closing(event=None):
        """This function is to be called when the window is closed."""
        my_msg.set("{quit}")
        send()


    global top
    global msg_list
    top = tkinter.Tk()

    fi = open('file.txt', 'r')
    curr = fi.read()

    top.title(curr)
    messages_frame = tkinter.Frame(top)
    my_msg = tkinter.StringVar()  # For the messages to be sent.


    my_msg.set("Type your messages here.")
    scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
    # Following will contain the messages.
    msg_list = tkinter.Listbox(messages_frame, height=15, width=60, yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()

    entry_field = tkinter.Entry(top, textvariable=my_msg)
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", command=send)
    send_button.pack()
    group_button = tkinter.Button(top, text="Join Group", command=another_join_group)
    group_button.pack()

    style = ttk.Style()

    # This will be adding style, and
    # naming that style variable as
    # W.Tbutton (TButton is used for ttk.Button).
    style.configure('W.TButton', font=
    ('calibri', 10, 'bold', 'underline'),
                    foreground='blue')

    # Style will be reflected only on
    # this button because we are providing
    # style only on this Button.
    ''' Button 1'''
    btn1 = ttk.Button(top, text='Your Groups -->',
                  style ='W.TButton',
                command=sidplay_your_groups_screen)

    btn1.place(relx=1, x=-2, y=2, anchor=NE)


    top.protocol("WM_DELETE_WINDOW", on_closing)



    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkinter.mainloop()  # Starts GUI execution.




# login screen





MAINWHATSAPP()