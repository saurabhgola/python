arrlist=["sham","apple","babana","coconut"]

print(arrlist[0])
print(arrlist[1])

# append use array add new value
arrlist.append("orange")
print(arrlist)

# array value to add index

arrlist[2]="grapes"
print(arrlist)
arrlist.insert(1,"papaya")
print(arrlist)


# array value delete 
del arrlist[3]
print(arrlist)

# item lenght array
print(len(arrlist))

arrlist.reverse()
print(arrlist)

arrlist.pop()
print(arrlist)
