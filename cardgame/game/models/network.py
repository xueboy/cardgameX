from gclib.object import object
from gclib.utility import currentTime


class network(object):
	
	def init(self):
		return
		
	
	def __init__(self):
		object.__init__(self)
		self.message = []
		self.mail = []
		self.email = {}			
		self.gift = {}						#{roleid:'#depend'}
		self.jail = {}						#[{'roleid':'', 'name':'abc'}]
		self.friend = {}
		self.friend_request = {}
		self.blacklist = []
		self.sequenceid = 1
		self.user = None
		
	def getData(self):
		data = {}
		data['friend_request'] = self.friend_request
		data['friend'] = self.friend
		data['message'] = self.message
		data['mail'] = self.mail
		data['email'] = self.email
		data['blacklist'] = self.blacklist
		data['sequenceid'] = self.sequenceid
		return data		
	
	def getClientData(self):
		data = {}
		data['friend'] = self.friend
		data['friend_request'] = self.friend_request
		data['message'] = self.message
		data['mail'] = self.mail
		data['email'] = self.email
		return data
		
	def load(self, roleid, data):
		self.roleid = roleid
		self.friend_request = data['friend_request']
		self.friend = data['friend']
		self.message = data['message']
		self.mail = data['mail']
		self.email = data['email']
		self.sequenceid = data['sequenceid']
		
		
	def addFriendRequest(self, friend):		
		data = self.user.getFriendData()
		friendNw = friend.getNetwork()
		requestid = str(friendNw.sequenceid)
		friendNw.sequenceid = friendNw.sequenceid + 1
		data.update({'type':'firend_request', 'id':requestid})		
		friendNw.email[requestid] = data		
		friendNw.save()
		if not friend.notify.has_key('notify_email'):
			friend.notify['notify_email'] = {}
		friend.notify['notify_email'][requestid] = data
		friend.save()		
		return data	
		
	def addFriend(self, friend):
		data = friend.getFriendData()
		self.friend[str(friend.roleid)] =  data
		return data
				
	def deleteFriend(self, friend):
		if self.friend.has_key(friend.roleid):
			del self.friend[friend.roleid]
			self.save()
		else:
			return {'msg':'friend_not_exist'}
		otherNw = friend.getNetwork()
		selfroleid = str(self.roleid)
		if otherNw.friend.has_key(selfroleid):
			del otherNw.friend[str(selfroleid)]			
			otherNw.save()
			return {'friend_delete':friend.roleid}
		
			
	def getFriend(self, friendRoleid):
		if self.friends.has_key(str(friendRoleid)):
			return friends[str(friendRoleid)]

	def sendMessage(self, toUser, msg):		
		self.updateMessage()
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
	
	def updateMessage(self):
		now = currentTime()
		gameConf = config.getConfig('game')
		expire = gameConf['message_expiry_date']
		self.message = filter(lambda x:(x['send_time'] + expire) > now)
		
		
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
		
	def emailAnswer(self, id, option):
		
		if not self.email.has_key(id):
			return {'msg':'email_not_exist'}
		email = self.email[id]
		if email['type'] == 'firend_request':
			return self.emailAnswerFriendRequest(email, option)
			
		
	def emailAnswerFriendRequest(self, mail, option):
		if option == 'yes':
			friendid = mail['roleid']
			if self.friend.has_key(friendid):
				return {'msg':','}
			friend = self.user.get(friendid)
			friendData = self.addFriend(friend)

			friendNw = friend.getNetwork()
			friendNw.addFriend(self.user)
			mailid = mail['id']
			del self.email[mailid]
			self.save()
			friendNw.save()
			return {'email_delete':mailid, 'friend_new':friendData}
		elif option == 'no':
			del self.email[mail['id']]		
			self.save()
			return {'email_delete':mailid}
		return {}
	
	def emailMarkReaded(self, mail):
		mail['readed'] = True
		self.save()
