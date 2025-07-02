import tkinter as tk
import random

# spēle jāpalaiž no šī faila 

class GameGUI:
    def __init__(self, root):
        # Inicializē GUI ar norādīto Tkinter logu (root)
        self.root = root
        self.root.title("Skaitļa dalīšanas spēle")  # Iestata loga nosaukumu
        self.root.geometry("500x590")  # Iestata loga izmērus
        
        # Ģenerē sākuma skaitļus (5 skaitļi no 10000 līdz 20000, kuri dalās ar 2 un 3)
        self.generated_numbers = self.generate_starting_numbers()
        
        # Izveido un sakārto GUI elementus
        self.setup_ui()

        self.engine = None  # Spēles dzinējs (GameEngine instance), kas tiks inicializēts, kad spēle sāksies
    
    def generate_starting_numbers(self):
        # Atgriež 5 sākuma skaitļus, kas atbilst nosacījumiem (dalās ar 2 un 3)
        start = []
        for i in range(5):
            start.append(6*random.randint(1667, 3333))
        return start
    
    def setup_ui(self):
        # Galvenā nosaukuma etiķete
        self.frameNums = tk.Frame(self.root)
        self.frameNums.pack()

        tk.Label(self.frameNums, text="Skaitļa dalīšanas spēle", font=("Arial", 16)).pack(pady=10)
        
        # Sākuma skaitļa izvēles sadaļa
        tk.Label(self.frameNums, text="Izvēlaties sākuma ciparu:").pack()
        self.start_number_var = tk.IntVar(value=self.generated_numbers[0])  # Saglabā izvēlēto sākuma skaitli
        # Izveido radio pogas katram no ģenerētajiem skaitļiem
        for num in self.generated_numbers:
            tk.Radiobutton(self.frameNums, text=str(num), variable=self.start_number_var, value=num).pack()
        
        # Algoritma izvēles sadaļa
        tk.Label(self.frameNums, text="Izvēlaties algoritmu:").pack(pady=(10, 0))
        self.algorithm_var = tk.IntVar(value=1)  # Noklusēti: 1 = Minimax, 2 = Alpha-Beta
        self.algo_frame = tk.Frame(self.root)
        self.algo_frame.pack()
        # Izveido radio pogas algoritmu izvēlei
        tk.Radiobutton(self.algo_frame, text="Minimaks", variable=self.algorithm_var, value=1).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(self.algo_frame, text="Alfa-beta", variable=self.algorithm_var, value=2).pack(side=tk.LEFT, padx=5)


        self.player1_frame = tk.Frame(self.root)
        self.player1_frame.pack()
        tk.Label(self.player1_frame, text="Izvelaties kurš spēlē kā spēlētājs_1:").pack(pady=(10, 0))
        self.player_vs_ai = tk.BooleanVar(value=True)  # Noklusēti: 1 = Minimax, 2 = Alpha-Beta
        
        
        tk.Radiobutton(self.player1_frame, text="Cilvēks", variable=self.player_vs_ai, value=True).pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(self.player1_frame, text="Dators", variable=self.player_vs_ai, value=False).pack(side=tk.LEFT, padx=5)
        
        # Poga, lai uzsāktu spēli
        self.startButton = tk.Button(self.root, text="Sākt Spēli", command=self.start_game)
        self.startButton.pack(pady=5)
        
        # Informācijas rāmis, kurā tiks parādīts spēles statuss
        self.info = tk.Frame(self.root)
        self.info.pack(pady=10)
        
        # Etiķetes un vērtības, kas parāda pašreizējo skaitli, spēlētāja un datora punktus un kurš gājas nākamais
        tk.Label(self.info, text="Tagadējais Skaitlis:").grid(row=0, column=0)
        self.current_number = tk.Label(self.info, text="--")
        self.current_number.grid(row=0, column=1)
        
        
        tk.Label(self.info, text="Spēlētāja_1 Punkti:").grid(row=1, column=0)
        self.human_score = tk.Label(self.info, text="0")
        self.human_score.grid(row=1, column=1)
        
        tk.Label(self.info, text="Spēlētāja_2 Punkti:").grid(row=2, column=0)
        self.computer_score = tk.Label(self.info, text="0")
        self.computer_score.grid(row=2, column=1)
        
        
        # Rāmis, kurā tiek izvietotas gājiena pogas
        self.button = tk.Frame(self.root)
        self.button.pack()
        
        # Izveido pogas dalīšanai ar 2 un 3; sākotnēji tās ir atspējotas
        self.buttonDivide2 = tk.Button(self.button, text="Dalīt ar 2", state=tk.DISABLED, command=lambda: self.make_move(2))
        self.buttonDivide3 = tk.Button(self.button, text="Dalīt ar 3", state=tk.DISABLED, command=lambda: self.make_move(3))
               
        # Novieto pogas režģī
        self.buttonDivide2.grid(row=0, column=0, padx=5, pady=5)
        self.buttonDivide3.grid(row=0, column=1, padx=5, pady=5)
        
        # Restart poga, lai sāktu spēli no jauna
        #self.restartButtonFrame = tk.Frame(self.root)
        self.restart_button = tk.Button(self.root, text="Ģenerēt jaunus ciparus", command=self.restart_game)
        self.restart_button.pack(pady=10)
    
    def start_game(self):
        # Saglabā izvēlēto sākuma skaitli un algoritma vērtību
        start_number = self.start_number_var.get()
        selected_algorithm = self.algorithm_var.get()  # Iegūst vērtību: 1 = Minimax, 2 = Alpha-Beta
        player_vs_ai = self.player_vs_ai.get()
        # Inicializē spēles dzinēju (GameEngine) ar izvēlēto sākuma skaitli un algoritmu
        self.engine = GameEngine(start_number, algorithm=selected_algorithm, player_vs_ai=player_vs_ai)
        self.update_ui()  # Atjaunina GUI, lai parādītu spēles sākuma stāvokli
        
        try:
            self.labelWinner.destroy()
        except:
            pass

        if player_vs_ai:
            self.enable_move_buttons()
        else:
            self.root.after(500, self.run_computer_vs_computer)
        
    

    def enable_move_buttons(self):
        # Ieslēdz pogas, lai spēlētājs varētu veikt gājienus
        self.buttonDivide2.config(state=tk.NORMAL)
        self.buttonDivide3.config(state=tk.NORMAL)
    
    def disable_move_buttons(self):
        # Atspējo gājiena pogas
        self.buttonDivide2.config(state=tk.DISABLED)
        self.buttonDivide3.config(state=tk.DISABLED)
    
    def run_computer_vs_computer(self):
        try:
            if not self.engine.is_game_over():
                self.computer_turn()
                self.root.after(500, self.run_computer_vs_computer)
            else:
                self.end_game()
        except:
            pass

    def make_move(self, divisor):
        # Veic spēlētāja gājienu ar norādīto dalītāju (2 vai 3)
        if self.engine:
            if self.engine.make_player_move(divisor):
                self.update_ui()  # Atjaunina GUI pēc spēlētāja gājiena
                if self.engine.is_game_over():
                    self.end_game()  # Pārbauda, vai spēle ir beigusies
                else:
                    # Dod datoram nedaudz laika (500 ms), pirms izsauc datorgājienu
                    self.root.after(500, self.computer_turn)
    
    def computer_turn(self):
        # Veic datorgājienu
        
        if self.engine:
            self.engine.make_ai_move()
            
            self.update_ui()  # Atjaunina GUI pēc datorgājiena
            if self.engine.is_game_over() and self.player_vs_ai.get():
                
                self.end_game()  # Ja spēle ir beigusies, izsauc beigu funkciju
        
    
    def update_ui(self): 
        # Iegūst spēles stāvokli no GameEngine un atjaunina GUI elementus
        state = self.engine.get_state()
        self.current_number.config(text=str(state["skaitlis"]))
        
        

        if self.player_vs_ai.get():
            self.human_score.config(text=str(state["cilvēks"]))
            self.computer_score.config(text=str(state["dators"]))
        else:
            
            self.human_score.config(text=str(state["dators1"]))
            self.computer_score.config(text=str(state["dators2"]))

    
    def end_game(self):
        # Kad spēle ir beigusies, atspējo gājiena pogas un parāda rezultātu
        self.disable_move_buttons()
        state = self.engine.get_state()

        player_vs_ai = self.player_vs_ai.get()
        if player_vs_ai:
             
            if state["cilvēks"] > state["dators"]: 
                winner = "Cilvēks"
            elif state["cilvēks"] < state["dators"]:
                winner = "Dators"
            else:
                winner = "Neizšķirts"
        else:
            if state["dators1"] > state["dators2"]: 
                winner = "Dators1"
            elif state["dators1"] < state["dators2"]:
                winner = "Dators2"
            else:
                winner = "Neizšķirts"
        
       

        self.labelWinner = tk.Label(self.root, text=f"Spēle ir beigusies! Uzvarētājs: {winner}", font=("Arial", 14))
        self.labelWinner.pack()


        
    
    def restart_game(self):
        # Atiestata GUI elementus uz sākotnējo stāvokli un atiestata spēles dzinēju
        self.current_number.config(text="--")
        self.human_score.config(text="0")
        self.computer_score.config(text="0")
        self.disable_move_buttons()
        self.generated_numbers = self.generate_starting_numbers()
        
        self.destroyFrames()

        self.setup_ui()

        self.engine = None  # Notīra esošo spēles dzinēju

    def destroyFrames(self):
        self.frameNums.destroy()
        self.algo_frame.destroy()
        self.player1_frame.destroy()
        self.info.destroy()
        self.button.destroy()
        self.startButton.destroy()
        self.restart_button.destroy()
        try:
            self.labelWinner.destroy()
        except:
            pass



