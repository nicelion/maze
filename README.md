# maze
Ian's maze.


## How to play
Use the arrow keys to control the player throughout the maze.

### Objective

The objective of the game is to complete the maze in the quickest amount of time, while collecting as many coins as possible.

## Switches

Some coins may appear to be behind walls. To fix this, you first must find the switch, switch it, and then you can retrieve your coin.

### High Scores

High scores can be found under the 'High Scores' section on the start screen.
At the end of a round and the player has the highest score, or within the top three, they will be asked to enter their enitials, and will be saved to the 'high_scores.txt' file, in the respected position.

### Scoring

The score is calculated very carefully and with a very complex equation.

The game uses a multiplier system. Below is the code in how the multiplyer system works.

    # let time represent the players elapsed time in game play
    if time >= 60:
        multiplier = 1
    if time <= 50 and time >= 40:
        multiplier = 0.5
    if time <= 49 and time >= 30:
        multiplier = 2
    if time <= 29 and time >= 15:
        multiplier = 3
    if time < 15:
        multiplier = 5

Then, the final score is calculated by the folloing equation:

    # let coins_collected be the amount of coins the player has collected in the game
    return (coins_collected * multiplier) + 100


## To Do

* ~~Doors~~ (Added 12/15/16)
* Saving functionality in the high score.
* Second player
* Making game 'endable' by completing the maze, not collecting all the coins.
