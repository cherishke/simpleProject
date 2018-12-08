def findEntityname(question,IOBlist):
    temp = []
    entitylist=[]
    wordlist = question.split(' ')
    i = 0

    for bio in IOBlist:
        if bio == 'B' or bio == 'I':
            temp.append(wordlist[i])
        if bio == 'O':
            if len(temp) != 0:
                str = ' '.join(temp)
                entitylist.append(str)
                temp = []
        i += 1

    if len(temp)!= 0:
        str = ' '.join(temp)
        entitylist.append(str)

    if len(entitylist)!=0:
        return entitylist[0]
    else :
        return None