import hmac


def hash_passwd(passwd):
    hash_passwd = hmac.new(passwd)
    hash_passwd.update(passwd[1:5])
    return hash_passwd.hexdigest()
