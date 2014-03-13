#coding:utf-8
#!/usr/bin/env python

from game.utility.config import config

def purchase(request):
	"""
	购买
	"""
	
	purchasenum = int(request.GET['purchase_num'])
	
	usr = request.user	
	mallPriceConf = config.getConfig('mall_price')
	
	if len(mallPriceConf) <= int(purchasenum):
		return {'msg':'puchaseid_not_exist'}
			
	mallPriceInfo = mallPriceConf[purchasenum]	
	data = {}
	if mallPriceInfo['goldPromote'] > 0:
		costGold = mallPriceInfo['goldPromote']
		if costGold > usr.gold:
			return {'msg':'gold_not_enough'}
		usr.gold = usr.gold - costGold
		data['gold'] = usr.gold
	if mallPriceInfo['gemPromote'] >0:
		costGem = mallPriceInfo['gemPromote']
		if costGem > usr.gem:
			return {'msg':'gem_not_enough'}
		usr.gem = usr.gem - costGem
		data['gem'] = usr.gem
		
	inv = usr.getInventory()
	upIt, newIt = inv.addItem(mallPriceInfo['itemid'])
	
	if upIt:
		data['update_item'] = upIt
	
	if newIt:
		data['add_item'] = newIt		
	return data