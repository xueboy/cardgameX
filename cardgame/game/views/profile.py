import hashlib
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def set_avatar(request):
	
	gender = request.GET['gender']
	avatar = request.body	
	usr = request.user
	
	m = hashlib.md5(avatar)		
	file_name = "".join([m.hexdigest() , str(usr.roleid), ".img"])
	
	f = open(file_name, "ab")
	f.write(avatar)		
	f.close()
	return {}
		
	
	
