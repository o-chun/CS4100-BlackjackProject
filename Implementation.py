import Player

class init():
    global bankroll 
    bankroll = 1000

    global deck
    deck = []
    def resetDeck():
        for i in range(6):
            for i in range(4):
                deck.append(("Ace", 1))
                deck.append(("2", 2))
                deck.append(("3", 3))
                deck.append(("4", 4))
                deck.append(("5", 5))
                deck.append(("6", 6))
                deck.append(("7", 7))
                deck.append(("8", 8))
                deck.append(("9", 9))
                deck.append(("10", 10))
                deck.append(("Jack", 10))
                deck.append(("Queen", 10))
                deck.append(("King", 10))
    
    resetDeck()

init()

class main():
    global bankroll
    numWins = 0
    numLosses = 0
    numTies = 0

    def deal():
        import random
        global deck 
        deckLength = len(deck)
        if deckLength < 20:
            init.resetDeck()

        rand = random.randint(0, len(deck) - 1)
        card = deck.pop(rand)
        return card
    
    # Set Player Type
    playerSetup = True
    while playerSetup:
        playerType = input("Enter a player type (user/simple/rewards/greedy): ") # User Input: Player Type
        player = None
        if playerType.lower() == "user":
            player = Player.User(input("Enter your name: "), bankroll) # User Input: Player Name
            playerSetup = False
        elif playerType.lower() == "simple":
            player = Player.SimpleBot(bankroll)
            playerSetup = False
        elif playerType.lower() == "rewards":
            bankroll = 10000000
            player = Player.RewardsBot(bankroll)
            playerSetup = False
        elif playerType.lower() == "greedy":
            player = Player.GreedyBot(bankroll)
            playerSetup = False
        else:
            print("Invalid player type. Please enter 'user', 'simple', 'rewards', or 'greedy'.")
            continue

    continuePlaying = True

    while continuePlaying:
        hit = True
        print("Round #", player.rounds)
        print("Your bankroll is $", bankroll)
        currentBet = player.betResponse() # Player Input: Bet
        if currentBet <= bankroll and currentBet >= 1:
            bankroll -= currentBet
            playerHand = 0
            dealerHand = 0
            deal1 = deal()
            print(f"Your first card is {deal1[0]}")
            playerHand += deal1[1]
            deal2 = deal()
            print(f"Your second card is {deal2[0]}")   
            playerHand += deal2[1]
            print(f"You have {playerHand}")
            deal3 = deal()
            print(f"Dealer's first card is {deal3[0]}")
            dealerHand += deal3[1]
            print(f"The dealer has {dealerHand}")

        while hit:
            if player.hitResponse(): # Player Input: Hit or Stay
                hit = True
                playerCard = deal()
                print(f"Your card is {playerCard[0]}")
                playerHand += playerCard[1]
                print(f"You have {playerHand}")
                if playerHand > 21:
                    numLosses += 1
                    print("You busted!")
                    print(f"Your bankroll is now {bankroll}")
                    hit = False
                if playerHand == 21:
                    print("You have 21, you cannot hit anymore!")
                    hit = False
            else:
                hit = False
                print(f"You have chosen to stay with {playerHand}")

        while dealerHand < 17 and playerHand <= 21:
            dealerCard = deal()
            print(f"Dealer's card is {dealerCard[0]}")
            dealerHand += dealerCard[1]
            print(f"Dealer has {dealerHand}")
            if dealerHand > 21:
                numWins += 1
                print("Dealer busted, you win!")
                bankroll += currentBet * 2
                print(f"Your bankroll is now {bankroll}")

        if playerHand <= 21:
            if playerHand > dealerHand:
                numWins += 1
                print("You win!")
                bankroll += currentBet * 2
                print(f"Your bankroll is now {bankroll}")
            elif playerHand == dealerHand:
                numTies += 1
                print("It's a tie!")
                bankroll += currentBet
                print(f"Your bankroll is now {bankroll}")
            elif playerHand < dealerHand and dealerHand <= 21: 
                numLosses += 1
                print("Dealer wins!")
                print(f"Your bankroll is now {bankroll}")

        # Update Player Bankroll for bot logic
        player.setPlayerHand(playerHand)
        player.setBankroll(bankroll)
        player.setNumWins(numWins)
        player.setNumLosses(numLosses)
        player.setNumTies(numTies)
        
        continuePlaying = player.playAgainResponse() # Player Input: Play Again

main()





        