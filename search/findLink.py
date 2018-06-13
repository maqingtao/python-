import pymysql
class findLink:
    def findLink(self,linkIp):
        con = pymysql.connect("localhost", "root", "root", "test");
        c = con.cursor();
        c.execute("SELECT * FROM userlink WHERE linkip='%s'" %(linkIp))
        r = c.fetchall()
        c.close()
        if r:
            return True
        else:
            return False
