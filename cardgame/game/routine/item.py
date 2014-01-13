#coding:utf-8
#!/usr/bin/env python

from game.utility.config import config

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
		for (funkey, v) in itemInfo['fun'].items():			
			if funkey == 'treasure':
				key = None
				while itemCount > 0:
					keyitemid = v[1]
					dropid = v[0]				
					key = item.get_by_itemid(inv, keyitemid)
					if not key:
						if itemCount == cnt:
							return {'msg':'key_not_exist'}
						else:
							break
					data = drop.open(usr, dropid, data)				
					data['delete_item_array'].append(key['id'])
					itemCount = itemCount - 1
					if inv.delItem(key['id']) == None:
						data['delete_item_array'].append(key['id'])
						key = None
				if key:					
					data['update_item_array'].append(key)
			elif funkey == 'protect':
				pass
			elif funkey == 'stamina':
				stamina = int(v[0])
				usr.chargeStamina(stamina * itemCount)
				itemCount = 0
				data['st'] = usr.stamina			
			elif funkey == 'sp':
				sp = int(v[0])
				usr.sp = usr.sp + sp * itemCount
				itemCount = 0
				data['sp'] = usr.sp
			elif funkey == 'arena_count':
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
		if not data['delete_item_array']:
			del data['delete_item_array']
		if not data['update_item_array']:
			del data['update_item_array']
		
		return data			

				
	@staticmethod
	def get_by_itemid(inv, itemid):
		for it in inv.item:
			if it['itemid'] == itemid:
				return it
		return None
				
		