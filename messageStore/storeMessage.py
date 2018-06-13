import pymysql
from search.getChatName import getChatName
class storeMessage:
    def store(self,message,userip,hostip):
         con = pymysql.connect("localhost", "root", "root", "test")
         username=getChatName().getName(userip)
         sendusername = getChatName().getName(hostip)
         c = con.cursor()
         c.execute("insert into usermessage(username,sendusername,message) values('%s','%s','%s')" % (username,sendusername,message))
         con.commit()
         c.close()
