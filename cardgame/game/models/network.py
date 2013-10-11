from gclib.object import object
from gclib.utility import currentTime

class network(object):
	
	def init(self):
		return
		
	
	def __init__(self):
		object.__init__(self)
		self.message = []
		self.mail = []
		self.email = []			
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
		data['mail'] = self.mail
		data['email'] = self.email
		data['blacklist'] = self.blacklist		
		return data		
	
	def getClientData(self):
		data = {}
		data['friends'] = self.friends
		data['friend_request'] = self.friend_request
		data['message'] = self.message
		data['mail'] = self.mail
		data['email'] = self.email
		return data
		
	def load(self, roleid, data):
		self.roleid = roleid
		self.friend_request = data['friend_request']
		self.friends = data['friends']
		self.message = data['message']
		self.mail = data['mail']
		self.email = data['email']
		
	def addFriendRequest(self, friend):
		user = self.user
		data = friend.getFriendData()
		data.update({'type':'firend_request'})
		self.email.append(data)
		self.save()
		if not user.notify.has_key('notify_email'):
			user.notify['notify_email'] = []
		user.notify['notify_email'].append(data)
		return data	
		
	def confirmFriendRequest(self, friend, isConfirm):
		
		requestEmail = None
		for email in self.email:
			if email['type'] == 'firend_request' and email['roleid'] == friend:
				requestEmail = email
				break
		
		if not requestEmail:
			return 0
		
		if isConfirm != '0':			
			
			self.addFriend(friend)
			friendNw = friend.getNetwork()
			friendNw.addFriend(self)			
			self.save()
			friend.save()			
		else:			
			self.save()
			
		self.email.remove(requestEmail)
		self.save()
		
	
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
		
	def sendMail(self, toUser, mail):
		toUserNw = toUser.getNetwork()		
		msgData = self.user.getFriendData()	
		msgData.update({'mail':mail, 'send_time': currentTime()})		
		toUserNw.mail.append(msgData)
		if not toUser.notify['notify_mail']:
			toUser.notify['notify_mail'] = []
		toUser.notify['notify_mail'].append(msgData)
		toUser.save()
		toUserNw.save()
		
		
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
		
