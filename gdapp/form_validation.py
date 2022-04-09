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

# def db_validation_check(*args):
