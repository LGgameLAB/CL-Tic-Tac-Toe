import re
# XO Board
# 1 2 3
# 4 5 6
# 7 8 9
def getBoolFromList(l):
    for i in l:
        if not i:
            return False
    return True

def checkWin(state, letter):
    rows = [state[0:3],state[3:6],state[6:9]]
    columns = [[rows[y][rows.index(x)] for y in range(3)] for x in rows]
    diagonals = [[rows[y][y] for y in range(3)], [rows[-y-1][y] for y in range(3)]]
    def replace(l):
        new = []
        for i in l:
            new.append(True if i == letter else False)
        return new
        
    for i in map(getBoolFromList, map(replace, rows+columns+diagonals)):
        if i:
            return True

    return False

def getLogicX(state):
    states  = {
        '''
        XO-
        ---
        ---
        ''': 5,
        '''
        X-O
        ---
        ---
        ''': 7,
        '''
        X--
        O--
        ---
        ''': 5,
        '''
        X--
        -O-
        ---
        ''': 9,
        '''
        X--
        --O
        ---
        ''': 5,
        '''
        X--
        ---
        O--
        ''': 3,
        '''
        X--
        ---
        -O-
        ''': 5,
        '''
        X--
        ---
        --O
        ''': 3,
        '''
        XO-
        ---
        ---
        ''': 5,
        '''
        XOO
        -X-
        ---
        ''': 9,
        '''
        XO-
        -XO
        ---
        ''': 9,
        '''
        XO-
        OX-
        ---
        ''': 9,
        '''
        XO-
        -X-
        O--
        ''': 9,
        '''
        XO-
        -X-
        -O-
        ''': 9,
        

        
    }
    
    for s in states:
        if re.sub(r"[\n\t\s]*", "", s) == state:
            return states[s]