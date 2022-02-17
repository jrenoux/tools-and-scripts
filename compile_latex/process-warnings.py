f = open("warnings.txt")

s = []
for l in f.readlines():
	s.append(l.replace("\n",""))
s.sort()

for e in s:
	print(e)
	
print("Total warnings:", len(s))

f.close()
