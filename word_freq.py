from collections import Counter

file = open("wordlist.rtf","r")
content = file.read()
content = content.replace("\n","")
content = content.replace("\\","")
content = content.replace("}","")
#print(content)
result = Counter(content)
print ("Frequency of alphabets in word list is : " +  str(result))