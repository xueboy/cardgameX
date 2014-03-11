#coding:utf-8
#!/usr/bin/env python
from game.routine.item import item


def use(request):
	"""
	使用道具
	"""
	usr = request.user
	id = request.GET['item_id']
	cnt = request.GET['count']
	cnt = int(cnt)
	
	return item.use(usr, id, cnt)