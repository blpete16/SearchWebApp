from stemming.porter2 import stem
from ResultObj import ResultObj
import sqlite3

DATABASEFILE = '/home/brian/Desktop/gradschool/InfoRetrieval/TwistedWebCrawler/index.db'

def buildQueryR(terms):
    if(len(terms) == 0):
        return ""
    elif(len(terms) == 1):
        return ['SELECT url, author FROM urls WHERE id IN (SELECT url_id FROM term_index WHERE term="'+terms[0]+'"', ')' ]
    else:
        vals= [' AND url_id IN (SELECT url_id FROM term_index WHERE term="'+terms[0]+'"', ')']
        subvals = buildQueryR(terms[1:])
        tvals = [subvals[0] + vals[0], subvals[1]+vals[1]]
        return tvals

def buildSQLQuery(terms):
    vals = buildQueryR(terms)
    return vals[0] + vals[1]

def execQuery(aSQLQuery):
    conn = sqlite3.connect(DATABASEFILE)
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

class QueryObj():


    def __init__(self, rawquery):
        self.rawquery = rawquery
        sanquery = sanitize(rawquery).split()
        self.query = queryfix(sanquery)
        
    def execute(self):
        sqlq = buildSQLQuery(self.query)
        
        results = execQuery(sqlq)
        return results
