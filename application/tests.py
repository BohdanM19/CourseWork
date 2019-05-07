from django.test import TestCase
import bcrypt

# Create your tests here.

hashed_pw = bcrypt.hashpw('antony'.encode(), bcrypt.gensalt())

print(hashed_pw)

print(bcrypt.hashpw('antony'.encode(), hashed_pw))





