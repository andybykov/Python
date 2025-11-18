#name = input("Enter your name: ")
#print("hello", name)

userName = "Tom"
userAge = 37
user = f"name: {userName}  age: {userAge +1}"
print(user, end = "\t")   # name: Tom  age: 37
userId = 234        # тип int
print(type(userId)) # <class 'int'>

for n in range(10):
    print(n, end="\n")