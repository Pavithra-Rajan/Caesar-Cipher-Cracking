from collections import Counter

file = open("wordlist.rtf","r")
content = file.read()
content = content.replace("\n","")
content = content.replace("\\","")
content = content.replace("}","")
file.close()
#print(content)
result = Counter(content)
print ("Frequency of alphabets in word list is : " +  str(result))

alpha = "abcdefghijklmnopqrstuvwxyz"
file = open("sample.txt", "r")
content = file.read()

content.replace("\\n"," ")
content.replace("."," ")
content.replace(","," ")
content = content.lower()
#print(f"The original string is : {len(content)}")
# Bigrams Frequency in String
# Using Counter() + generator expression
res = Counter(content[idx : idx + 2] for idx in range(len(content) - 1))
#print(res)
# printing result
print(f"The original string is : {len(res)}")
new_dict = {k: v for k, v in sorted(dict(res).items(), key=lambda item: item[1])}
new__ = {}
for k, v in new_dict.items():
    if k[0] == " " or k[1]== " " or "\n" in k:
        continue
    else:
        new__[k] = v

print(new__)
print(f"The original string is : {len(new__)}")

def score(cipher):
    res = Counter(cipher[idx : idx + 2] for idx in range(len(cipher) - 1))
    return {k: v for k, v in sorted(dict(res).items(), key=lambda item: item[1])}

cipher = input()
print(score(cipher))