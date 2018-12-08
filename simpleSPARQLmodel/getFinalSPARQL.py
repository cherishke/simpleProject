#coding=utf-8
import re

def getSimpleSPARQL(type_pattern,q_entity):
    patternlist=type_pattern.split(' ')
    # type_pattern=type_pattern.replace('<e>',midlist[0])
    patternlist[6]='ns:'+patternlist[6]
    patternlist[5]=patternlist[5].replace('<e>','ns:'+q_entity)
    type_pattern=' '.join(patternlist)

    return type_pattern