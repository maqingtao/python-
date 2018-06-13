import pymysql
class getChatName:
    #根据自身ip来获得聊天昵称
    def getName(self,ip):
        con = pymysql.connect("localhost", "root", "root", "test");
        c = con.cursor();
        c.execute("SELECT * FROM userinformation WHERE ip='%s'" %(ip))
        r = c.fetchone()
        c.close()
        return r[2]

