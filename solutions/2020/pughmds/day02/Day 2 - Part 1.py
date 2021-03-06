#!/usr/bin/env python
# coding: utf-8

testData = [
    "1-3 a: abcde",
    "1-3 b: cdefg",
    "2-9 c: ccccccccc"
]


def splitInput(filename):
  inputValues = []
  with open(filename, 'r') as fileStream:
    fileText = fileStream.read()
    inputStrings = fileText.split('\n')
  return inputStrings

def parseInputString(s):
    result = {
        "startnum": int(s[0:s.index("-")]),
        "endnum": int(s[s.index("-")+1:s.index(" ")]),
        "letter": s[s.index(" "):s.index(":")].strip(),
        "password": s[s.index(":")+1:].strip()
    }
    return result

def checkPassword(rule):
    neededCharacter = ''.join(c for c in rule["password"] if c == rule["letter"])
    if len(neededCharacter) >= rule["startnum"] and len(neededCharacter) <= rule["endnum"]:
        rule["valid"] = True
    else:
        rule["valid"] = False
        
    return rule
    
def validatePasswords(testData):
    correctCount = 0
    for item in testData:
        parsedPasswordRule = parseInputString(item)
        parsedPasswordRule = checkPassword(parsedPasswordRule)
        print(parsedPasswordRule)
        if parsedPasswordRule["valid"]:
            correctCount += 1
        else:
            continue
    return correctCount
    


correctCount = validatePasswords(testData)    
print("The number of correct passwords is %d out of %d " % (correctCount, len(testData)))


passwordData = splitInput("day2.txt")
correctCount = validatePasswords(passwordData)
print("The number of correct passwords is %d out of %d " % (correctCount, len(passwordData)))





