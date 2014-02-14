#coding:utf-8
#!/usr/bin/env python

from game.utility.config import config
from game.routine.luck import luck

class pvp:
	
	@staticmethod
	def almanacPvpProperty(usr):
		
		al = usr.getAlmanac()
		
		combinaionConf = config.getConfig('almanac_combination')
		
		ppData = {}
		ppData['attack'] = 0
		ppData['hp'] = 0
		ppData['pd'] = 0
		ppData['md'] = 0
		ppData['pt'] = 0		
		ppData['pr'] = 0
		ppData['mr'] = 0
		ppData['critical'] = 0
		ppData['tenacity'] = 0
		ppData['block'] = 0
		ppData['wreck'] = 0
		ppData['hit'] = 0
		ppData['dodge'] = 0
		ppData['pa'] = 0		
		ppData['strength'] = 0
		ppData['intelligence'] = 0
		ppData['artifice'] = 0
		ppData['pi'] = 0		
		ppData['pe'] = 0
		
		
		
		for cb in al.combine:
			if st['typestr'] == 'strenghth':
				ppData['strenghth'] = ppData['strenghth'] + st['val']
			elif st['typestr'] == 'intelligence':
				ppData['intelligence'] = ppData['intelligence'] + st['val']
			elif st['typestr'] == 'artifice':
				ppData['artifice'] = ppData['artifice'] + st['val']
			elif st['typestr'] == 'attack':
				ppData['attack'] = ppData['attack'] + st['val']
			elif st['typestr'] == 'hp':
				ppData['hp'] = ppData['hp'] + st['val']
			elif st['typestr'] == 'critical':
				ppData['critical'] = ppData['critical'] + st['val']
			elif st['typestr'] == 'tenacity':
				ppData['tenacity'] = ppData['tenacity'] + st['val']
			elif st['typestr'] == 'dodge':
				ppData['dodge'] = ppData['dodge'] + st['val']
			elif st['typestr'] == 'hit':
				ppData['hit'] = ppData['hit'] + st['val']
			elif st['typestr'] == 'block':
				ppData['block'] = ppData['block'] + st['val']
			elif st['typestr'] == 'wreck':
				ppData['wreck'] = ppData['wreck'] + st['val']
			elif st['typestr'] == 'pt':
				ppData['pt'] = ppData['pt'] + st['val']			
			elif st['typestr'] == 'pd':
				ppData['pd'] = ppData['pd'] + st['val']
			elif st['typestr'] == 'md':
				ppData['md'] = ppData['md'] + st['val']
			elif st['typestr'] == 'criticallv':
				ppData['criticallv'] = ppData['criticallv'] + st['val']
			elif st['typestr'] == 'tenacitylv':
				ppData['tenacity'] = ppData['tenacity'] + st['val']
			elif st['typestr'] == 'dodgelv':
				ppData['dodgelv'] = ppData['dodgelv'] + st['val']
			elif st['typestr'] == 'hitlv':
				ppData['hitlv'] = ppData['hitlv'] + st['val']
			elif st['typestr'] == 'blocklv':
				ppData['blocklv'] = ppData['blocklv'] + st['val']
			elif st['typestr'] == 'wrecklv':
				ppData['wrecklv'] = ppData['wrecklv'] + st['val']
			elif st['typestr'] == 'speed':
				ppData['speed'] = ppData['speed'] + st['val']
				
		return ppData
		
	@staticmethod
	def medalPvpProperty(usr):
		
		inv = usr.getInventory()
		
		medalConfig = config.getConfig('medal')
		
		ppData = {}
		ppData['attack'] = 0
		ppData['hp'] = 0
		ppData['pd'] = 0
		ppData['md'] = 0
		ppData['pt'] = 0		
		ppData['pr'] = 0
		ppData['mr'] = 0
		ppData['critical'] = 0
		ppData['tenacity'] = 0
		ppData['block'] = 0
		ppData['wreck'] = 0
		ppData['hit'] = 0
		ppData['dodge'] = 0
		ppData['pa'] = 0		
		ppData['strength'] = 0
		ppData['intelligence'] = 0
		ppData['artifice'] = 0
		ppData['pi'] = 0		
		ppData['pe'] = 0
		
			
		for medalid in inv.medal:
			
			if medalConfig[medalid]['typestr'] == 'strenghth':
				ppData['strenghth'] = ppData['strenghth'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'intelligence':
				ppData['intelligence'] = ppData['intelligence'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'artifice':
				ppData['artifice'] = ppData['artifice'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'attack':
				ppData['attack'] = ppData['attack'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'hp':
				ppData['hp'] = ppData['hp'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'critical':
				ppData['critical'] = ppData['critical'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'tenacity':
				ppData['tenacity'] = ppData['tenacity'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'dodge':
				ppData['dodge'] = ppData['dodge'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'hit':
				ppData['hit'] = ppData['hit'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'block':
				ppData['block'] = ppData['block'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'wreck':
				ppData['wreck'] = ppData['wreck'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'pt':
				ppData['pt'] = ppData['pt'] + medalConfig[medalid]['val']			
			elif medalConfig[medalid]['typestr'] == 'pd':
				ppData['pd'] = ppData['pd'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'md':
				ppData['md'] = ppData['md'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'criticallv':
				ppData['criticallv'] = ppData['criticallv'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'tenacitylv':
				ppData['tenacity'] = ppData['tenacity'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'dodgelv':
				ppData['dodgelv'] = ppData['dodgelv'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'hitlv':
				ppData['hitlv'] = ppData['hitlv'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'blocklv':
				ppData['blocklv'] = ppData['blocklv'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'wrecklv':
				ppData['wrecklv'] = ppData['wrecklv'] + medalConfig[medalid]['val']
			elif medalConfig[medalid]['typestr'] == 'speed':
				ppData['speed'] = ppData['speed'] + medalConfig[medalid]['val']		
		
		return ppData
		
	@staticmethod
	def practicePvpProperty(usr):
		ppData = {}
		ppData['attack'] = 0
		ppData['hp'] = 0
		ppData['pd'] = 0
		ppData['md'] = 0
		ppData['pt'] = 0		
		ppData['pr'] = 0
		ppData['mr'] = 0
		ppData['critical'] = 0
		ppData['tenacity'] = 0
		ppData['block'] = 0
		ppData['wreck'] = 0
		ppData['hit'] = 0
		ppData['dodge'] = 0
		ppData['pa'] = 0		
		ppData['strength'] = 0
		ppData['intelligence'] = 0
		ppData['artifice'] = 0
		ppData['pi'] = 0		
		ppData['pe'] = 0		
		
		practicePropertyConf = config.getConfig('practice_property')
		
		if usr.practice['critical_level'] > 0:
			ppData[critical] = practicePropertyConf[usr.practice['critical_level']]
		if usr.practice['tenacity_level'] > 0:
			ppData[tenacity] = practicePropertyConf[usr.practice['tenacity_level']]
		if usr.practice['block_level'] > 0:
			ppData[block] = practicePropertyConf[usr.practice['block_level']]
		if usr.practice['wreck_level'] > 0:
			ppData[wreck] = practicePropertyConf[usr.practice['wreck_level']]
			
		return ppData
		
	@staticmethod
	def luckPvpProperty(usr, card):
		ppData = {}
		ppData['attack'] = 0
		ppData['hp'] = 0
		ppData['pd'] = 0
		ppData['md'] = 0
		ppData['pt'] = 0		
		ppData['pr'] = 0
		ppData['mr'] = 0
		ppData['critical'] = 0
		ppData['tenacity'] = 0
		ppData['block'] = 0
		ppData['wreck'] = 0
		ppData['hit'] = 0
		ppData['dodge'] = 0
		ppData['pa'] = 0		
		ppData['strength'] = 0
		ppData['intelligence'] = 0
		ppData['artifice'] = 0
		ppData['pi'] = 0		
		ppData['pe'] = 0		
		
		petConf = config.getConfig('pet')
		luckConf = config.getConfig('luck')
	
		for luckdata in petConf[card['cardid']]['luck']:
			luckid = luck.check(usr, card, petConf)		
			
			luckInfo = luckConf[luckid]
			
		
			if luckInfo['typestr'] == 'strenghth':
				ppData['strenghth'] = ppData['strenghth'] + luckInfo['value']
			elif luckInfo['typestr'] == 'intelligence':
				ppData['intelligence'] = ppData['intelligence'] + luckInfo['value']
			elif luckInfo['typestr'] == 'artifice':
				ppData['artifice'] = ppData['artifice'] + luckInfo['value']
			elif luckInfo['typestr'] == 'attack':
				ppData['attack'] = ppData['attack'] + luckInfo['value']
			elif luckInfo['typestr'] == 'hp':
				ppData['hp'] = ppData['hp'] + luckInfo['value']
			elif luckInfo['typestr'] == 'critical':
				ppData['critical'] = ppData['critical'] + luckInfo['value']
			elif luckInfo['typestr'] == 'tenacity':
				ppData['tenacity'] = ppData['tenacity'] + luckInfo['value']
			elif luckInfo['typestr'] == 'dodge':
				ppData['dodge'] = ppData['dodge'] + luckInfo['value']
			elif luckInfo['typestr'] == 'hit':
				ppData['hit'] = ppData['hit'] + luckInfo['value']
			elif luckInfo['typestr'] == 'block':
				ppData['block'] = ppData['block'] + luckInfo['value']
			elif luckInfo['typestr'] == 'wreck':
				ppData['wreck'] = ppData['wreck'] + luckInfo['value']
			elif luckInfo['typestr'] == 'pt':
				ppData['pt'] = ppData['pt'] + luckInfo['value']			
			elif luckInfo['typestr'] == 'pd':
				ppData['pd'] = ppData['pd'] + luckInfo['value']
			elif luckInfo['typestr'] == 'md':
				ppData['md'] = ppData['md'] + luckInfo['value']
			elif luckInfo['typestr'] == 'criticallv':
				ppData['criticallv'] = ppData['criticallv'] + luckInfo['value']
			elif luckInfo['typestr'] == 'tenacitylv':
				ppData['tenacity'] = ppData['tenacity'] + luckInfo['value']
			elif luckInfo['typestr'] == 'dodgelv':
				ppData['dodgelv'] = ppData['dodgelv'] + luckInfo['value']
			elif luckInfo['typestr'] == 'hitlv':
				ppData['hitlv'] = ppData['hitlv'] + luckInfo['value']
			elif luckInfo['typestr'] == 'blocklv':
				ppData['blocklv'] = ppData['blocklv'] + luckInfo['value']
			elif luckInfo['typestr'] == 'wrecklv':
				ppData['wrecklv'] = ppData['wrecklv'] + luckInfo['value']
			elif luckInfo['typestr'] == 'speed':
				ppData['speed'] = ppData['speed'] + luckInfo['value']
				
		return ppData
		
		
	@staticmethod
	def mergePvpProperty(p1, p2):
		ppData = p1.copy()
		ppData['attack'] = p1['attack'] + p2['attack']
		ppData['hp'] = p1['hp'] + p2['hp']
		ppData['pd'] = p1['pd'] + p2['pd']
		ppData['md'] = p1['md'] + p2['md']
		ppData['pt'] = p1['pt'] + p2['pt']		
		ppData['pr'] = p1['pr'] + p2['pr']
		ppData['mr'] = p1['mr'] + p2['mr']
		ppData['critical'] = p1['critical'] + p2['critical']
		ppData['tenacity'] = p1['tenacity'] + p2['tenacity']
		ppData['block'] = p1['block'] + p2['block']
		ppData['wreck'] = p1['wreck'] + p2['wreck']
		ppData['hit'] = p1['hit'] + p2['hit']
		ppData['dodge'] = p1['dodge'] + p2['dodge']
		ppData['pa'] = p1['pa'] + p2['pa']		
		ppData['strength'] = p1['strength'] + p2['strength']
		ppData['intelligence'] = p1['intelligence'] + p2['intelligence']
		ppData['artifice'] = p1['artifice'] + p2['artifice']
		ppData['pi'] = p1['pi'] + p2['pi']		
		ppData['pe'] = p1['pe'] + p2['pe']
		return ppData
		
		
	@staticmethod
	def pvpPetProperty(card, petConf):
		
		petInfo = petConf[card['cardid']]
		
		star = card['init_start'] + int(card['level'] * 0.4)
		
		ppData = {}
		ppData['attack'] = petInfo['attack'] + petInfo['attackgrowth'] * (card['level'] + star * 5)  * 0.5		
		ppData['hp'] = petInfo['hp'] + petInfo['hpgrowth'] * (card['level'] + star * 5) * 0.5		
		ppData['pd'] = 0
		ppData['md'] = 0
		ppData['pt'] = 0		
		ppData['pr'] = petInfo['pr'] + star * petInfo['prgrowth']
		ppData['mr'] = petInfo['mr'] + star * petInfo['mrgrowth']
		ppData['critical'] = petInfo['critical']
		ppData['tenacity'] = petInfo['tenacity']
		ppData['block'] = petInfo['block']
		ppData['wreck'] = petInfo['wreck']
		ppData['hit'] = petInfo['hit']
		ppData['dodge'] = petInfo['dodge']		
		ppData['strength'] = petInfo['strength']
		ppData['intelligence'] = petInfo['intelligence']
		ppData['artifice'] = petInfo['artifice']
		ppData['pi'] = 0		
		ppData['pa'] = petInfo['pa'] + petInfo['pagrowth'] * star		
		ppData['id'] = card['id']
		ppData['cardid'] = card['cardid']
		ppData['pe'] = 0
		return ppData
		