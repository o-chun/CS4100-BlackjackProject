import random
import json
import os

class Player():
    def __init__(self, name: str = "JackBlack", bankroll: int = 1000, numWins: int = 0, numLosses: int = 0, numTies: int = 0, playerHand: int = 0, dealerHand: int = 0):
        self.name = name
        self.bankroll = bankroll
        self.startingBankroll = bankroll
        self.score = 0
        self.rounds = 1
        self.numWins = numWins
        self.numLosses = numLosses
        self.numTies = numTies
        self.playerHand = playerHand
        self.dealerHand = dealerHand

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

    def setDealerHand(self, dealerHand: int):
        self.dealerHand = dealerHand

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
    def __init__(self, name: str = "SimpleBot", bankroll: int = 1000):
        super().__init__(name, bankroll)

    def betResponse(self) -> int:
        return 1
    
    def hitResponse(self) -> bool:
        return random.choice([True, False])
        
    def playAgainResponse(self) -> bool:
        if self.rounds < 1000 and self.bankroll > 0:
            self.rounds += 1
            return True
        else:
            print("Ended with " + str(self.bankroll) + " after " + str(self.rounds) + " rounds for a total winnings of " + str(self.bankroll - self.startingBankroll) + ".")
            print("SimpleBot won " + str(self.numWins) + " times, lost " + str(self.numLosses) + " times, and tied " + str(self.numTies) + " times.")
            return False
        
class RewardsBot(Player):
    def __init__(self, name: str = "BotRewards", bankroll: int = 10000000):
        super().__init__(name, bankroll)
        self.previousBankroll = 10000000
        self.dataFile = "rewardData.json"
        self.loadData()

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
                self.saveData()
                return True      
            
        for index, j in enumerate(self.rewardEstimates):
            j[1] = self.rewardSamples[index][1] / self.rewardSamples[index][2]
            
        print(self.rewardSamples)
        print(self.rewardEstimates)
        self.saveData()
        return False  
    
    def saveData(self):
        data = {
            "rewardSamples": self.rewardSamples,
            "rewardEstimates": self.rewardEstimates
        }
        with open(self.dataFile, "w") as f:
            json.dump(data, f)

    def loadData(self):
        if os.path.exists(self.dataFile):
            with open(self.dataFile, "r") as f:
                data = json.load(f)
                self.rewardSamples = data.get("rewardSamples", self.rewardSamples)
                self.rewardEstimates = data.get("rewardEstimates", self.rewardEstimates)
        else:
            self.rewardSamples = [[i, 0, 0] for i in range(2, 21)]
            self.rewardEstimates = [[i, 0] for i in range(2, 21)]

class GreedyBot(Player):
    def __init__(self, name: str = "BotGreedy", bankroll: int = 1000):
        super().__init__(name, bankroll)

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
            print("Ended with " + str(self.bankroll) + " after " + str(self.rounds) + " rounds for a total winnings of " + str(self.bankroll - self.startingBankroll) + ".")
            print("GreedyBot won " + str(self.numWins) + " times, lost " + str(self.numLosses) + " times, and tied " + str(self.numTies) + " times.")
            return False 
            
        
