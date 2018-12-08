import frontStart

def searchInReal(pre_entity):

    realmid = ''
    ifin = frontStart.realtable.find({'name': pre_entity}).sort("value", -1)

    for a in ifin:
        # print(i)
        # print(i['mid'])
        realmid = a['mid']
        break

    return realmid

def searchInAlias(pre_entity):
    aliasmid = ''
    inalias = frontStart.aliastable.find({'name': pre_entity}).sort("value", -1)

    for a in inalias:
        # print(i)
        # print(i['mid'])
        aliasmid = a['mid']
        break

    return aliasmid

def searchAllProc(pre_entity):
    realname = searchInReal(pre_entity)
    resultname=''
    if realname is not '':
        resultname=realname

    else:
        aliasname = searchInAlias(pre_entity)
        if aliasname is not '':
            resultname=aliasname

    return resultname

def findAllprobName(pre_entity):
    #print('3')
    #proname=realtable.find({'name':{'$regex':pre_entity}}).sort("value", -1)   #all contain pre_entity
    if '[' in pre_entity:
        pre_entity="\\"+pre_entity
    if '*' in pre_entity:
        pre_entity=pre_entity.replace('*','\\*')
    proname = frontStart.realtable.find({'name': {'$regex': pre_entity}}).sort("value", -1)   #all contain pre_entity
    pre_word_num = pre_entity.count(' ') + 1
    probmid=''
    probname=''

    print(proname)
    for pro in proname:

        wordnum=pro['name'].count(' ')+1
        if wordnum==pre_word_num+1 or wordnum==pre_word_num:
            probmid=pro['mid']
            probname=pro['name']
            #print(pro)
            break

    if probmid=='':
        proname = frontStart.aliastable.find({'name': {'$regex': pre_entity}}).sort("value", -1)
        for pro in proname:
            wordnum = pro['name'].count(' ') + 1
            if wordnum == pre_word_num + 1:
                probmid = pro['mid']
                probname=pro['name']
                #print(pro)
                break

    #print(probmid)
    print('==============')
    return probmid,probname

def qianzhuiSearch(pre_entity):
    qzmid=''
    pre_entity=pre_entity
    if pre_entity.count(' ') > 0:
        wordlist = pre_entity.split(' ')
        wordlen = len(wordlist)
        i = wordlen - 1
        while i > 0 and qzmid == '':
            pre_entity = ' '.join(wordlist[0:i])
            qzmid = searchAllProc(pre_entity)
            i-=1

    return qzmid,pre_entity

def houzhuiSearch(pre_entity):
    hzmid=''
    pre_entity=pre_entity
    #print(pre_entity)
    if pre_entity.count(' ')>0:
        wordlist=pre_entity.split(' ')
        wordlen=len(wordlist)
        i=1
        while i<wordlen and hzmid=='':
            pre_entity=' '.join(wordlist[i:])
            #print(pre_entity)
            hzmid=searchAllProc(pre_entity)
            i+=1

    return hzmid,pre_entity

def regexSearch(pre_entity):
    regexmid=''
    regexname=''
    if '*' in pre_entity:
        pre_entity = pre_entity.replace('*', '\\*')
    wordlist = pre_entity.split(' ')
    sqlstr='.*'.join(wordlist)

    realmid = frontStart.realtable.find({'name': {'$regex':sqlstr}}).sort("value", -1)
    for i in realmid:
        regexmid = i['mid']
        regexname=i['name']
        break
    if realmid is '':
        aliasmid = frontStart.aliastable.find({'name': {'$regex': sqlstr}}).sort("value", -1)
        for i in aliasmid:
            regexmid = i['mid']
            regexname=i['name']
            break

    return regexmid,regexname

def sameLetter(pre_entity):
    lettermid=''
    lettername=''

    pre_entity=pre_entity.replace(' ','')
    letterlist=list(pre_entity)
    print(letterlist)
    sqlstr='.?'.join(letterlist)
    print(sqlstr)
    realmid=frontStart.realtable.find({'name': {'$regex':sqlstr}}).sort("value", -1)
    for i in realmid:
        lettermid= i['mid']
        lettername=i['name']
        break
    if lettermid is '':
        aliasmid = frontStart.aliastable.find({'name': {'$regex': sqlstr}}).sort("value", -1)
        for i in aliasmid:
            lettermid = i['mid']
            lettername=i['name']
            break

    return lettermid,lettername

