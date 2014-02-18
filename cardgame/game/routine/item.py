#coding:utf-8
#!/usr/bin/env python

from game.utility.config import config
from game.routine.drop import drop
from game.routine.vip import vip

class item:
	@staticmethod
	def use(usr, id, cnt):
		
		inv = usr.getInventory()
		it = inv.getItem(id)
		if not it:
			return {'msg' : 'item_not_exist'}
		if it['count'] < cnt:
			return {'msg': 'time_not_enough'}
				
		itemid = it['itemid']
		itemConfig = config.getConfig('item')
		itemInfo = itemConfig[itemid]		
		
		data = {}
		data['delete_item_array'] = []
		data['update_item_array'] = []		
		itemCount = cnt
		save_usr = False
		save_inv = False
		for (funkey, v) in itemInfo['fun'].items():			
			if funkey == 'treasure':
				key = None
				while itemCount > 0:
					keyitemid = v[1]
					dropid = v[0]		
					if keyitemid != '':
						key = item.get_by_itemid(inv, keyitemid)
						if not key:
							if itemCount == cnt:
								return {'msg':'key_not_exist'}
							else:
								break
						if inv.delItem(key['id']) == None:
							data['delete_item_array'].append(key['id'])
							key = None											
							
					data = drop.open(usr, dropid, data)					
					data = drop.makeData(data)					
					itemCount = itemCount - 1					
				if key:					
					data['update_item_array'].append(key)				
			elif funkey == 'protect':
				if not vip.canBuyArenaProtectTimes(usr):
					return {'msg':'vip_required'}
				
			elif funkey == 'stamina':
				if not vip.canBuyStamina(usr):
					return {'msg':'vip_required'}
				stamina = int(v[0])
				usr.chargeStamina(stamina * itemCount)
				itemCount = 0
				data['st'] = usr.stamina
				usr.vip['buy_stamina_count'] = usr.vip['buy_stamina_count'] + 1
				save_usr = True
			elif funkey == 'sp':
				if not vip.canBuyStamina(usr):
					return {'msg':'vip_required'}
				sp = int(v[0])
				usr.sp = usr.sp + sp * itemCount
				itemCount = 0
				data['sp'] = usr.sp
				usr.vip['buy_sp_count'] = usr.vip['buy_sp_count'] + 1
				save_usr = True
			elif funkey == 'arena_count':
				if not vip.canBuyArenaTimes(usr):
					return {'msg' : 'vip_required'}
				times = int(v[0])
				usr.arena['times'] = usr.arena['times'] - times * itemCount
				itemCount = 0
				data['arena_times'] = usr.arena['times']
				usr.vip['buy_arena_times'] = usr.vip['buy_arena_times'] + 1
				save_usr = True
			elif funkey == 'protect':
				pass				
			elif funkey == 'key':
				treasure = None
				while itemCount > 0:
					treasureid = v[0]				
					treasure = item.get_by_itemid(treasureid)
					if not treasure:
						if itemCount == cnt:
							return {'msg':'treasure_not_exist'}
						else:
							break
					treasureInfo = itemConfig[treasure['itemid']]
					if not treasureInfo['fun'].has_key('treasure'):
						if itemCount == cnt:
							return {'msg':'treasure_is_not'}
						else: 
							break
					dropid = treasureInfo['fun']['treasure'][0]
					data = drop.open(usr, dropid, data)
					data = drop.makeData(data)					
					if inv.delItem(treasure['id']) == None:						
						data['delete_item_array'].append(treasure['id'])
						treasure = None
					
				if treasure:					
					data['update_item_array'].append(treasure)
			elif funkey == 'medium':
				pass
		
		if inv.delItem(it['id'], cnt - itemCount) == None:
			data['delete_item_array'].append(it['id'])
		else:
			data['update_item_array'].append(it)
		save_inv = True
		if not data['delete_item_array']:
			del data['delete_item_array']
		if not data['update_item_array']:
			del data['update_item_array']
		if save_inv:
			inv.save()
		if save_usr:
			usr.save()
		return data			

				
	@staticmethod
	def get_by_itemid(inv, itemid):
		for it in inv.item:
			if it['itemid'] == itemid:
				return it
		return None
				
		