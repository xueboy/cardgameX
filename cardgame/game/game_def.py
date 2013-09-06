import sys
import game.views.dungeon
import game.views.gm
import game.views.card
import game.views.friend

viewsmap = {
	'dungeon':sys.modules['game.views.dungeon'],
	'gm':sys.modules['game.views.gm'],
	'card':sys.modules['game.views.card'],
	'friend':sys.modules['game.views.friend']
}


serverid = 1