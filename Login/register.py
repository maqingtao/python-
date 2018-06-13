import tkinter.messagebox
import tkinter
import pymysql


class register:
    def register(self):
        root = tkinter.Tk()
        root.title('用户注册')
        root.geometry("280x180")
        varName = tkinter.StringVar()
        varName.set('')
        varPwd = tkinter.StringVar()
        varPwd.set('')
        varenPwd = tkinter.StringVar()
        varenPwd.set('')
        labelName = tkinter.Label(root, text='用户名:', justify=tkinter.RIGHT, width=80)
        labelName.place(x=10, y=5, width=80, height=20)
        entryName = tkinter.Entry(root, width=100, textvariable=varName)
        entryName.place(x=100, y=5, width=80, height=20)

        labelPwd = tkinter.Label(root, text='密   码:', justify=tkinter.RIGHT, width=80)
        labelPwd.place(x=10, y=30, width=80, height=20)
        entryPwd = tkinter.Entry(root, show='*', width=100, textvariable=varPwd)
        entryPwd.place(x=100, y=30, width=80, height=20)

        labelenPwd = tkinter.Label(root, text='确认密码:', justify=tkinter.RIGHT, width=80)
        labelenPwd.place(x=10, y=55, width=80, height=20)
        entryenPwd = tkinter.Entry(root, show='*', width=100, textvariable=varenPwd)
        entryenPwd.place(x=100, y=55, width=80, height=20)
        print()
        def cancel():
            varName.set('')
            varPwd.set('')
            varenPwd.set('')
            root.destroy()
        def check():
            username = entryName.get();
            password = entryPwd.get();
            enpassword = entryenPwd.get();
            con = pymysql.connect("localhost", "root", "root", "test");
            c = con.cursor();
            if password == enpassword and password !='' and enpassword!='':
                tkinter.messagebox.showinfo(title='用户注册', message='注册成功！')
                c.execute("insert into userinformation(username,password) values('%s','%s')" % (username, password))
                con.commit()
                c.close()
                root.destroy()
            else:
                tkinter.messagebox.showinfo(title='用户注册', message='两次密码不一致或为空！')
                varName.set('')
                varPwd.set('')
                varenPwd.set('')
        buttonRegister = tkinter.Button(root, text="注册", command=check)
        buttonRegister.place(x=60, y=80, width=50, height=20)
        buttonCancel = tkinter.Button(root, text='取消', command=cancel)
        buttonCancel.place(x=160, y=80, width=50, height=20)
        root.mainloop()
