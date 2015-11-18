import Const
import sqlite3

RANGE = 85

class ResultObj():
    def __init__(self, row):
        #zero is url_id, one is url, two is author
        self.url_id = row[0]
        self.text = row[1] + ", " + row[2]
        self.url = row[1]
        self.author = row[2]
        self.email = row[3]
        self.snippet = ""
        self.bestterm = ""

    def containsPhrases(self, phrases):
        filename = Const.PGFOLDER + str(self.url_id)
        ucfile = None
        with open(filename, 'r') as myfile:
            entirefile = myfile.read()
            ucfile = unicode(entirefile, 'utf-8').lower()
        for phrase in phrases:
            anIndex = ucfile.find(phrase)
            if(anIndex == -1):
                return False
            if(self.snippet == ""):
                start = max(anIndex-RANGE, 0)
                end = min(len(ucfile), anIndex+RANGE)
                self.snippet = ucfile[start:end]
        return True

    def prepare(self):
        Const.log("URLID " + str(self.url_id))
        Const.log("BESTTERM " + self.bestterm)
        if(self.snippet == "" and not self.bestterm == ""):
            Const.log("in if")
            filename = Const.PGFOLDER + str(self.url_id)
            ucfile = None
            with open(filename, 'r') as myfile:
                Const.log("File open")
                entirefile = myfile.read()
                ucfile = unicode(entirefile, 'utf-8').lower()
            anIndex = ucfile.find(self.bestterm)
            Const.log("Find ind " + str(anIndex))
            if(not anIndex == -1):
                start = max(anIndex-RANGE, 0)
                Const.log("START : " + str(start))
                end = min(len(ucfile), anIndex + RANGE)
                Const.log("END : " + str(end))
                rng = end - start
                Const.log("RNG : " + str(rng))
                self.snippet = ucfile[start:end]
                Const.log("SNIPPET : " + self.snippet)

    def calcTFIDF(self, terms, qids, idfs):
        
        self.dbgTFIDF = ""
        conn = sqlite3.connect(Const.DATABASEFILE)
        c = conn.cursor()
        i = 0
        sum_tfidf = 0
        maxtfidf = -1.0
        for anid in qids:
            
            c.execute('SELECT freq FROM term_index WHERE _term_id="' + str(anid) + '" AND url_id=' + str(self.url_id))
            freq = int(c.fetchone()[0])
            tfidf = freq * idfs[i]
            if(tfidf > maxtfidf):
                maxtfidf = tfidf
                self.bestterm = terms[i]
            sum_tfidf = sum_tfidf + tfidf
            self.dbgTFIDF = self.dbgTFIDF + "Term:" + terms[i] + " TF:" + str(freq) + " IDF:" + str(idfs[i]) + " TFIDF:" + str(tfidf) + "\n"
            i = i + 1
        conn.close()
        self.rank = sum_tfidf