def FindMid(entity):
    answerlist = []
    answernamelist=[]

    #对标点的处理
    pre_entity=entity
    if '.' in pre_entity:
        pre_entity = pre_entity.replace('.', '')
    if ',' in pre_entity:
        if ' ,' in pre_entity:
            pre_entity = pre_entity.replace(' ,', '').strip()
        else:
            pre_entity = pre_entity.replace(',', '').strip()
    if ' \'s' in pre_entity:
        pre_entity = pre_entity.replace(' \'s', '\'s')
    if pre_entity.endswith('\''):
        pre_entity = pre_entity.replace('\'', '')

    #去realdict中查找
    ifinReal = searchInReal(pre_entity)
    # print(ifinReal)
    if ifinReal is not '':
        pre_mid = ifinReal
        answerlist.append(pre_mid)
        answernamelist.append(pre_entity)
        print('real===>',pre_mid)

    if len(answerlist)<4:
        #若realdict中没有，去aliasdict中查找
        ifinAlias = searchInAlias(pre_entity)
        print("ifinalias:"+ifinAlias)
        if ifinAlias is not '':
            pre_mid = ifinAlias
            if pre_mid not in answerlist:
                answerlist.append(pre_mid)
                answernamelist.append(pre_entity)
        if len(answerlist)<4:

            #去掉开头的the
            # findthe = 0
            if pre_entity.startswith('the '):
                pre_entity = pre_entity[4:len(pre_entity)]
                pre_mid=searchAllProc(pre_entity)
                if pre_mid is not '' :
                    if pre_mid not in answerlist:
                        answerlist.append(pre_mid)
                        answernamelist.append(pre_entity)
                    # findthe=1

            #若还没找到
            if len(answerlist)<4:
                #完全包含的情况
                probmid,probname = findAllprobName(pre_entity)
                print("probmid:"+probmid)
                if probmid is not '':
                    if probmid not in answerlist:
                        answerlist.append(probmid)
                        answernamelist.append(probname)
                if len(answerlist)<4:
                    # 非按顺序查找
                    pre_mid,pre_name = regexSearch(pre_entity)
                    print("regex:"+pre_mid)
                    if pre_mid is not '':
                        if pre_mid not in answerlist:
                            answerlist.append(pre_mid)
                            answernamelist.append(pre_name)
                    if len(answerlist)<4:

                        # 字母均一样，中间可能有字符 空格等
                        pre_mid,pre_name = sameLetter(pre_entity)
                        print("qianzhui:"+pre_mid)
                        if pre_mid is not '':
                            if pre_mid not in answerlist:
                                answerlist.append(pre_mid)
                                answernamelist.append(pre_name)
                        if len(answerlist)<4:
                            # 前缀匹配
                            pre_mid,pre_entity = qianzhuiSearch(pre_entity)
                            print("letter:"+pre_mid)
                            if pre_mid is not '':
                                if pre_mid not in answerlist:
                                    answerlist.append(pre_mid)
                                    answernamelist.append(pre_entity)
                            if len(answerlist)<4:

                                #后缀匹配
                                pre_mid,pre_entity=houzhuiSearch(pre_entity)
                                print("houzhui:"+pre_mid)
                                if pre_mid is not '':
                                    if pre_mid not in answerlist:
                                        answerlist.append(pre_mid)
                                        answernamelist.append(pre_entity)
                                if len(answerlist)<4:
                                    #去掉s
                                    if pre_entity.endswith('s'):
                                        pre_entity = pre_entity[:-1]
                                        pre_mid = searchAllProc(pre_entity)
                                        if pre_mid is not '':
                                            if pre_mid not in answerlist:
                                                answerlist.append(pre_mid)
                                                answernamelist.append(pre_entity)
                                        else:
                                            answerlist.append(' ')
                                    else:
                                        answerlist.append(' ')

    return answerlist,answernamelist
