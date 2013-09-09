import sys
#import game.views.dungeon
#import game.views.gm
#import game.views.card
#import game.views.friend

__import__('game.views.dungeon')
__import__('game.views.gm')
__import__('game.views.card')
__import__('game.views.friend')
viewsmap = {
	'dungeon':sys.modules['game.views.dungeon'],
	'gm':sys.modules['game.views.gm'],
	'card':sys.modules['game.views.card'],
	'friend':sys.modules['game.views.friend']
}


serverid = 1