class ValueBot(Player):
    def __init__(self, name: str = "BotData", bankroll: int = 1000, rewardFile="rewardData.json"):
        super().__init__(name, bankroll)
        self.gamma = 0.85 # Find good balance 
        self.epsilon = 0.001
        self.policy = {}
        self.V = {}
        self.R = {}
        self.loadEstimates(rewardFile)
        self.runValueIteration()

    def betResponse(self) -> int:
        return 1

    def hitResponse(self) -> bool:
        handTotal = self.playerHand
        #if self.rounds % 100 == 0: # Update policy every 100 rounds (don't think this affects it currently)
        #    self.runValueIteration() # Could be useful when changing up betting depending on current bankroll or counting cards)
        return self.policy.get(handTotal, False)

    def playAgainResponse(self) -> bool:
        if self.rounds < 1000 and self.bankroll > 0:
            self.rounds += 1
            return True
        else:
            print("Ended with " + str(self.bankroll) + " after " + str(self.rounds) + " rounds for a total winnings of " + str(self.bankroll - self.startingBankroll) + ".")
            print("ValueBot won " + str(self.numWins) + " times, lost " + str(self.numLosses) + " times, and tied " + str(self.numTies) + " times.")
            return False

    def loadEstimates(self, rewardFile):
        try:
            with open(rewardFile, "r") as f:
                reward_data = json.load(f)
                rewardEstimates = reward_data.get("rewardEstimates")
                self.R = {int(item[0]): float(item[1]) for item in rewardEstimates if 2 <= item[0] <= 20}
        except FileNotFoundError:
            print("Reward file not found. Make sure RewardsBot has saved it first.")
            self.R = {s: 0.0 for s in range(2, 21)}
        
    def runValueIteration(self):
        self.V = {s: 0.0 for s in range(2, 21)}
        maxIterations = 10000

        for i in range(maxIterations):
            delta = 0
            newV = self.V.copy()
            for s in range(2, 21):
                standVal = self.R[s]

                hitVal = 0
                for card in range(1, 14):  # Cards 1 to 13
                    if card > 10: # face cards
                        card = 10
                    next_s = s + card
                    if next_s > 21:
                        hitVal += -1.0 * 1/13  # bust
                    else:
                        hitVal += self.V.get(next_s, 0.0) * 1/13  # expected value
                hitVal = self.gamma * hitVal

                newV[s] = max(standVal, hitVal)
                delta = max(delta, abs(newV[s] - self.V[s]))
            self.V = newV

            if delta < self.epsilon:
                break

        # Form policy
        for s in range(2, 21):
            standVal = self.R[s]

            hitVal = 0
            for card in range(1, 14):
                if card > 10:
                    card = 10
                next_s = s + card
                if next_s > 21:
                    hitVal += -1.0 * 1/13
                else:
                    hitVal += self.V.get(next_s, 0.0) * 1/13
            hitVal = self.gamma * hitVal

            self.policy[s] = hitVal > standVal

class DealerRewardsBot(Player):
    def __init__(self, name: str = "BotDealerRewards", bankroll: int = 1000000000000):
        super().__init__(name, bankroll)
        self.previousBankroll = 1000000000000
        self.dataFile = "dealerRewardData.json"
        self.loadData()

    def betResponse(self) -> int:
        return 1
    
    def hitResponse(self) -> bool:
        return False
    
    dealerRewardSamples = []
    for i in range (2, 21):
        for j in range (2):
            dealerRewardSamples.append([i, j, 0, 0])

    dealerRewardEstimates = []
    for i in range (2, 21):
        for j in range (2):
            dealerRewardEstimates.append([i, j, 0])
    
    def playAgainResponse(self) -> bool:
        if self.dealerHand < 7:
            dealer = 0 # Dealer is showing an Ace, 2, 3, 4, 5, or 6
        else:
            dealer = 1 # Dealer is showing a 7, 8, 9, or 10

        for i in self.dealerRewardSamples:
            if i[0] == self.playerHand and i[1] == dealer and i[3] < 1000:
                if self.bankroll > self.previousBankroll:
                    i[2] += 1
                elif self.bankroll < self.previousBankroll:
                    i[2] -= 1
                i[3] += 1

        self.previousBankroll = self.bankroll

        for i in self.dealerRewardSamples:
            if i[3] < 1000:
                self.rounds += 1
                self.saveData()
                return True      
            
        for index, i in enumerate(self.dealerRewardEstimates):
            i[2] = self.dealerRewardSamples[index][2] / self.dealerRewardSamples[index][3]
            
        print(self.dealerRewardSamples)
        print(self.dealerRewardEstimates)
        self.saveData()
        return False  
    
    def saveData(self):
        data = {
            "dealerRewardSamples": self.dealerRewardSamples,
            "dealerRewardEstimates": self.dealerRewardEstimates
        }
        with open(self.dataFile, "w") as f:
            json.dump(data, f)

    def loadData(self):
        if os.path.exists(self.dataFile):
            with open(self.dataFile, "r") as f:
                data = json.load(f)
                self.dealerRewardSamples = data.get("dealerRewardSamples", self.dealerRewardSamples)
                self.dealerRewardEstimates = data.get("dealerRewardEstimates", self.dealerRewardEstimates)
        else:
            self.dealerRewardSamples = [[i, j, 0, 0] for i in range(2, 21) for j in range(2)]
            self.dealerRewardEstimates = [[i, j, 0] for i in range(2, 21) for j in range(2)]

