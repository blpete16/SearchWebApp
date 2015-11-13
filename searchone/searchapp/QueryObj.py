from stemming.porter2 import stem
from ResultObj import ResultObj
import sqlite3
import Const


def buildQueryR(terms):
    if(len(terms) == 0):
        return ""
    elif(len(terms) == 1):
        return ['SELECT id, url, author FROM urls WHERE id IN (SELECT url_id FROM term_index WHERE _term="'+terms[0]+'"', ')' ]
    else:
        vals= [' AND url_id IN (SELECT url_id FROM term_index WHERE _term="'+terms[0]+'"', ')']
        subvals = buildQueryR(terms[1:])
        tvals = [subvals[0] + vals[0], subvals[1]+vals[1]]
        return tvals

def buildSQLQuery(terms):
    vals = buildQueryR(terms)
    return vals[0] + vals[1]

def execQuery(aSQLQuery):
    conn = sqlite3.connect(Const.DATABASEFILE)
    c = conn.cursor()
    c.execute(aSQLQuery)
    rows = c.fetchall()
    results = []
    for row in rows:
        results.append(ResultObj(row))
    conn.close()
    return results

def sanitize(text):
    ZERO_ASCII = 48
    NINE_ASCII = 57
    CAPA_ASCII = 65
    CAPZ_ASCII = 90
    SPACE_ASCII = 32
    LOWA_ASCII = 97
    LOWZ_ASCII = 122

    output = ""
    for letter in text:
        asciival = ord(letter)
        if(asciival == SPACE_ASCII):
            output = output + letter
        if(asciival >= ZERO_ASCII and asciival <= NINE_ASCII):
            output = output + letter
        if(asciival >= CAPA_ASCII and asciival <= CAPZ_ASCII):
            output = output + str(unichr(32+asciival))
        if(asciival >= LOWA_ASCII and asciival <= LOWZ_ASCII):
            output = output + letter
    return output


def queryfix(queryterms):
    output = map(stem, queryterms)
    output = list(set(output))
    return output

def queryidfs(aquery):
    conn = sqlite3.connect(Const.DATABASEFILE)
    print "Connecting to: " + Const.DATABASEFILE
    c = conn.cursor()
    results = []
    for term in aquery:
        c.execute('SELECT idf FROM terms WHERE _term="' + term + '"')
        idf = float(c.fetchone()[0])
        results.append(idf)
    conn.close()
    return results

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
        sanquery = sanitize(rawquery).split()
        self.query = queryfix(sanquery)
        self.idfs = queryidfs(self.query)
        
    def execute(self):
        sqlq = buildSQLQuery(self.query)
        
        results = execQuery(sqlq)

        phrases = getPhrases(self.rawquery)

        #starthere.
        results = filter(lambda r : r.containsPhrases(phrases), results)

        for result in results:
            result.calcTFIDF(self.query, self.idfs)


        results = sorted(results, key=lambda result: result.rank, reverse=True)

        return results
