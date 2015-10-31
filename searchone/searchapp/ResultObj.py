

class ResultObj():
    def __init__(self, row):
        #zero is url, one is author
        self.text = row[0] + ", " + row[1]
