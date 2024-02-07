#!/bin/env python3

from TicTacToe import TicTacToe
from TicTacToe import Joueur


jeu = TicTacToe()
bob = Joueur('Bob',jeu,'X')
alice = Joueur('Alice',jeu,'O')




alice.joue(1,2)
bob.joue(1,1)
alice.joue(3,1)
bob.joue(3,3) 
alice.joue(2,3)
bob.joue(3,1) 
bob.joue(1,3)
alice.joue(3,2)
bob.joue(2,2)
alice.joue(2,1)

print(jeu)
print(jeu.vainqueur())

###############################################################################


# alice.joue(1,2)
# alice.joue(1,1)

# bob.joue(3,3) 
# alice.joue(2,3)
# bob.joue(3,1) 
# bob.joue(1,3)
# alice.joue(3,2)
# bob.joue(2,2)

# print(jeu)
# print(jeu.vainqueur())

###############################################################################

# alice.joue(1,2)
# alice.joue(1,1)

# bob.joue(3,3) 
# alice.joue(2,3)
# bob.joue(3,1) 
# bob.joue(1,3)
# alice.joue(3,2)
# alice.joue(2,2)

# bob.joue(2,1)
# print(jeu)
# print(jeu.vainqueur())

###############################################################################

# alice.joue(1,1)

# bob.joue(3,3) 
# alice.joue(2,3)
# bob.joue(3,1) 
# bob.joue(1,3)
# alice.joue(3,2)
# alice.joue(2,2)
# alice.joue(2,1)

# bob.joue(1,2)

# print(jeu)
# print(jeu.vainqueur())