class gameNode:
    def __init__(self, number, player1Pts, player2Pts, currentPlayer, left, right, heuristicValue, dynamicValue):      # player1Pts = player, player2Pts = computer
        self.number = number            # player1Pts | num | player2Pts
        self.player1Pts = player1Pts    
        self.player2Pts = player2Pts                                                
        self.currentPlayer = currentPlayer    
        self.left = left   # Virsotne                                       
        self.right = right 
        self.heuristicValue = heuristicValue
        self.dynamicValue = dynamicValue
        

class gameTree:
    def __init__(self, number):
        self.root = self.build(gameNode(number, 0, 0, "player", None, None, 0, -6000), 1)
        
    

    def build(self, node, num):
        gameList = ["player","computer"]
        nt = gameList[num]

        if (node.number >= 10):
            if (num == 0):
                num = 1
                if(node.number % 2 == 0):
                    heuristicValue = node.player1Pts - node.player2Pts + 0
                    node.right = gameNode(node.number//2, node.player1Pts+2, node.player2Pts, nt, None, None, heuristicValue, -6000)
                    self.build(node.right, num)

                if(node.number % 3 == 0):
                    heuristicValue = node.player1Pts - node.player2Pts + 2
                    node.left = gameNode(node.number//3, node.player1Pts, node.player2Pts+3, nt, None, None, heuristicValue, -6000)
                    self.build(node.left, num)

            else:
                num = 0
                if(node.number % 2 == 0):
                    heuristicValue = node.player1Pts - node.player2Pts + 0
                    node.right = gameNode(node.number//2, node.player1Pts, node.player2Pts+2, nt, None, None, heuristicValue, -6000)
                    self.build(node.right, num)

                if(node.number % 3 == 0):
                    heuristicValue = node.player1Pts - node.player2Pts - 2
                    node.left = gameNode(node.number//3, node.player1Pts+3, node.player2Pts, nt, None, None, heuristicValue, -6000)
                    self.build(node.left, num)
            
            return node
    

# mimimax un alphaBeta pamat funkcijas balstās no YouTube kanāla: Sebastian Lague
def minimax(node, depth, isMaximisingPlayer):
    if (depth == 0 or ((node.left == None and node.right == None))):
        node.dynamicValue = node.heuristicValue
        return node.heuristicValue
    
    
    if isMaximisingPlayer:
        maxEval = -10000
        if (node.left != None):
            eval = minimax(node.left, depth - 1, False)
            maxEval = max(maxEval, eval)
            
        
        if (node.right != None):
            eval = minimax(node.right, depth - 1, False)
            maxEval = max(maxEval, eval)
            

        node.dynamicValue = maxEval
        return maxEval
    
    else:
        minEval = 10000
        if (node.left != None):
            eval = minimax(node.left, depth - 1, True)
            minEval = min(minEval, eval)
            
        
        if (node.right != None):
            eval = minimax(node.right, depth - 1, True)
            minEval = min(minEval, eval)
            


        node.dynamicValue = minEval
        return minEval
    

def alphaBeta(node, depth, isMaximisingPlayer, alpha, beta):
    if (depth == 0 or ((node.left == None and node.right == None))):
            node.dynamicValue = node.heuristicValue
            return node.heuristicValue
        
    if isMaximisingPlayer:
        maxEval = -10000
        if (node.left != None):
            maxEval, alpha = alphaBetaMax(node.left, depth, False, alpha, beta, maxEval)

        if (not(beta <= alpha)):
            if (node.right != None):
                maxEval, beta = alphaBetaMax(node.right, depth, False, alpha, beta, maxEval)

        node.dynamicValue = maxEval
        return maxEval
    
    else:
        minEval = 10000
        if (node.left != None):
            minEval, beta = alphaBetaMin(node.left, depth, True, alpha, beta, minEval)

        if (not(beta <= alpha)):
            if (node.right != None):
                minEval, beta = alphaBetaMin(node.right, depth, True, alpha, beta, minEval)

        
        node.dynamicValue = minEval
        return minEval
    
def alphaBetaMax(node, depth, isMaximisingPlayer, alpha, beta, maxEval):
    eval = alphaBeta(node, depth - 1, False, alpha, beta)
    maxEval = max(maxEval, eval)
    alpha = max(alpha, eval)
    
    return  maxEval, alpha

def alphaBetaMin(node, depth, isMaximisingPlayer, alpha, beta, minEval):
    eval = alphaBeta(node, depth - 1, True, alpha, beta)
    minEval = min(minEval, eval)
    beta = min(beta, eval)
    
    return minEval, beta



# Pievienotā GameEngine klase, lai varam apvienot loģiku ar GUI

# komentari šim un gui ir ģenerēti :)

class GameEngine:
    def __init__(self, start_number, algorithm=1, player_vs_ai=True):
        # Inicializē spēles dzinēju ar sākuma skaitli, algoritma izvēli un spēles režīmu (cilvēks pret datoru)
        # algorithm: 1 = minimax, 2 = alphaBeta
        self.tree = gameTree(start_number)  # Izveido spēles koku, izmantojot start_number kā sākuma vērtību
        self.current = self.tree.root       # Saglabā sākuma stāvokli no koka saknes
        self.player_vs_ai = player_vs_ai    # Saglabā informāciju par to, vai spēle ir cilvēks pret datoru
        self.algorithm = algorithm          # Saglabā izvēlēto algoritmu (1 vai 2)    
        self.traversedNodes = 0

    def get_state(self):
        # Atgriež pašreizējo spēles stāvokli kā vārdnīcu, ko var izmantot GUI interfeisā
        if self.player_vs_ai:
            return {
                "skaitlis": self.current.number,         # Pašreizējais skaitlis
                "cilvēks": self.current.player1Pts,      # Spēlētāja punkti
                "dators": self.current.player2Pts,       # Datora punkti
            }
        else:
            return {
                "skaitlis": self.current.number,         # Pašreizējais skaitlis
                "dators1": self.current.player1Pts,      # Spēlētāja punkti
                "dators2": self.current.player2Pts,      # Datora punkti
            }

    def is_game_over(self):
        # Pārbauda, vai spēle ir beigusies:
        # Spēle beidzas, ja pašreizējais skaitlis ir mazāks vai vienāds ar 10 vai ja skaitli vairs nevar dalīt ar 2 vai 3.
        return self.current.number <= 10 or (self.current.number % 2 != 0 and self.current.number % 3 != 0)

    def make_player_move(self, divisor):
        
        # Veic spēlētāja gājienu, ja tas ir atļauts:
        # Pārbauda, vai nākamais gājiens ir spēlētājam un vai pašreizējais skaitlis dalās ar norādīto divisor (2 vai 3).
        if self.current.currentPlayer == "player" and self.current.number % divisor == 0 :
            self.current.number //= divisor  # Dalās ar divisor, atjaunojot skaitli
            # Pāriet uz atbilstošo apakšmezglu (koka mezglu) atkarībā no izvēlētā dalītāja
            if divisor == 3 and self.current.left is not None:
                self.current = self.current.left
            elif divisor == 2 and self.current.right is not None:
                self.current = self.current.right
            return True  # Gājiens veiksmīgi izpildīts
      
        return False  # Ja nosacījumi netiek izpildīti, gājiens nav veiksmīgs

    def make_ai_move(self):
        # Veic datora (AI) gājienu, ja nākamais gājiens ir "computer" tad minimizē, ja "player" tad maximizē
        isMaximising = False
        if self.current.currentPlayer == "computer":
            isMaximising = False
        else:
            isMaximising = True


        goTroughAlgorythm = True        
        try:
            if (self.current.left.dynamicValue == self.current.dynamicValue and not (self.current.dynamicValue == -6000)):
                if not (self.current.left.dynamicValue == -6000):
                    goTroughAlgorythm = False
                else:
                    goTroughAlgorythm = True
        except:
            pass

        try:    
            if self.current.right.dynamicValue == self.current.dynamicValue and not (self.current.dynamicValue == -6000): 
                if not (self.current.right.dynamicValue == -6000):
                    goTroughAlgorythm = False
                else:
                    goTroughAlgorythm = True
        except:
            pass


        SEARCH_DEPTH = 10
        if goTroughAlgorythm:

            if self.algorithm == 1:
                eval = minimax(self.current, SEARCH_DEPTH, isMaximising) 

            else:
                eval = alphaBeta(self.current, SEARCH_DEPTH, isMaximising, -10000, 10000)

       
        # Pārbauda, kurš apakšmezgls atbilst aprēķinātajam vērtējumam:

        # Ja Kreisais (dalīšana ar 3) apakšmezgls ir derīgs un tā dinamiskā vērtība sakrīt ar pašreizējo, tad veic gājienu
        if self.current.left is not None and self.current.left.dynamicValue == self.current.dynamicValue:
            self.current.number //= 3
            self.current = self.current.left

        # Pretējā gadījumā, ja labo (dalīšana ar 3) apakšmezgls atbilst, tad veic gājienu        
        elif self.current.right is not None and self.current.right.dynamicValue == self.current.dynamicValue:
            self.current.number //= 2
            self.current = self.current.right
        
        
        
   


if __name__ == "__main__":
    root = tk.Tk()           # Izveido galveno Tkinter logu
    game_gui = GameGUI(root) # Inicializē GameGUI klasi ar logu
    root.mainloop()          # Sāk Tkinter galveno notikumu cilpu
