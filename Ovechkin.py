# -*- coding: cp1251 -*-

import sqlite3
import time
import datetime


class Database:
    def __init__(self, db_name=None):
        today = datetime.datetime.today()
        print(today.strftime("%m/%d/%Y"))  # '04/05/2017'

        self.conn = sqlite3.connect(today.strftime("%Y_%m_%d_%H%M%S_") + db_name+'.db')
        self.cu = self.conn.cursor()
        self.cu.execute("CREATE TABLE User (user_name text, user_id INTEGER PRIMARY KEY)")
        self.cu.execute("CREATE TABLE Comments (comments text, user_id INTEGER NOT NULL REFERENCES User(user_id), "
                        "comments_id INTEGER PRIMARY KEY, commentsTonality text)")
        self.cu.execute("CREATE INDEX indexA ON User (user_id, user_name)")
        self.cu.execute("CREATE INDEX indexC ON Comments (user_id, comments_id, comments)")
        self.userId= 0
        self.commentsId = 0
    
    def checkUserId(self, userName):        
        self.cu.execute("SELECT user_id FROM User WHERE user_name LIKE '" + userName + "'")
        results = self.cu.fetchall()
        
        if len(results):
            res = list(results[0])
            return 1, res[0]
        else:
            return 0, 0
        
    def savetodb(self, userName, comment, wordsSearch):
        #print "User Id ="+self.userId
        flag_exist = 0

        if len(wordsSearch):
            for name in wordsSearch:
                if name in comment:
                    flag_exist = 1
        else:
            flag_exist = 1

        if flag_exist:            
            un = userName  # type: object
            cmnt = comment
            self.commentsId+=1
            flag, res = self.checkUserId(un)
            if(flag):
                self.cu.execute("INSERT INTO Comments(comments, comments_id, commentsTonality, user_id) VALUES(?, ?, ?, ?)",
                                (comment, self.commentsId, "NOT", res))
            else:
                print self.userId
                self.userId += 1
                self.cu.execute("INSERT INTO User(user_name, user_id) VALUES(?, ?)", (un, self.userId,))
                self.cu.execute("INSERT INTO Comments(comments, comments_id, "
                                "commentsTonality, user_id) VALUES(?, ?, ?, ?)",
                                (cmnt, self.commentsId, "NOT", self.userId))
            
    def deinit(self):
        print "End"
        self.conn.commit()
        self.conn.close()
