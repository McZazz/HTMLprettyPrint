import re

# read in .txt and strip each line
with open('prettyHTML_input.html', 'r') as f:
    linesInList = f.readlines()
    # lstrip = beginning, rstrip = end, strip = both
linesInList = [_.rstrip() for _ in linesInList]
newlinesinlist = ' \n'.join(linesInList)
splitList = list(newlinesinlist)
areaList = []
# splitList will stay unedited with our individual chars
# areaList starts with empty values of '---'
for _ in range(len(splitList)):
    areaList.append('---')

lasti = len(splitList) - 1

# label <!--  --> comment areas (this one must come first!!!)
flag = False
lasti = len(splitList)-1
for i, _ in enumerate(splitList):
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    if i+3 <= lasti and openn and flag == False and _ == '<' and splitList[i+1] == '!' and splitList[i+2] == '-' and splitList[i+3] == '-':
        flag = True
    elif i+2 <= lasti and openn and flag and _ == '-' and splitList[i+1] == '-' and splitList[i+2] == '>':
        areaList[i] = 'gray'
        areaList[i+1] = 'gray'
        areaList[i+2] = 'gray'
        flag = False
    if openn and flag:
        areaList[i] = 'gray'

# string areas
flag = False
lasti = len(splitList)-1
cntr = 0
for i, _ in enumerate(splitList):
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    if openn and flag == False and _ == '"':
        flag = True
    if openn and flag and _ == '"':
        cntr += 1
    # pattern start
    if i>0 and openn and flag and cntr == 1 and splitList[i-1] == '"':
        areaList[i] = "strgrn"
        areaList[i-1] = 'white'
    # pattern middle
    if openn and flag and _ != '"':
        areaList[i] = "strgrn"
    # pattern end
    if openn and i>0 and cntr == 2 and splitList[i] == '"':
        areaList[i] = "white"
    if cntr == 2:
        flag = False
        cntr = 0

# color the = and any other white things ("" alrady done)
flag = False
cntr = 0
for i, _ in enumerate(splitList):
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    if _ == '=':
        areaList[i] = 'white'

# color the tag params
lasti = len(splitList) - 1
i = lasti
flag = False
wordstarted = False
cntr = 0
while i >= 0:
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    # cant use openn here, referenceing a closed item
    if i+1 <= lasti and flag == False and wordstarted == False and areaList[i+1] == 'white' and splitList[i+1] == '"':
        flag = True
    # start of word
    if i+1 <= lasti and openn and flag and wordstarted == False and splitList[i+1] != ' ' and splitList[i+1] != '='\
    and splitList[i+1] != '"':
        areaList[i+1] = 'green'
        wordstarted = True
    if wordstarted and openn and flag and splitList[i] != ' ':
        areaList[i] = 'green'
    # end of pattern
    if i+1 <= lasti and openn and flag and wordstarted and splitList[i] == ' ' and splitList[i+1] != '"':
        areaList[i+1] = 'green'
        flag = False
        wordstarted = False
    # always at end!
    i -= 1
    # print(flag)

# label blue areas <  between >
flag = False
lasti = len(splitList)-1
cntr = 0
for i, _ in enumerate(splitList):
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    # pattern start
    if openn and flag == False and _ == '<':
        flag = True
        areaList[i] = "blue"
    # pattern middle
    if openn and flag and _ != '<' and _ != '>' and splitList[i] != ' ':
        areaList[i] = "blue"
    # pattern end
    if openn and flag and splitList[i] == '>':
        areaList[i] = "blue"
        flag = False
    # print(str(flag) + " " + _)

# label enters
for i, _ in enumerate(splitList):
    if _ == '\n':
        areaList[i] = 'enter'

# print('before getting spaces:')
testList = []
for i, _ in enumerate(splitList):
    data = areaList[i] + ' ' + _
    testList.append(data)
# print(testList)
# print()

# label spaces starting at i==0
cntr = 1
flag = False
lasti = len(splitList)-1
for i, _ in enumerate(splitList):
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    if openn and flag == False and i==0 and _ == ' ':
        flag = True
        areaList[i] = 'del'

    if openn and flag:
        areaList[i] = 'del'
        if openn and flag and i+1 <= lasti and splitList[i+1] != ' ':
            areaList[i] = str(cntr)
            splitList[i] = 'space'
            flag = False
            cntr = 1
        cntr += 1

