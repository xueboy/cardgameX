import hashlib


def set_avatar(request):
	
	sex = request.GET['sex']
	avatar = request.body
	usr = request.user
	
	m = md5.new(avatar)		
	file_name = string.join(m.hexdigest() , str(usr.roleid), ".png")
	
	f = open(file_name, "ab")
	for chunk in avatar.chunks():
		f.write(chunk)		
	f.close()
		
	
	
