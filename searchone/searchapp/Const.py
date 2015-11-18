PGFOLDER = '/home/brian/Desktop/gradschool/InfoRetrieval/DataStore/FullPages/'

DATABASEFILE = '/home/brian/Desktop/gradschool/InfoRetrieval/DataStore/index.db'

LOGFILE = 'questionfile.txt'

def log(val):
    pass
    #with open (LOGFILE, 'a') as afile:
    #    afile.write(str(val.encode("ascii", "ignore")) + "\n")


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
