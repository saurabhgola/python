a=10
age=18
sum=10+20
if age >= 18:
    print("you are sure vote")
else:
        print("not for vot")
for i in range(5):
    print(i)
print(sum,type(a),"this is first programmar")

fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)

# test index number    
for index,fruit in enumerate(fruits):
    print(fruit,index)

print(10+30 ,f"test is the loop{fruits}")
print(f"sum of two numbers{10+20}")

a=[1,2,7,23,89,90,31,14,2,9,6,7]
b=[]
for i in a:
     if i%2==0:
        b.append(i)
        print(b)