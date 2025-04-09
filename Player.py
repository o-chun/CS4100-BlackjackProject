import random


class Player():
    def __init__(self, name: str = "JackBlack", bankroll: int = 1000):
        self.name = name
        self.bankroll = bankroll
        self.score = 0
        self.rounds = 1

    def __str__(self):
        return f"Player {self.name} has score {self.score}"

    def __repr__(self):
        return f"Player({self.name})"
    
    def setBankroll(self, bankroll: int):
        self.bankroll = bankroll
    
    def betResponse(self) -> int:
        pass
    
    def hitResponse(self) -> bool:
        pass
    
    def playAgainResponse(self) -> bool:
        pass

class User(Player):
    def __init__(self, name: str = "JackBlack", bankroll: int = 1000):
        super().__init__(name, bankroll)

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
        if self.rounds < 10 and self.bankroll > 0:
            self.rounds += 1
            return True
        else:
            return False