# alpha-gomoku

This program plays Gomoku game, which is explained in the following link.
https://en.wikipedia.org/wiki/Gomoku

A board state is expresed as a feature, which consists of a 3 dimensional vector (player, length, status).
Player represents 1st and 2nd players, respectively as 1 and 2. Length means a consecutive line's length. Finally status expreses how both sides of the line are open. If both sides are open (means not occupied yet), the status is 2. Status=1 means just one side is open, and 0 means both sides are already occupied by the opponent. 

Each board feature is socred by the evaluation of the 2 step ahead state, and the evaluation is done by the current hypothesis. If the game is won by the player, the final state is scored as 100. in case of a lost game, the value is -100. As a game finishs, each step of the game is evaluated in that way. After that, your hypothesis is adjusted to minimize the total error. It's a usual Least Mean Squared error. Gradient Descent is used for find the minimal. 

The basic idea comes from chapter 1 of this book.
https://www.amazon.com/Machine-Learning-Tom-M-Mitchell/dp/0070428077
