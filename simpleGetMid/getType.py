import frontStart

def getType(q_entity, inputquestion):
    #print(index)
    mid=q_entity  #如果识别出两个实体，选第一个作为mid
    midtype=''
    ctype=frontStart.commontable.find_one({'mid':mid})

    #若有commontype则作为其type
    if ctype is not None:
        midtype=ctype['type']
    else:
        #search othertype
        if mid =='m.02lx2r':
            midtype='music.album_release_type'
        else:
            otype=frontStart.othertable.find_one({'mid':mid})
            if otype is not None:
                typelist=otype['type']
                typelen=len(typelist)

                if typelen==1:
                    midtype='typelist[0]'

                if typelen==2 and 'common.topic' in typelist:
                    topicindex=typelist.index('common.topic')
                    # print(topicindex)
                    midtype=typelist[1-topicindex]

                #找句子中的词
                if midtype=='':
                    # q=questionlist[index-1].replace('_',' ')
                    for type in typelist:
                        if type !='common.topic':
                            everyword=re.split(r"\.|_",type)
                            for word in everyword:
                                if word in inputquestion:
                                    midtype=type
                #若还未找到，随机
                if midtype=='':
                    randomtype=choice(typelist)
                    while randomtype == 'common.topic':
                        randomtype = choice(typelist)
                    midtype=randomtype

            else:
                midtype='common.topic'
    
    return midtype