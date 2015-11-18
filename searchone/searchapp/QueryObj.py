from stemming.porter2 import stem
from ResultObj import ResultObj
import sqlite3
import Const



def buildQueryR(terms):
    if(len(terms) == 0):
        return ["",""]
    elif(len(terms) == 1):
        return ['SELECT id, url, author, email FROM urls WHERE id IN (SELECT url_id FROM term_index WHERE _term_id='+str(terms[0]), ')' ]
    else:
        vals= [' AND url_id IN (SELECT url_id FROM term_index WHERE _term_id='+str(terms[0]), ')']
        subvals = buildQueryR(terms[1:])
        tvals = [subvals[0] + vals[0], subvals[1]+vals[1]]
        return tvals

def buildSQLQuery(terms):
    vals = buildQueryR(terms)
    return vals[0] + vals[1]

def execQuery(aSQLQuery, c):
    c.execute(aSQLQuery)
    rows = c.fetchall()
    results = []
    for row in rows:
        results.append(ResultObj(row))
    return results


def queryfix(queryterms):
    output = map(stem, queryterms)
    output = list(set(output))
    return output

def getPhrases(rawquery):
    phrases = []
    ind = 0
    while(True):
        quotestart = rawquery.find('"', ind)
        if(quotestart == -1):
            break
        quoteend = rawquery.find('"', quotestart + 1)
        ind = quoteend + 1
        if(ind == 0):
            break
        quote = rawquery[quotestart+1:quoteend]
        phrases.append(quote.lower())
    return phrases

class QueryObj():


    def __init__(self, rawquery):
        self.rawquery = rawquery
        sanquery = Const.sanitize(rawquery).split()
        self.query = queryfix(sanquery)
        self.reorderedterms = []

    def getQIDs(self, listterms, c):
        qur = 'SELECT id, idf, _term FROM terms WHERE _term IN("'
        for term in listterms:
            qur = qur + term + '","'
        qur = qur[:-2]
        qur = qur + ") ORDER BY idf ASC"
        c.execute(qur)
        ret = []
        self.idfs = []
        self.reorderedterms = []

        rows = c.fetchall()
        for row in rows:
            ret.append(row[0])
            self.idfs.append(row[1])
            self.reorderedterms.append(row[2])
        return ret

        
    def execute(self):
        conn = sqlite3.connect(Const.DATABASEFILE)
        c = conn.cursor()

        qids = self.getQIDs(self.query, c)
        sqlq = buildSQLQuery(qids)
        
        results = execQuery(sqlq, c)
        
        conn.close()
 
        phrases = getPhrases(self.rawquery)

        if(len(phrases) > 0):
            for result in results:
                result.calcTFIDF(self.reorderedterms, qids, self.idfs)

            results = sorted(results, key=lambda result: result.rank, reverse=True)
            newresults = []
            ind = 0
            while(len(newresults) < 20 and ind < len(results)):
                if(results[ind].containsPhrases(phrases)):
                    newresults.append(results[ind])
                ind = ind + 1
            results = newresults

        else:
            for result in results:
                result.calcTFIDF(self.reorderedterms, qids, self.idfs)


            results = sorted(results, key=lambda result: result.rank, reverse=True)
        
            if(len(results) > 20):
                results = results[:20]

        for result in results:
            result.prepare()

        return results
