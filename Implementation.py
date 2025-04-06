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

    def deal():
        import random
        global deck 
        deckLength = len(deck)
        if deckLength < 20:
            init.resetDeck()

        rand = random.randint(0, len(deck) - 1)
        card = deck.pop(rand)
        return card
    
    continuePlaying = True

    while continuePlaying:
        hit = True
        bet = input("Enter your bet (minimum bet is $1): ")
        currentBet = int(bet)
        if currentBet > bankroll:
            print("You can't bet more than you have!")
            currentBet = input(f"Enter your bet under {bankroll}: ")
        elif currentBet < 1:
            print("You can't bet less than $1!")
            currentBet = input("Enter your bet (minimum bet is $1): ")
        if currentBet < bankroll and currentBet >= 1:
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
            playerChoice = input("Do you want to hit or stay?")
            if playerChoice == "hit" or playerChoice == "Hit":
                hit = True
                deal = deal()
                print(f"Your card is {deal[0]}")
                playerHand += deal[1]
                print(f"You have {playerHand}")
                if playerHand > 21:
                    print("You busted!")
                    print(f"Your bankroll is now {bankroll}")
                    nextRound = input("Do you want to play again?")
                    if nextRound == "yes" or nextRound == "Yes":
                        continuePlaying = True
                    else:
                        continuePlaying = False
            else:
                hit = False
                print(f"You have chosen to stay with {playerHand}")

        while dealerHand < 17:
            dealerCard = deal()
            print(f"Dealer's card is {dealerCard[0]}")
            dealerHand += dealerCard[1]
            print(f"Dealer has {dealerHand}")
            if dealerHand > 21:
                print("Dealer busted, you win!")
                bankroll += currentBet * 2
                print(f"Your bankroll is now {bankroll}")
                nextRound = input("Do you want to play again?")
                if nextRound == "yes" or nextRound == "Yes":
                    continuePlaying = True
                else:
                    continuePlaying = False

        if playerHand > dealerHand:
            print("You win!")
            bankroll += currentBet * 2
            print(f"Your bankroll is now {bankroll}")
            nextRound = input("Do you want to play again?")
            if nextRound == "yes" or nextRound == "Yes":
                continuePlaying = True
            else:
                continuePlaying = False
        elif playerHand == dealerHand:
            print("It's a tie!")
            bankroll += currentBet
            print(f"Your bankroll is now {bankroll}")
            nextRound = input("Do you want to play again?")
            if nextRound == "yes" or nextRound == "Yes":
                continuePlaying = True
            else:
                continuePlaying = False
        else:
            print("Dealer wins!")
            print(f"Your bankroll is now {bankroll}")
            nextRound = input("Do you want to play again?")
            if nextRound == "yes" or nextRound == "Yes":
                continuePlaying = True
            else:
                continuePlaying = False

main()





        