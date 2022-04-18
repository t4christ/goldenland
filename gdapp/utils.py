import shortuuid

def validate_input(*args):
        check_against = re.compile(r'[a-zA-Z0-9 ]*$')
        false_arr=[]
        true_arr=[]
        for val in args:
            if check_against.match(val):
                    true_arr.append(val)
                    print(true_arr)
            else:
                    false_arr.append(val)
        if len(false_arr) > 0:
                return False
        return True


def get_ip(request):
	try:
		x_forward=request.META.get("HTTP_X_FORWARDED_FOR")
		if x_forward:
			ip=x_forward.split(",")[0]
		else:ip= request.META.get("REMOTE_ADDR")
	except:
			ip=""
	return ip


def generate_referral_code():
        return shortuuid.ShortUUID().random(length=13)

