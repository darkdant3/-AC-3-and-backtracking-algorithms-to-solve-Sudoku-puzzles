
# coding: utf-8

# In[34]:

from collections import OrderedDict


# In[45]:

import time


# In[46]:

import sys


# In[2]:

def init_variables():
    V = OrderedDict()
    for x in range(ord('A'), ord('I')+1):
        for i in range(1, 10):
            V[chr(x) + str(i)] = 0
    return V


# In[6]:

V = init_variables()


# In[2]:

len('003020600900305001001806400008102900700000008006708200002609500800203009005010300'),len(V)


# In[33]:

assigments = '094000130000000000000076002080010000032000000000200060000050400000008007006304008'
for i,v in enumerate(V):
    #print v, assigments[i]
    pass


# In[5]:

# variable domain values
def init_domains(V):
    D = OrderedDict()
    for x in V:
        D[x] = range(1, 10)
    return D
#print D


# In[18]:

D = init_domains(V)


# In[22]:

#D


# In[8]:

#assign initial value domains
def init_values(V, D, vals):
    for i, x in enumerate(V):
        if int(vals[i]) != 0:
            D[x] = [int(vals[i])]


# In[ ]:




# In[9]:

#constraints
#1. 3x3, row, column must contain values from 1 to 9
import numpy as np
C1 = {}
b = np.array(V.keys())
b = b.reshape(9,9)
#print b
C1 = {}
for i in range(3, 12, 3):
    #print i,i-3
    #print b[i-3:i]
    for e in range(3,12,3):
        #print e
        by_3 = b[i-3:i,e-3:e]
        by_3_lst = []
        for c in by_3:
            by_3_lst.extend(c)
        #print by_3_lst
        C1['-'.join(by_3_lst)] = range(1,10)
#print C1,len(C1)


# In[28]:

#print b


# In[10]:

#row , column constraints
C2 = {}
C3 = {}
for i in range(0,9):
    k_row =  '-'.join(b[:, i].tolist())
    k_col = '-'.join(b[i, :].tolist())
    C2[k_row] = range(1, 10)
    C3[k_col] = range(1, 10)


# In[11]:

C = zip(C1,C2,C3)
def neighbors(v, C):
    ''' v - a variable to find its neighbors'''
    #check in 3x3 grid
    n_lst = []
    for c1, c2,c3 in C:
        if v in c1:
            c1_lst = c1.split('-')
            c1_lst.remove(v)
            for c1_ in c1_lst:
                if not c1_ in n_lst:
                    n_lst.append(c1_)
        if v in c2:
            c2_lst = c2.split('-')
            c2_lst.remove(v)
            for c2_ in c2_lst:
                if not c2_ in n_lst:
                    n_lst.append(c2_)
        if v in c3:
            c3_lst = c3.split('-')
            c3_lst.remove(v)
            for c3_ in c3_lst:
                if not c3_ in n_lst:
                    n_lst.append(c3_)
    #print n_lst
    return n_lst


# In[12]:

#neighbors('A1',C)


# In[13]:

from copy import deepcopy
def revise(X_i, X_j):
    revised = False
    Dx = deepcopy(D)
    #print Dx[X_j]
    DX_j = []
    for x in Dx[X_i]:

        for y in Dx[X_j]:
            if x == y:
                #print y
                DX_j.append(y)
        #print Dx[X_j] , DX_j
        if Dx[X_j] == DX_j:
            D[X_i].remove(x)
            revised = True
            #break
        #print D[X_i]
    return revised


# In[60]:

D['A1'] = [1,2,3]
D['A2'] = [1,2,3]


# In[61]:

revise('A1', 'A2')


# In[314]:

D['A1'], D['A2']


# In[14]:

