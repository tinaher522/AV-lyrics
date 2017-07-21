__all__ = ['gen_id_list_incrementing','gen_id_list_unique']
"""
Created on Sun May 22 22:00:12 2016

@author: groa
"""

import numpy as np

def gen_id_list_unique(valuelist, valuelist_2=None, digits=3, concatenate=0, concatenator=","):
    '''Generate id for unique items
    only increment id for new unique values
    
    valuelist    list of value to generate ID
    valuelist_2  list of value for tuple with valuelist
    digits       len of ids
    concatenate  0 = return only id
                 1 = return value + id
                 2 = return id + value
    '''
    valuelist_ids = [] 
    value = 0

    if not valuelist_2 is None:    
        valuelist = map(lambda x,y:(x,y),valuelist,valuelist_2)
        valuelist = [concatenator.join(s) for s in valuelist]
    
    for vl in range(len(valuelist)):
        if valuelist[vl] in valuelist[:vl]:
            valuelist_ids.append(valuelist_ids[valuelist.index(valuelist[vl])])
        else:
            value += 1
            valuelist_ids.append('0'*(digits-len(str(value))) + str(value)) 

    
    if concatenate == 1:
        for i in range(len(valuelist_ids)):
            valuelist_ids[i] = str(valuelist[i]) + str(valuelist_ids[i])
    elif concatenate == 2:
        for i in range(len(valuelist_ids)):
            valuelist_ids[i] = str(valuelist_ids[i]) + str(valuelist[i])

    return valuelist, valuelist_ids



def gen_id_list_incrementing(valuelist, digits = 3, concatenate = 0 ):
    '''Generate id for groups
    If one register is repited, the id is incremented.
    
    valuelist    list of value to generate ID
    digits       len of ids
    concatenate  0 = return only id
                 1 = return value + id
                 2 = return id + value
    '''
    valuelist_ids = [] # np.zeros(len(valuelist))
    valuelist_processed = [] #np.zeros(len(valuelist))
    for vl in range(len(valuelist)):
        if valuelist[vl] in valuelist_processed:
            pos = [item for item in range(len(valuelist_processed)) if valuelist_processed[item] ==  valuelist[vl]]
            valuelist_processed.append(valuelist[vl])
            value = str(int(valuelist_ids[pos[np.argmax(pos)]]) + 1)
            valuelist_ids.append('0'*(digits-len(value)) + value)
        else:
            valuelist_processed.append(valuelist[vl])
            valuelist_ids.append('0'*(digits-1) +'1')
    
    if concatenate == 1:
        for i in range(len(valuelist_ids)):
            valuelist_ids[i] = str(valuelist[i]) + str(valuelist_ids[i])
    elif concatenate == 2:
        for i in range(len(valuelist_ids)):
            valuelist_ids[i] = str(valuelist_ids[i]) + str(valuelist[i])
            
    return valuelist_ids