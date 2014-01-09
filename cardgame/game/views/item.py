#coding:utf-8
#!/usr/bin/env python
from game.routine.item import item


def use(request):
	usr = request.user
	id = request.GET['item_id']
	
	return item.use(usr, id)