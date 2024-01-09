# codingame-thor2
My solution on Condingame hard puzzle Thor 2

## link to puzzle
https://www.codingame.com/training/hard/power-of-thor-episode-2

## The goal :
Thor must annihilate all the giants on the map: by striking the ground with his hammer he sends out a bolt of light which wipes out the giants which are nearby.

## Statement :
### Game Input
The program must first read the initialization data from standard input. Then, within an infinite loop, read the data from the standard input related to Thor's current state and provide to the standard output Thor's movement instructions.

### Initialization input
Line 1: 2 integers TX TY. (TX, TY) indicates Thor's starting position.

### Input for one game turn
Line 1: 2 integers H N:
H indicates the remaining number of hammer strikes.
N indicates the number of giants which are still present on the map.
N next lines: the positions X Y of the giants on the map.

### Output for one game turn
A single line, which indicates the movement or action to be carried out: WAIT STRIKE N NE E SE S SW W or NW

