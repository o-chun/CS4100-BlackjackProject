# CS4100-BlackjackProject
Blackjack AI Project for CS4100

Game setup:
1. Run the command "python Implementation.py" in the terminal to run the game
2. You will first be prompted how you want to play with Aces:
"Do you want to play with simple Aces (always 1) or normal Aces (1 or 11)? (s/n):"
Enter 's' to play with simplified Aces always valued at 1
or 'n' to play with normal Aces that can be valued at 1 or 11.
Note: the bots were not yet adjusted to account for the option to have aces as 11 in their decision making,
    however, if the feauture is selected, aces are defaulted to 11 if that makes the hand win before the option
    to hit or stand is prompted, so the bots (and the user) can still get blackjacks when dealt.
3. Next you will be prompted for a player type:
"Enter a player type (user/simple/rewards/greedy/value/rewards2/value2):"
Enter 'user' to play yourself or one of the various bot names to see how it plays.
By default, the game messages will only print for a 'user' player and only the end results will print for the bots.
If you want to see the game messages for the bot, switch the 'botMessages' variable in 'Implementation.py' to 'True'
4. If playing as a 'user' you will be promted to enter a name:
"Enter your name:"
Simply enter the name you want to use. This ends the game setup.
The full game setup should look similar to this:
"""
% python Implementation.py
Do you want to play with simple Aces (always 1) or normal Aces (1 or 11)? (s/n): n
Enter a player type (user/simple/rewards/greedy/value/rewards2/value2): user
Enter your name: jack
"""
5. For each round of a game, the player is first promted to make a bet.
Note: Currently, all bots only bet $1, but the user can bet any positive amount within their bankroll.
6. The player and dealer are then dealt cards and the player is prompted to hit or stay.
- If the player hits, they will be prompted again until they bust or stay.
7. The dealer will then be dealt the rest of their cards and the round will end.
8. The player will then be prompted if they want to play another round if possible.
9. The sequence of one round should look similar like this:
"""
Round # 1
Your bankroll is $ 1000
Enter your bet (minimum bet is $1): 1
Your first card is 8
Your second card is 6
You have 14
Dealer's first card is 6
The dealer has 6
Do you want to hit or stay? (hit/stay): hit
Your card is 3
You have 17
Do you want to hit or stay? (hit/stay): stay
You have chosen to stay with 17
Dealer's card is Queen
Dealer has 16
Dealer's card is 2
Dealer has 18
Dealer wins!
Your bankroll is now 999
Do you want to play again? (yes/no): yes
"""