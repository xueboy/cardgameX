#coding:utf-8
#!/usr/bin/env python

from django.http import HttpResponse
from game.models.user import user

	
def tool_create_player(request):
	if request.method == 'POST':
		levelf = request.POST['levelf']
		levelt = request.POST['levelt']
		cnt = request.POST['count']
		main_card_dropid = request.POST['main_card_dropid']
		other_card_dropid = request.POST['other_card_dropid']
		card_levelf = request.POST['card_levelf']
		card_levelt = request.POST['card_levelt']
		equip_strenght_levelf = request.POST['equip_strenght_levelf']
		equip_strenght_levelt = request.POST['equip_strenght_levelt']
		skill_levelf = request.POST['skill_levelf']
		skill_levelt = request.POST['skill_levelt']
		stone_levelf = request.POST['stone_levelf']
		stone_levelt = request.POST['stone_levelt']
		
		for i in range(cnt):
			pass
			
		
	return HttpResponse('tool_create_player')