# label spaces starting after i of 0
cntr = 1
flag = False
lasti = len(splitList)-1
for i, _ in enumerate(splitList):
    if areaList[i] == '---':
        openn = True
    else:
        openn = False

    if openn and flag == False and i>0 and splitList[i-1] == ' ' and _ == ' ':
        flag = True
        areaList[i-1] = 'del'
        cntr = 2
    if openn and flag:
        areaList[i] = 'del'
        if openn and flag and i+1 <= lasti and splitList[i+1] != ' ':
            areaList[i] = str(cntr)
            splitList[i] = 'space'
            flag = False
            cntr = 1
        cntr += 1

# replace  enters
for i, _ in enumerate(areaList):
    if areaList[i] == 'enter':
        areaList[i] = '---'
        splitList[i] = 'enter'

# print('after getting spaces and dels:')
testList = []
for i, _ in enumerate(splitList):
    data = areaList[i] + ' ' + _
    testList.append(data)
# print(testList)
# print()

#how many to delete
isdel = 0
for i, _ in enumerate(areaList):
    if _ == 'del':
        isdel += 1

# print()
# print("dels: "+ str(isdel))

delshene = True
while delshene:
    for i, _ in enumerate(areaList):
        if _ == 'del':
            areaList.pop(i)
            splitList.pop(i)
    isdel = 0
    for i, _ in enumerate(areaList):
        if _ == 'del':
            isdel += 1
    if isdel == 0:
        delshene = False
    else:
        delshene = True

# did we delete them all?
isdel = 0
for i, _ in enumerate(areaList):
    if _ == 'del':
        isdel += 1

# print('dels after del: ' + str(isdel))
# print(len(splitList))
# print(len(areaList))
# print('after deleting dels:')
testList = []
for i, _ in enumerate(splitList):
    data = areaList[i] + ' ' + _
    testList.append(data)
# print(testList)
# print()

# fill in white characters
for i, _ in enumerate(splitList):
    if areaList[i] == '---' and _ != ' ' and splitList[i] != 'enter':
        areaList[i] = 'white'

# print('before deleteing useless space b4 enter:')
# print(len(splitList))
# print(len(areaList))
testList = []
for i, _ in enumerate(splitList):
    data = str(i) + " " + areaList[i] + ' ' + _
    testList.append(data)
# print(testList)
# print()

# pop useless ' ' before enter
lasti = len(splitList)-1
for i, _ in enumerate(splitList):
    if i>0 and splitList[i-1] == ' ' and _ == '\n':
        areaList.pop(i-1)
        splitList.pop(i-1)

# print('after deleteing useless space b4 enter:')
# print(len(splitList))
# print(len(areaList))
testList = []
for i, _ in enumerate(splitList):
    data = str(i) + " " +  areaList[i] + ' ' + _
    testList.append(data)
# print(testList)
# print()

# fill in empty colors, carry over style
for i, _ in enumerate(splitList):
    if i>0 and _ == ' ' or _ == '\n':
        areaList[i] = areaList[i-1]

# replace <> with &lt; &gt; and &amp;
############################################################################################## add to cssPretty
for i, _ in enumerate(splitList):
    if _ == '<':
        splitList[i] = '&lt;'
    elif _ == '>':
        splitList[i] = '&gt;'

# print('after filling in empty colors and changing <>:')
# print(len(splitList))
# print(len(areaList))
testList = []
for i, _ in enumerate(splitList):
    data = areaList[i] + ' ' + _
    testList.append(data)
# print(testList)
# print()

# empty list for final ruleset, start and stop style
ruleList = []
for i, _ in enumerate(areaList):
    ruleList.append('---')
# first round of instruction making
for i, _ in enumerate(areaList):
    # for some reason this breaks if we
    # try elfi anywhere
    if i == 0:
        ruleList[i] = 'open'
    if i>0 and _ != areaList[i-1]:
        ruleList[i-1] = 'close'
        ruleList[i] = 'open'
    if i>1 and areaList[i-2] != areaList[i-1] and _ != areaList[i-1]:
        ruleList[i-1] = 'only'
# fix index zero errors
for i, _ in enumerate(areaList):
    # for some reason this breaks if we
    # try elif anywhere
    if i == 0:
        if i+1<=(len(areaList)-1) and areaList[i] == areaList[i+1]:
            ruleList[i] = 'open'
        else:
            ruleList[i] = 'only'

# fix final spot
for i, _ in enumerate(areaList):
    if i == len(areaList)-1:
        if areaList[i-1] == areaList[i]:
            ruleList[i] = 'close'
        elif areaList[i-1] != areaList[i]:
            ruleList[i] = 'only'

