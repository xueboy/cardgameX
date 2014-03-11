#coding:utf-8
#!/usr/bin/env python

from game.models.quest import quest

def finish(request):
	"""
	完成任务
	"""
	usr = request.user
	questid = request.GET['quest_id']	
	qt = usr.getQuest()
	return qt.finishQuest(questid)
	
def new_drama(request):
	"""
	新剧情
	"""
	usr = request.user
	dramaid = request.GET['drama_id']
	qt = usr.getQuest()
	if not qt.drama.has_key(dramaid):
		qt.drama[dramaid] = {'count':0, 'dramaid':dramaid}
	qt.drama[dramaid]['count'] = qt.drama[dramaid]['count'] + 1
	qt.save()
	return {'drama':qt.drama[dramaid]}
	
