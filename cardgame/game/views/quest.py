#coding:utf-8
#!/usr/bin/env python

from game.models.quest import quest

def finish(request):	
	usr = request.user
	questid = request.GET['quest_id']	
	qt = usr.getQuest()
	return qt.finishQuest(questid)
	
def new_drama(request):
	usr = request.user
	dramaid = request.GET['drama_id']
	qt = usr.getQuest()
	if not qt.drama.has_key(dramaid):
		qt.drama[dramaid] = {'count':0, 'dramaid':dramaid}
	qt.drama[dramaid]['count'] = qt.drama[dramaid]['count'] + 1
	qt.save()
	return {'drama':pt.drama[dramaid]}
	