# if splitlist == space and rulelist == only or close, change to open
lasti = len(splitList)-1
for i, _ in enumerate(splitList):
    if _ == 'space' and (areaList[i] != 'blue' and areaList[i] != 'red' and areaList[i] != 'white' and areaList[i] != 'green' and \
    areaList[i] != 'strgrn' and areaList[i] != 'gray'):
        if i+1 <= lasti and ruleList[i+1] == 'open':
            ruleList[i] = 'open'
            ruleList[i+1] = '---'
        elif i+1 <= lasti and ruleList[i+1] == 'only':
            ruleList[i] = 'only'
            ruleList[i+1] = '---'

for i, _ in enumerate(splitList):
    if i>0 and ruleList[i-1] == 'close' and splitList[i] == 'enter':
        ruleList[i-1] = '---'
        ruleList[i] = 'close'
        areaList[i] = areaList[i-1]

for i, _ in enumerate(splitList):
    if i>0 and splitList[i] == 'enter' and ruleList[i] == 'only' and ruleList[i-1] == '---':
        ruleList[i] = 'close'
        areaList[i] = areaList[i-1]

# print()
# print("after rules:")
testList4 = []
for i, _ in enumerate(ruleList):
    data = str(i) + " " + areaList[i] + ' ' + _ + ' ' + splitList[i]
    testList4.append(data)
# print(testList4)

dicti = {
    'white-open': '<span class="cw">', 'red-open': '<span class="cn">', 'green-open': '<span class="fg">',
    'strgrn-open': '<span class="sg">', 'red-open': '<span class="cn">', 'green-open': '<span class="fg">',
    'tab': '<p class="t', 'gray-open': '<span class="cg">', 'white': 'cw',  'red': 'cn', 'green': 'fg',
    'strgrn': 'sg', 'gray': 'cg', 'blue': '',
}

# put in the html
htmlList=[]
for i, _ in enumerate(splitList):
    htmlList.append('---')

for i, _ in enumerate(splitList):
    opens = areaList[i] + '-' + 'open'

    if ruleList[i] == 'open':
        if (areaList[i] == 'white' or areaList[i] == 'red' or areaList[i] == 'green' or areaList[i] == 'strgrn'\
        or areaList[i] == 'gray'):
            htmlList[i] = dicti[opens] + _
        else:
            htmlList[i] = _

    elif ruleList[i] == 'close':
        if areaList[i] == 'white' or areaList[i] == 'red' or areaList[i] == 'green' or areaList[i] == 'strgrn'\
        or areaList[i] == 'gray':
            htmlList[i] = _ + '</span>'
        else:
            htmlList[i] = _
    elif ruleList[i] == 'only':
        if areaList[i] == 'white' or areaList[i] == 'red' or areaList[i] == 'green' or areaList[i] == 'strgrn'\
        or areaList[i] == 'gray':
            htmlList[i] = dicti[opens] + _ + '</span>'
        else:
            htmlList[i] = _
    elif ruleList[i] == '---':
        htmlList[i] = _
    if splitList[i] == 'enter':
        htmlList[i] = ' \n'
    if splitList[i] == 'space' and i+1 <= len(splitList):
        htmlList[i] = '<span class="t' + areaList[i] + ' ' + dicti[areaList[i+1]] + '">'

# print()
# print("html list fter hit with dictionary")
# print(htmlList)

# prepare for putting in final <p> tags
stringsdone = "".join(htmlList).split("\n")

# print()
# print("strings done b4 empty lines fixed")
# print(stringsdone)
# print()

# fix empty lines
newlist2 = []
for _ in stringsdone:
    # normal line
    if _.startswith('<p class="t') == False and _ != '\n':
        _ = '<p>' + _ + '</p>'
    # tab line
    elif _.startswith('<p class="t') == True:
        _ = _ + '</p>'
    # enter line
    if _ == '<p></p>' or _ == '<p> </p>' or _ == '<p>  </p>' or _ == '<p>    </p>' or _ == '<p>     </p>' or _ == '<p>      </p>':
        _ = '<p class="hidden">*</p>'
    newlist2.append(_)

# print()
# print("newlist2 after <p> and empty lines added")
# print(newlist2)
# print()

# save to new file
with open('prettyHTML_output.txt', 'w') as finalList:
    # this puts each list item as new line
    for _ in newlist2:
        finalList.write(_ + ' \n')
