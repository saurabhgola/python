user1={
    "name":"test1",
    "email":"test1@gmail.com",
    "salary":50000, 
    "address":"indore",
}

user2={
    "name":"test2",
    "email":"test2@gmail.com",
    "salary":60000, 
    "address":"bhopal",
}


print(user1,user2)
# Iterating through keys
for key in user1:
    print(key, user1[key])

# Iterating through values
for value in user2.values():
    print(value)

# Iterating through key-value pairs
# for key, value in user1.items():
#     print(key, value)
