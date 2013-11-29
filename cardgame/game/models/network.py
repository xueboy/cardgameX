from gclib.object import object
from gclib.utility import currentTime
from game.utility.config import config


class network(object):
	
	def init(self):
		return
		
	
	def __init__(self):
		object.__init__(self)
		self.message = {}
		self.mail = {}
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
		data['friend'] = self.friend
		data['message'] = self.message
		data['mail'] = self.mail
		data['email'] = self.email
		data['blacklist'] = self.blacklist
		data['sequenceid'] = self.sequenceid
		return data		
	
	def getClientData(self):	
		
		avatarmap = {}		
		for key in self.message:
			otherid = self.message[key]['roleid']
			if not avatarmap.has_key(otherid):
				usr = self.user.__class__.get(otherid)
				if usr:
					avatarmap[otherid] = usr.avatar_id
			self.message[key]['avatar_id'] = avatarmap[otherid]				
		data = {}
		data['friend'] = self.friend	
		data['message'] = self.message
		data['mail'] = self.mail
		data['email'] = self.email
		return data
		
	def load(self, roleid, data):
		object.load(self, roleid, data)
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
		requestid = str(toUserNw.sequenceid)
		toUserNw.sequenceid = toUserNw.sequenceid + 1
		msgData = self.user.getFriendData()		
		msgData.update({'message':msg, 'send_time': currentTime(), 'id':requestid})
		toUserNw.message[requestid] = msgData
		if not toUser.notify.has_key('notify_message'):
			toUser.notify['notify_message'] = {}
		toUser.notify['notify_message'][requestid] = msgData
		toUser.save()
		toUserNw.save()
	
	def deleteMessage(self, messageid):
		if self.message.has_key(messageid):
			del self.message[messageid]
			self.save()
	
	def updateMessage(self):
		now = currentTime()
		gameConf = config.getConfig('game')
		expire = gameConf['message_expiry_period']
		self.message = dict((k, v) for k,v in self.message.items() if (v['send_time'] + expire) > now)
		
		
	def sendMail(self, toUser, mail):
		toUserNw = toUser.getNetwork()		
		msgData = self.user.getFriendData()	
		requestid = str(toUserNw.sequenceid)
		toUserNw.sequenceid = toUserNw.sequenceid + 1
		msgData.update({'mail':mail, 'send_time': currentTime(), 'id':requestid})		
		toUserNw.mail[requestid] = msgData
		if not toUser.notify.has_key('notify_mail'):
			toUser.notify['notify_mail'] = {}
		toUser.notify['notify_mail'][requestid] = msgData
		toUser.save()
		toUserNw.save()
		
		
	def ban(self, ben_roleid, ben_name):
		self.blacklist.append({'roleid':ben_roleid, 'name':ben_name, 'create_time':currentTime()})
			
	def updateBlacklist(self):
		gameConf = config.getConfig('game')
		expire = gameConf['blacklist_expiry_period']
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
			
	def updateFriendData(self):
		for friendid in self.friend:
			fNw = network.get(friendid)
			strRoleid = str(self.roleid)
			if fNw.friend.has_key(strRoleid):
				fNw.friend[strRoleid] = self.user.getFriendData()
				fNw.save()
			
		
	def emailAnswerFriendRequest(self, mail, option):
		if option == 'yes':
			friendid = mail['roleid']
			if self.friend.has_key(friendid):
				return {'msg':'friend_not_exist'}
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
	
	def emailMarkReaded(self, emailid):
		if not self.email.has_key(emailid):
			return {'msg':'email_not_exist'}
		self.email[emailid]['readed'] = True
		self.save()
		return self.email[emailid]		
		
		
	def emailDelete(self, emailid):
		if self.email.has_key(emailid):
			del self.email[emailid]
			self.save()
			return {'email_delete':emailid}
		return {'msg':'email_not_exist'}

	def yell(self, name, msg):
		ms = massyell.get(0)		
		return ms.yell(self.roleid, name, msg)
		
		
