from stemming.porter2 import stem
from ResultObj import ResultObj


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
    output = []
    for term in queryterms:
        output.append(stem(term))
    return output

class QueryObj():


    def __init__(self, rawquery):
        self.rawquery = rawquery
        sanquery = sanitize(rawquery).split()
        self.query = queryfix(sanquery)
        
    def execute(self):
        results = []
        return results