class DealerValueBot(Player):
    def __init__(self, name: str = "BotDealerValue", bankroll: int = 1000, rewardFile="dealerRewardData.json"):
        super().__init__(name, bankroll)
        self.gamma = 0.9 # Find good balance 
        self.epsilon = 0.001
        self.policy = {}
        self.V = {}
        self.R = {}
        self.loadEstimates(rewardFile)
        self.runValueIteration()

    def betResponse(self) -> int:
        return 1

    def hitResponse(self) -> bool:
        handTotal = self.playerHand
        if self.dealerHand < 7:
            dealerCard = 0
        else:
            dealerCard = 1

        return self.policy.get((handTotal, dealerCard))

    def playAgainResponse(self) -> bool:
        if self.rounds < 1000 and self.bankroll > 0:
            self.rounds += 1
            return True
        else:
            print("Ended with " + str(self.bankroll) + " after " + str(self.rounds) + " rounds for a total winnings of " + str(self.bankroll - self.startingBankroll) + ".")
            print("ValueBot2 won " + str(self.numWins) + " times, lost " + str(self.numLosses) + " times, and tied " + str(self.numTies) + " times.")
            return False

    def loadEstimates(self, rewardFile):
        try:
            with open(rewardFile, "r") as f:
                reward_data = json.load(f)
                rewardEstimates = reward_data.get("dealerRewardEstimates")
                self.R = {(int(item[0]), int(item[1])): float(item[2]) for item in rewardEstimates if 2 <= item[0] <= 20}
        except FileNotFoundError:
            print("Reward file not found. Make sure RewardsBot has saved it first.")
            self.R = {(p, d): 0.0 for p in range(2, 21) for d in range(2)}
        
    def runValueIteration(self):
        self.V = {(p,d): 0.0 for p in range(2, 21) for d in range(2)}
        maxIterations = 10000

        for i in range(maxIterations):
            delta = 0
            newV = self.V.copy()
            for p in range(2, 21):
                for d in range(2):
                    standVal = self.R[(p,d)]

                    hitVal = 0
                    for card in range(1, 14):  # Cards 1 to 13
                        if card > 10: # face cards
                            card = 10
                        next_p = p + card
                        if next_p > 21:
                            hitVal += -1.0 * 1/13  # bust
                        else:
                            hitVal += self.V.get((next_p, d), 0.0) * 1/13  # expected value
                    hitVal = self.gamma * hitVal

                    newV[(p,d)] = max(standVal, hitVal)
                    delta = max(delta, abs(newV[(p,d)] - self.V[(p,d)]))
            self.V = newV

            if delta < self.epsilon:
                break

        # Form policy
        for p in range(2, 21):
            for d in range(2):
                standVal = self.R[(p,d)]

                hitVal = 0
                for card in range(1, 14):
                    if card > 10:
                        card = 10
                    next_p = p + card
                    if next_p > 21:
                        hitVal += -1.0 * 1/13
                    else:
                        hitVal += self.V.get((next_p, d), 0.0) * 1/13
                hitVal = self.gamma * hitVal
                self.policy[(p,d)] = hitVal > standVal

        print(self.policy)