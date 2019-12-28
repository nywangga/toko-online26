import os

user = os.environ.get('S3_USER')
passw = os.environ.get('S3_PASS')

print(user, passw)