
filename = input()
textfile = open(filename, "r")
String = textfile.read()
p1 = ""
p2 = ""

for i in range(len(String)):
    if i%2 == 0:
        l1 = [p1, String[i]]
        p1 = " ".join(l1)
    else:
        l2 = [p2, String[i]]
        p2 = " ".join(l2)


print(p1)
print(p2)