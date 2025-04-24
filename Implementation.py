import Player
from math import floor

botMessages = False # To toggle bot messages
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
    player = None
    isAceSimple = True
    while playerSetup:
        aceResponse = input("Do you want to play with simple Aces (always 1) or normal Aces (1 or 11)? (s/n): ")
        isAceSimple = aceResponse.lower() == "simple" or aceResponse.lower() == "s"
        playerType = input("Enter a player type (user/simple/rewards/greedy/value/rewards2/value2): ") # User Input: Player Type
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
        elif playerType.lower() == "value":
            player = Player.ValueBot(bankroll)
            playerSetup = False
        elif playerType.lower() == "rewards2":
            bankroll = 1000000000000
            player = Player.DealerRewardsBot(bankroll)
            playerSetup = False
        elif playerType.lower() == "value2":
            player = Player.DealerValueBot(bankroll)
            playerSetup = False
        else:
            print("Invalid player type. Please enter 'user', 'simple', 'rewards', 'greedy', 'value', 'rewards2', or 'value2'.")
            continue

    player.setIsAceSimple(isAceSimple)
    continuePlaying = True

    while continuePlaying:
        if bankroll == 0:
            print("You are out of money!")
            continuePlaying = False
            break
        print("Round #", player.rounds)
        print("Your bankroll is $", bankroll)
        currentBet = player.betResponse() # Player Input: Bet
        if currentBet <= bankroll and currentBet >= 1:
            bankroll -= currentBet
            playerHand = 0
            dealerHand = 0
            playerAceHand = 0
            dealerAceHand = 0
            dealerCardCount = 0
            playerBlackjack = False
            dealerBlackjack = False
            deal1 = deal()
            hit = True
            if (type(player) == Player.User or botMessages): # First player card
                print(f"Your first card is {deal1[0]}")
            if deal1[0] == "Ace" and not isAceSimple:
                player.addPlayerAce()
            playerHand += deal1[1]
            deal2 = deal()
            if (type(player) == Player.User or botMessages): # Second player card
                print(f"Your second card is {deal2[0]}")   
            if deal2[0] == "Ace" and not isAceSimple:
                player.addPlayerAce()
            playerHand += deal2[1]
            player.setPlayerHand(playerHand)
            if not isAceSimple:
                if player.getPlayerAces() > 0:
                    playerAceHand = playerHand + 10
            if (type(player) == Player.User or botMessages):
                if playerAceHand == 21:
                    print("You have 21. Blackjack!")
                    hit = False
                    playerBlackjack = True
                else:
                    print(f"You have {playerHand}")
                    if player.getPlayerAces() > 0 and not isAceSimple and playerAceHand < 21:
                        print(f"or {playerAceHand} with an Ace as 11")
            deal3 = deal()
            dealerCardCount += 1
            if (type(player) == Player.User or botMessages): # First dealer card
                print(f"Dealer's first card is {deal3[0]}")
            if deal3[0] == "Ace" and not isAceSimple:
                player.addDealerAce()
            dealerHand += deal3[1]
            player.setDealerHand(dealerHand)
            if (type(player) == Player.User or botMessages):
                print(f"The dealer has {dealerHand}")

        while hit:
            if player.hitResponse(): # Player Input: Hit or Stay
                hit = True
                playerCard = deal()
                if playerCard[0] == "Ace" and not isAceSimple:
                    player.addPlayerAce()
                if (type(player) == Player.User or botMessages):
                    print(f"Your card is {playerCard[0]}")
                playerHand += playerCard[1]
                player.setPlayerHand(playerHand)
                if (type(player) == Player.User or botMessages):
                    print(f"You have {playerHand}")
                if player.getPlayerAces() > 0:
                    playerAceHand = playerHand + 10
                    if playerAceHand < 21:
                        if (type(player) == Player.User or botMessages):
                            print(f"or {playerAceHand} with an Ace as 11")
                if playerHand > 21:
                    numLosses += 1
                    if (type(player) == Player.User or botMessages):
                        print("You busted!")
                        print(f"Your bankroll is now {bankroll}")
                    hit = False
                elif playerHand == 21 or playerAceHand == 21:
                    if (type(player) == Player.User or botMessages):
                        print("You have 21, you cannot hit anymore!")
                    hit = False
            else:
                hit = False
                if (type(player) == Player.User or botMessages):
                    print(f"You have chosen to stay with {playerHand}")

        while dealerHand < 17 and dealerAceHand < 17 and playerHand <= 21:
            dealerCard = deal()
            dealerCardCount += 1
            if (type(player) == Player.User or botMessages):
                print(f"Dealer's card is {dealerCard[0]}")
            dealerHand += dealerCard[1]
            if dealerCard[0] == "Ace" and not isAceSimple:
                player.addDealerAce()
            if (type(player) == Player.User or botMessages):
                print(f"Dealer has {dealerHand}")
            if player.getDealerAces() > 0:
                dealerAceHand = dealerHand + 10
                if dealerAceHand == 21 and dealerCardCount == 2:
                    dealerBlackjack = True
                    if (type(player) == Player.User or botMessages):
                        print(f"or {dealerAceHand} with an Ace as 11")
                elif dealerAceHand <= 21:
                    if (type(player) == Player.User or botMessages):
                        print(f"or {dealerAceHand} with an Ace as 11")
            else:
                dealerAceHand = dealerHand
            if dealerHand > 21:
                numWins += 1
                if (type(player) == Player.User or botMessages):
                    print("Dealer busted, you win!")
                if playerBlackjack:
                    bankroll += floor(currentBet * 2.5)
                else:
                    bankroll += currentBet * 2
                if (type(player) == Player.User or botMessages):
                    print(f"Your bankroll is now {bankroll}")

        if playerHand <= 21:
            if not isAceSimple:
                if playerAceHand <= 21 and playerAceHand > playerHand:
                    playerHand = playerAceHand
                if dealerAceHand <= 21 and dealerAceHand > dealerHand:
                    dealerHand = dealerAceHand
            if playerHand > dealerHand:
                numWins += 1
                bankroll += currentBet * 2
                if (type(player) == Player.User or botMessages):
                    print("You win!")
                    print(f"Your bankroll is now {bankroll}")
            elif playerHand < dealerHand and dealerHand <= 21: 
                numLosses += 1
                if (type(player) == Player.User or botMessages):
                    print("Dealer wins!")
                    print(f"Your bankroll is now {bankroll}")
            elif playerHand == dealerHand:
                if playerBlackjack and not dealerBlackjack:
                    numWins += 1
                    bankroll += floor(currentBet * 2.5)
                    if (type(player) == Player.User or botMessages):
                        print("You have blakcjack, you win!")
                        print(f"Your bankroll is now {bankroll}")
                elif dealerBlackjack:
                    numLosses += 1
                    if (type(player) == Player.User or botMessages):
                        print("Dealer has blackjack, you lose!")
                        print(f"Your bankroll is now {bankroll}")
                numTies += 1
                bankroll += currentBet
                if (type(player) == Player.User or botMessages):
                    print("It's a tie!")
                    print(f"Your bankroll is now {bankroll}")

        # Update Player Bankroll for bot logic
        player.setPlayerHand(playerHand)
        player.setBankroll(bankroll)
        player.setNumWins(numWins)
        player.setNumLosses(numLosses)
        player.setNumTies(numTies)
        player.setDealerAces(0)
        player.setPlayerAces(0)
        
        continuePlaying = player.playAgainResponse() # Player Input: Play Again

main()





        