import sys
import game.views.dungeon
import game.views.gm

viewsmap = {
'dungeon':sys.modules['game.views.dungeon'],
'gm':sys.modules['game.views.gm']
}


serverid = 1