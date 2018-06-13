import tkinter.messagebox
import tkinter
import pymysql
from chatDetail.chatLink import chatLink
from Login.register import register
root = tkinter.Tk()
root.title("聊天系统")
root.geometry("280x180")
varName = tkinter.StringVar()
varName.set('')
varPwd = tkinter.StringVar()
varPwd.set('')
labelName = tkinter.Label(root, text='用户名:', justify=tkinter.RIGHT, width=80)
labelName.place(x=10, y=5, width=80, height=20)
entryName = tkinter.Entry(root, width=100,textvariable=varName)
entryName.place(x=100, y=5, width=80, height=20)
labelPwd = tkinter.Label(root, text='密   码:', justify=tkinter.RIGHT, width=80)
labelPwd.place(x=10, y=30, width=80, height=20)
entryPwd = tkinter.Entry(root, show='*',width=100, textvariable=varPwd)
entryPwd.place(x=100, y=30, width=80, height=20)
# 登录选项
def login():
    name = entryName.get()
    password=entryPwd.get()
    con = pymysql.connect("localhost", "root", "root", "test");
    c = con.cursor();
    c.execute("SELECT * FROM userinformation WHERE username='%s'AND password='%s'" % (name, password))
    r = c.fetchone()
    c.close()
    if r:
        tkinter.messagebox.showinfo(title='login message', message='登录成功！')
        root.destroy()
        s=chatLink()
        s.link(r[2])

    else:
        tkinter.messagebox.showerror('login message', message='密码或用户名错误!')
        varName.set('')
        varPwd.set('')
def cancel():
    varName.set('')
    varPwd.set('')
    root.destroy()
#注册页面
def re():
    re=register()
    re.register()
buttonOk = tkinter.Button(root, text='登录', command=login)
buttonOk.place(x=60, y=70, width=50, height=20)
buttonCancel = tkinter.Button(root, text='取消', command=cancel)
buttonCancel.place(x=120, y=70, width=50, height=20)
labels = tkinter.Label(root, text='没有账号的话请注册', justify=tkinter.RIGHT, width=120)
labels.place(x=20,y=120,width=120,height=20)
buttonRegister=tkinter.Button(root,text="注册",command=re)
buttonRegister.place(x=140,y=120,width=50,height=20)
root.mainloop()