binary_cs = []
for c1, c2, c3 in C:
    c1_lst = c1.split('-')
    c2_lst = c2.split('-')
    c3_lst = c3.split('-')

    for i in range(0, len(c1_lst)):
        if i + 1 < len(c1_lst):
            pass
        for j in range(i+1, len(c1_lst)):
            binary_cs.append((c1_lst[i], c1_lst[j]))
            binary_cs.append((c2_lst[i], c2_lst[j]))
            binary_cs.append((c2_lst[i], c2_lst[j]))

#print len(binary_cs), len(C1), len(C2), len(C3)
#print binary_cs


# In[16]:

import Queue
def ac3():
    q = Queue.Queue()
    for arc in binary_cs:
        #print arc
        q.put(arc)
    #print q.empty()
    while not q.empty():
        X_i, X_j = q.get()
        if revise(X_i, X_j):
            if len(D[X_i]) == 0:
                return False
            n_lst = neighbors(X_i, C)
            n_lst.remove(X_j)
            for X_k in n_lst:
                q.put((X_k, X_i))
    return True


# In[17]:

ac3()


# In[70]:

D['A1']


# In[19]:

def select_unsigned_variable(V, D, C):
    '''The variable with fewest remaining values in its domain'''
    selected_variable = ''
    smallest_possible = 9
    for v in V:
        if len(D[v]) > 1 and len(D[v]) <= smallest_possible:
            selected_variable = v
            smallest_possible = len(D[v])

    return selected_variable


# In[20]:

V = init_variables()
D = init_domains(V)
init_values(V, D, assigments)


# In[21]:

select_unsigned_variable(V, D, C)


# In[22]:

def is_complete(D):
    for x in D:
        if len(D[x]) != 1:
            return False
    return True


# In[30]:

def is_consistent(var, d, D, C):
    consistent = True
    neighbors_lst = neighbors(var, C)
    #print var , neighbors_lst, len(neighbors_lst)
    for x in neighbors_lst:
        #print D[x], d
        if D[x] == [d]:
            consistent = False
            break
    return consistent


# In[24]:

def backtrack(assigment, V, D, C):

    if is_complete(D):
        return assigment
    var = select_unsigned_variable(V, D, C)
    domain = D[var]
    for  d in D[var]:
        if is_consistent(var, d, D, C):
            assigment[var] = [d]
            D[var] = [d]
            result = backtrack(assigment, V, D, C)
            if result:
                return result
            del assigment[var]
            D[var] = domain

    return {}


# In[25]:

def backtracking_search(V, D, C):
    return backtrack({}, V, D, C)


# In[42]:

sudokus_start = []
with open('sudokus_start.txt','r') as _file:
    for line in _file.readlines():
        #print int(line)
        sudokus_start.append(line.replace('\r\n', ''))
    _file.close()
solved = 0
start_time = time.time()
elapsed = 0
'''for start in sudokus_start:
    V = init_variables()
    D = init_domains(V)
    init_values(V,D, start)
    if backtracking_search(V, D, C):
        solved += 1
    elapsed = time.time() - start_time
    if  elapsed > 360 + 5 :
        break;

print 'Solved=%d in %.2f seconds' % (solved, elapsed)
'''

# In[43]:

V = init_variables()
D = init_domains(V)
init_values(V,D, assigments)
#assignment = backtracking_search(V, D, C)


# In[44]:

assigments


# In[39]:

D


# In[ ]:

if __name__ == '__main__':
    #print sys.argv
    inital_assigment = sys.argv[1]

    V = init_variables()
    D = init_domains(V)
    start = time.time()
    init_values(V,D, inital_assigment)
    backtracking_search(V, D, C)
    print 'Solved in %.2f seconds' % (time.time() - start)
    with open('output.txt', 'w') as _file:
        assigments = D.values()
        assignment_lst = []
        for a in assigments:
            assignment_lst.append(a[0])
        assigments = ''.join(str(val) for val in assignment_lst)
        print 'Assigments [{}]'.format(assigments)
        print assigments
        _file.write(assigments)
        _file.close()
