from gclib.object import object
from gclib.utility import currentTime

class network(object):
	
	def init(self):
		return
		
	
	def __init__(self):
		object.__init__(self)
		self.message = []				
		self.gift = {}						#{roleid:'#depend'}
		self.jail = {}						#[{'roleid':'', 'name':'abc'}]
		self.friends = {}
		self.friend_request = {}
		self.blacklist = []
		self.user = None
		
	def getData(self):
		data = {}
		data['friend_request'] = self.friend_request
		data['friends'] = self.friends
		data['message'] = self.message
		data['blacklist'] = self.blacklist
		return data		
	
	def getClientData(self):
		data = {}
		data['friends'] = self.friends
		data['friend_request'] = self.friend_request
		data['message'] = self.message
		return data
		
	def load(self, roleid, data):
		self.roleid = roleid
		self.friend_request = data['friend_request']
		self.friends = data['friends']
		self.message = data['message']
		
	def addFriendRequest(self, friend):
		data = friend.getFriendData()
		self.friend_request[friend.roleid] = data
		self.save()
		return data	
		
	def confirmFriendRequest(self, friend, isConfirm):
		
		if isConfirm != '0':
			if len(self.friends) >= 2:			
				return 0
			
			self.addFriend(friend)
			friend.addFriend(self)
			del self.friend_request[str(friend.roleid)]
			self.save()
			friend.save()
			return friend.roleid
		else:
			del self.friend_request[str(friend.roleid)]
			self.save()
			return friend.roleid
	
	def addFriend(self, friend):
		self.friends[str(friend.roleid)] =  friend.getFriendData()
	
	def getFriend(self, friendRoleid):
		if self.friends.has_key(str(friendRoleid)):
			return friends[str(friendRoleid)]


	def sendMessage(self, toUser, msg):
		toUserNw = toUser.getNetwork()
		fromUserId = str(self.roleid)		
		msgData = self.user.getFriendData()
		msgData.update({'message':msg, 'send_time': currentTime()})
		toUserNw.message.append(msgData)		
		if not toUser.notify.has_key('notify_message'):
			toUser.notify['notify_message'] = []
		toUser.notify['notify_message'].append(msgData)
		toUser.save()
		toUserNw.save()
		
	def talk(self, toUser, msg):
		toUserNw = toUser.getNetwork()		
		msgData = self.user.getFriendData()	
		msgData.update({'message':msg, 'send_time': currentTime()})		
		if not toUser.notify['notify_talk']:
			toUser.notify['notify_talk'] = []
		toUser.notify['notify_talk'].append(msgData)
		toUser.save()
		
		
	def ban(self, ben_roleid, ben_name):
		self.blacklist.append({'roleid':ben_roleid, 'name':ben_name, 'create_time':currentTime()})
			
	def updateBlacklist(self):
		gameConf = config.getConfig('game')
		expire = gameConf['blacklist_expiry_date']
		now = currentTime()		
		self.blacklist = filter(lambda ban: ban['create_time'] + exp > now, self.blacklist)
			
	def isBan(self, ban_roleid):
		self.updateBlacklist()
		for ban in self.blacklist:
			if ban['roleid'] == ban_roleid:
				return True
		return False
		
