import tkinter.messagebox
import tkinter
from search.findLink import findLink
from chatDetail.chatStart import P2pChat
class chatLink:
    def link(self,chatname):
        root = tkinter.Tk()
        root.title('建立连接')
        root.geometry("300x100")
        varLink=tkinter.StringVar()
        helloword="尊敬的用户:"+chatname+"您好！"
        usernameLabel = tkinter.Label(root, text=helloword, justify=tkinter.RIGHT, width=100)
        usernameLabel.place(x=5, y=5, width=140, height=20)
        labelLink = tkinter.Label(root, text='输入连接用户IP地址', justify=tkinter.RIGHT, width=100)
        labelLink.place(x=5, y=35, width=140, height=20)
        entryLink = tkinter.Entry(root, width=150, textvariable=varLink)
        entryLink.place(x=140, y=35, width=130, height=20)
        def linkStart():
            linkip=entryLink.get()
            find=findLink()
            flag=find.findLink(linkip)

            if flag:
                tkinter.messagebox.showinfo('link message', message='连接成功!')
                root.destroy()
                roots = tkinter.Tk()
                roots.title("聊天登录")
                p2p_chat = P2pChat(master=roots, username=chatname)
                p2p_chat.mainloop()
            else:
                tkinter.messagebox.showerror('link message', message='连接地址不存在!')

        buttonLink = tkinter.Button(root, text="开始连接",command=linkStart)
        buttonLink.place(x=40, y=70, width=60, height=20)
        def cancel():
            varLink.set('')
            root.destroy()
        buttonCancel = tkinter.Button(root, text='取消',command=cancel)
        buttonCancel.place(x=130, y=70, width=60, height=20)

        root.mainloop()


if __name__ == '__main__':
  c=chatLink()
  c.link()