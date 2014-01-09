#coding:utf-8
#!/usr/bin/env python

from game.utility.config import config

class item:
	@staticmethod
	def use(usr, id):
		
		inv = usr.getInventory()
		it = inv.getItem(id)
		if not it:
			return {'msg' : 'item_not_exist'}
		itemid = it['itemid']
		itemConfig = config.getConfig('item')
		itemInfo = itemConfig[itemid]
		
		
		
		data = {'delete_item_array':[]}
		for (funkey, v) in itemInfo['fun'].items():			
			if funkey == 'treasure':
				keyitemid = v[1]
				dropid = v[0]				
				key = item.get_by_itemid(inv, keyitemid)
				if not key:
					return {'msg':'key_not_exist'}			
				data = drop.open(usr, dropid, data)				
				data['delete_item_array'].append(key['id'])				
				inv.delItem(key['id'])				
			elif funkey == 'protect':
				pass
			elif funkey == 'stamina':
				stamina = v[0]
				usr.chargeStamina(stamina)				
				data['st'] = usr.stamina			
			elif funkey == 'sp':
				sp = v[0]
				usr.sp = usr.sp + sp
				data['sp'] = usr.sp
			elif funkey == 'arena_count':
				pass
			elif funkey == 'key':
				treasureid = v[0]				
				treasure = item.get_by_itemid(treasureid)
				if not treasure:
					return {'msg':'treasure_not_exist'}
				treasureInfo = itemConfig[treasure['itemid']]
				if not treasureInfo['fun'].has_key('treasure'):
					return {'treasure_is_not'}
				dropid = treasureInfo['fun']['treasure'][0]
				data = drop.open(usr, dropid, data)				
				data['delete_item_array'].append(treasure['id'])
				inv.delItem(treasure['id'])
			elif funkey == 'medium':
				pass
		data['delete_item_array'].append(it['id'])
		inv.delItem(it['id'])
		return data
		
		
				
				
				
				
				
	@staticmethod
	def get_by_itemid(inv, itemid):
		for it in inv.item:
			if it['itemid'] == itemid:
				return it
		return None
				
		