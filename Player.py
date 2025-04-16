import random

class Player():
    def __init__(self, name: str = "JackBlack", bankroll: int = 1000, numWins: int = 0, numLosses: int = 0, numTies: int = 0, playerHand: int = 0):
        self.name = name
        self.bankroll = bankroll
        self.score = 0
        self.rounds = 1
        self.numWins = numWins
        self.numLosses = numLosses
        self.numTies = numTies
        self.playerHand = playerHand

    def __str__(self):
        return f"Player {self.name} has score {self.score}"

    def __repr__(self):
        return f"Player({self.name})"
    
    def setBankroll(self, bankroll: int):
        self.bankroll = bankroll
    
    def setNumWins(self, numWins: int):
        self.numWins = numWins

    def setNumLosses(self, numLosses: int):
        self.numLosses = numLosses

    def setNumTies(self, numTies: int):
        self.numTies = numTies

    def setPlayerHand(self, playerHand: int):
        self.playerHand = playerHand

    def betResponse(self) -> int:
        pass
    
    def hitResponse(self) -> bool:
        pass
    
    def playAgainResponse(self) -> bool:
        pass

class User(Player):
    def __init__(self, name: str = "JackBlack", bankroll: int = 1000, numWins: int = 0, numLosses: int = 0, numTies: int = 0):
        super().__init__(name, bankroll, numWins, numLosses, numTies)

    def betResponse(self) -> int:
        while True:
            try:
                bet = int(input(f"Enter your bet (minimum bet is $1): "))
                if bet < 1:
                    print("You can't bet less than $1!")
                elif bet > self.bankroll:
                    print(f"You can't bet more than you have! Your bankroll is ${self.bankroll}.")
                else:
                    return bet
            except ValueError:
                print("Please enter a valid number.")

    def hitResponse(self) -> bool:
        while True:
            response = input("Do you want to hit or stay? (hit/stay): ").lower()
            if response == "hit":
                return True
            elif response == "stay":
                return False
            else:
                print("Invalid response. Please enter 'hit' or 'stay'.")

    def playAgainResponse(self) -> bool:
        while True:
            response = input("Do you want to play again? (yes/no): ").lower()
            if response == "yes":
                self.rounds += 1
                return True
            elif response == "no":
                return False
            else:
                print("Invalid response. Please enter 'yes' or 'no'.")
    
class SimpleBot(Player):
    def __init__(self, name: str = "SimpleBot"):
        super().__init__(name)

    def betResponse(self) -> int:
        return 1
    
    def hitResponse(self) -> bool:
        return random.choice([True, False])
        
    def playAgainResponse(self) -> bool:
        if self.rounds < 5000 and self.bankroll > 0:
            self.rounds += 1
            return True
        else:
            print("Ended with " + str(self.bankroll) + " after " + str(self.rounds) + " rounds for a total winnings of " + str(self.bankroll - 1000) + ".")
            print("SimpleBot won " + str(self.numWins) + " times, lost " + str(self.numLosses) + " times, and tied " + str(self.numTies) + " times.")
            return False 
        
class RewardsBot(Player):
    def __init__(self, name: str = "BotRewards"):
        super().__init__(name)
        self.previousBankroll = 10000000

    def betResponse(self) -> int:
        return 1
    
    def hitResponse(self) -> bool:
        return False
    
    rewardSamples = [[2, 0, 0],[3, 0, 0], [4, 0, 0], [5, 0, 0], [6, 0, 0], [7, 0, 0], [8, 0, 0], [9, 0, 0], [10, 0, 0], [11, 0, 0], [12, 0, 0], [13, 0, 0], [14, 0, 0], [15, 0, 0], [16, 0, 0], [17, 0, 0], [18, 0, 0], [19, 0, 0], [20, 0, 0]]
    rewardEstimates = [[2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0], [11, 0], [12, 0], [13, 0], [14, 0], [15, 0], [16, 0], [17, 0], [18, 0], [19, 0], [20, 0]]
    
    def playAgainResponse(self) -> bool:
        for i in self.rewardSamples:
            if i[0] == self.playerHand and i[2] < 1000:
                if self.bankroll > self.previousBankroll:
                    i[1] += 1
                elif self.bankroll < self.previousBankroll:
                    i[1] -= 1
                i[2] += 1

        self.previousBankroll = self.bankroll

        for i in self.rewardSamples:
            if i[2] < 1000:
                self.rounds += 1
                return True      
            
        for index, j in enumerate(self.rewardEstimates):
            j[1] = self.rewardSamples[index][1] / self.rewardSamples[index][2]
            
        print(self.rewardSamples)
        print(self.rewardEstimates)
            
        return False  

class GreedyBot(Player):
    def __init__(self, name: str = "BotGreedy"):
        super().__init__(name)

    def betResponse(self) -> int:
        return 1
    
    def hitResponse(self) -> bool:
        if self.playerHand < 18:
            return True
        else:
            return False
            
    def playAgainResponse(self) -> bool:
        if self.rounds < 1000 and self.bankroll > 0:
            self.rounds += 1
            return True
        else:
            print("Ended with " + str(self.bankroll) + " after " + str(self.rounds) + " rounds for a total winnings of " + str(self.bankroll - 1000) + ".")
            print("SimpleBot won " + str(self.numWins) + " times, lost " + str(self.numLosses) + " times, and tied " + str(self.numTies) + " times.")
            return False 
            
        