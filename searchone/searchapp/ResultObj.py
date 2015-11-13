import Const
import sqlite3


class ResultObj():
    def __init__(self, row):
        #zero is url_id, one is url, two is author
        self.url_id = row[0]
        self.text = row[1] + ", " + row[2]
        self.url = row[1]
        self.author = row[2]

    def containsPhrases(self, phrases):
        filename = Const.PGFOLDER + str(self.url_id)
        ucfile = None
        with open(filename, 'r') as myfile:
            entirefile = myfile.read()
            ucfile = unicode(entirefile, 'utf-8').lower()
        for phrase in phrases:
            if(ucfile.find(phrase) == -1):
                return False
        return True

    def calcTFIDF(self, queryterms, idfs):
        
        self.dbgTFIDF = ""
        conn = sqlite3.connect(Const.DATABASEFILE)
        c = conn.cursor()
        i = 0
        sum_tfidf = 0
        for term in queryterms:
            
            c.execute('SELECT freq FROM term_index WHERE _term="' + term + '" AND url_id=' + str(self.url_id))
            freq = int(c.fetchone()[0])
            tfidf = freq * idfs[i]
            sum_tfidf = sum_tfidf + tfidf
            self.dbgTFIDF = self.dbgTFIDF + "Term:" + term + " TF:" + str(freq) + " IDF:" + str(idfs[i]) + " TFIDF:" + str(tfidf) + "\n"
            i = i + 1
        conn.close()
        self.rank = sum_tfidf
