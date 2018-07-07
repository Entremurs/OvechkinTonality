# -*- coding: cp1251 -*-
import texterra
import sqlite3
import time

texterra.__init__('89f374098c44e275f5b9b0a28933c953ab01b50c')
t= texterra.API('89f374098c44e275f5b9b0a28933c953ab01b50c')


class OvechkinTonalityDetection():
    def __init__(self):
        self.conn = sqlite3.connect('Ovechkin.db');
        self.cu = self.conn.cursor()
        self.qty = 0
        print "ok"
        
    def getTonalitySaveDB(self):

        self.cu.execute("SELECT comments FROM Comments")
        results = self.cu.fetchall()
        print len(results)
        for comment in results:
            sents   = t.polarity_detection(comment)
            print sents
            s       = list(sents)[0]
            print s
            time.sleep(1)
            self.qty+=1
            if self.qty%10 == 0:
                time.sleep(20)
            if self.qty%200 == 0:
                self.conn.commit()
                time.sleep(500)
          
            print self.qty
            self.cu.execute("UPDATE Comments SET commentsTonality=? WHERE comments_id=?", (s[0], self.qty))
            
    def deinit(self):
        print "End"
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    ton = OvechkinTonalityDetection()
    ton.getTonalitySaveDB()
    ton.deinit()
