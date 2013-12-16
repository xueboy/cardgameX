#coding:utf-8
#!/usr/bin/env python

from game.models.quest import quest

def finish(request):	
	usr = request.user
	questid = request.GET['quest_id']	
	qst = usr.getQuest()
	return qst.finishQuest(questid)
	
