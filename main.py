import colorama as cl
from colorama import Fore, Style, Back, ansi
import time, sys, os, random
if os.name == 'nt':
    import msvcrt

def printw(statement, delay=2, command = lambda: True):
    if command():
        print(statement)
        time.sleep(delay)
        print("\x1b[1A\x1b[2K", end = "")

class Board:
    def __init__(self):
        self.board = ["-" for x in range(9)]
        # self.board[0] = "X"
        self.isrend = False

        # The introduction stuff
        [print("\x1b[1A\x1b[2K", end = "") for x in range(17)]
        print(ansi.clear_screen())
        print(f"{Fore.BLUE}{Style.BRIGHT}---------------Welcome to {Fore.RED}Tic-{Fore.GREEN}Tac-{Fore.LIGHTMAGENTA_EX}Toe{Fore.BLUE}---------------\n")
        print(Fore.YELLOW + "Insert your X or O in the board using these number positions :)")
        example = [[f" {z+3*(x)+1} " for z in range(3)] for x in range(3)]
        for l in example:
            print(Back.WHITE + Style.BRIGHT + Fore.GREEN + "".join(l))
        print("---------------------------------------------\n")
        v = input(Fore.LIGHTMAGENTA_EX + "Choose X (Goes first) or O (Goes Second) >>>")
        self.letter = "X" if v.upper() in ["X", "XX"] else "O" 
        self.AiLetter = "X" if self.letter is "O" else "O"
        print("\x1b[1A\x1b[2K", end = "")
        if self.AiLetter == "X":
            self.board[random.randint(0, 8)] = "X"

    def render(self, delete=4):
        if self.isrend:
            [print("\x1b[1A\x1b[2K", end = "") for x in range(delete)]
        
        self.display = [[f" {self.board[z+3*(x)]} " for z in range(3)] for x in range(3)]
        for l in self.display:
            print(Back.WHITE + Style.BRIGHT + Fore.GREEN + "".join(l) + Back.BLACK)
            self.isrend = True
    
    def getPlayerMove(self, pos):
        i = int(pos)-1
        if self.board[i]=="-":
            self.board[i] = self.letter
        else:
            raise IndexError
    
    def checkWinner(self):
        won = self.analyze(self.board)
        if won or not '-' in self.board:
            if won:
                print(f"{Fore.RED}You lost (ￗ﹏ￗ )" if won == self.AiLetter else f"{Fore.LIGHTCYAN_EX}YOU WIN :)))")
            else:
                print(Fore.YELLOW + "Thou hast drawn")
            i = input(Fore.GREEN + "would you like to play again?").lower()
            if i in ["y", "yes", "ye", "yeah"]:
                self.__init__()
                self.isrend = False
            else:
                sys.exit()
            return True
        return False

    def getAiMove(self):
        if not self.checkWinner():
            b = self.board.copy()
            value = -99
            pos = None
            for i in range(0,9):
                if(b[i] == '-'):
                    b[i] = self.AiLetter
                    score = self.minimax(False, self.AiLetter, b)
                    b[i] = '-'
                    if(score>value):
                        value=score
                        pos=i
            self.board[pos] = self.AiLetter
            return True
        else:
            return False 
    
    def analyze(self, board):
        # All the columns/diagnols which pieces can win on
        wins = [ [0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6] ];

        for i in range(0,8):
            if(board[wins[i][0]] != '-' and
            board[wins[i][0]] == board[wins[i][1]] and
            board[wins[i][0]] == board[wins[i][2]]):
                return board[wins[i][2]]
        return False

    def oppositeMark(self, m):
        if m == self.AiLetter:
            return self.letter
        else:
            self.AiLetter
    # Remember, the letter we provide is the letter we want maximized
    def minimax(self, maximizing, maximizer, board):
        # Checks to see if game has ended or not
        won = self.analyze(board)
        if won:
            return 1 if won == maximizer else -1
        elif not '-' in board:
            return 0
        
        scores = []
        for i in range(len(board)):
            if board[i] == '-':
                board[i] = maximizer if maximizing else self.oppositeMark(maximizer) 
                scores.append(self.minimax(not maximizing, maximizer, board))
                board[i] = '-'
        
        return max(scores) if maximizing else min(scores)
            
cl.init(autoreset=True)
b = Board()
while True:
    b.render(3)
    if not b.checkWinner():
        try:
            i = input(f"{Fore.GREEN}Choose your position {b.letter} >>>")
            b.getPlayerMove(i)
            b.render()
            printw(f'{Fore.RED}"{b.AiLetter}" is thinking...', 1.5, b.getAiMove)
        except:
            print("Please Enter a number 1-9 in an unoccupied space")
            time.sleep(1.5)
            if os.name == 'nt':
                while msvcrt.kbhit():
                    msvcrt.getch()
            [print("\x1b[1A\x1b[2K", end="") for x in range(2)]
