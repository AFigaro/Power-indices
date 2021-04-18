import sys
sys.path.append(r'C:\\Python files\\Power indices\\')


from utils.index_utils import *
from collections import OrderedDict

def Penrose(frac, q):

    '''Compute Penrose index (unnormalized Banzhaf index)'''

    number_of_keys = key_num_ban(frac, q)
    Pen = dict()
    N = 2 ** ((len(number_of_keys)) - 1)
    for i in range(len(number_of_keys)):
        Pen[str(i)] = number_of_keys[str(i)] / N
    return Pen

def Banzhaf(frac, q):

    '''Compute Banzhaf index'''

    number_of_keys = key_num_ban(frac, q)
    answ = 0
    ban = dict()
    k = 0
    for i in range(len(number_of_keys)):
        if frac[i] >= q:
            answ = 1
            part = i
            k += 1
    if answ == 0:
        summ = 0
        for i in range(len(number_of_keys)):
            summ += number_of_keys[str(i)]
        for i in range(len(number_of_keys)):
            ban[str(i)] = number_of_keys[str(i)] / summ
        return OrderedDict(sorted(ban.items(), key=lambda t: int(t[0])))
    else:
        if k == 1:
            for i in range(len(number_of_keys)):
                ban[str(i)] = 0
            ban[str(part)] = 1
            return OrderedDict(sorted(ban.items(), key=lambda t: int(t[0])))
        else:
            return 'computation is impossible'

def general_index_dig(frac, q):

    '''Compute general Deegan-Packel index (unnormalized)'''

    win_coal = min_win_dig(frac, q)
    indeces = dict()
    for i in range(len(frac)):
        indeces[str(i)] = 0
    for coalition in win_coal:
        div = len(coalition)
        for party in coalition:
            indeces[str(party[0])] += 1 / div
    return indeces

def Digen_Packel(frac, q):

    '''Deegan-Packel power index'''

    indeces = general_index_dig(frac, q)
    summ_index = sum(list(indeces.values()))
    for i in range(len(frac)):
        indeces[str(i)] = indeces[str(i)] / summ_index
    return OrderedDict(sorted(indeces.items(), key=lambda t: int(t[0])))

def Holler_Packel(frac, q):

    '''Holler-Packel power index'''

    number_of_keys = key_num_holl(frac, q)
    answ = 0
    holl = dict()
    k = 0
    for i in range(len(number_of_keys)):
        if frac[i] >= q:
            answ = 1
            part = i
            k += 1
    if answ == 0:
        summ = 0
        for i in range(len(number_of_keys)):
            summ += number_of_keys[str(i)]
        for i in range(len(number_of_keys)):
            holl[str(i)] = number_of_keys[str(i)] / summ
        return OrderedDict(sorted(holl.items(), key=lambda t: int(t[0])))
    else:
        if k == 1:
            for i in range(len(number_of_keys)):
                holl[str(i)] = 0
            holl[str(part)] = 1
            return OrderedDict(sorted(holl.items(), key=lambda t: int(t[0])))
        else:
            return 'computation is impossible'

def general_index_john(frac, q):

    '''Johnston general index (unnormalized)'''

    working_coal = win_only_parties(frac, q)
    indeces = dict()
    for i in range(len(frac)):
        indeces[str(i)] = 0
    for coalition in working_coal:
        div = len(coalition)
        for party in coalition:
            indeces[str(party[0])] += 1 / div
    return indeces

def Johnson(frac, q):

    '''Johnston power index'''

    indeces = general_index_john(frac, q)
    summ_index = sum(list(indeces.values()))
    for i in range(len(frac)):
        indeces[str(i)] = indeces[str(i)] / summ_index
    return OrderedDict(sorted(indeces.items(), key=lambda t: int(t[0])))

def Shapley_Shubik(frac, q):

    '''Shapley-Shubik power index'''

    n = len(frac)
    key_party_per_size = key_party(frac, q)
    Sh_Sh = dict()
    for i in range(len(frac)):
        Sh_Sh[str(i)] = 0
    for i in range(len(frac)):
        for size in key_party_per_size:
            s = size[0]
            Sh_Sh[str(i)] += size[i + 1] * (math.factorial(n - s) * math.factorial(s - 1) / math.factorial(n))
    return OrderedDict(sorted(Sh_Sh.items(), key=lambda t: int(t[0])))

def prevent_index(frac, q):

    '''Compute Coleman preventive index'''

    num_of_keys = key_num_colem(frac, q)
    all_win_len = len(all_win_colem(frac, q))
    col_prev = dict()
    for i in range(len(num_of_keys)):
        col_prev[str(i)] = num_of_keys[str(i)] / all_win_len
    return OrderedDict(sorted(col_prev.items(), key=lambda t: int (t[0])))


def initiative_index(frac, q):

    '''Compute Coleman initiative index'''

    num_of_keys = key_num_colem(frac, q)
    all_win_len = len(all_win_colem(frac, q))
    all_lose_len = len(combination_all_colem(frac)) - all_win_len
    col_prev = dict()
    for i in range(len(num_of_keys)):
        col_prev[str(i)] = num_of_keys[str(i)] / all_lose_len
    return OrderedDict(sorted(col_prev.items(), key=lambda t: int (t[0])))

def PowerIndex(data_dict, q, index):

    '''The function to compute any power index and return dictionary with power distribution'''

    frac = list(OrderedDict(sorted(data_dict.items(), key=lambda t: t[0])).values())
    zip_number_name = list(zip(range(len(frac)), list(OrderedDict(sorted(data_dict.items(), key=lambda t: t[0])).keys())))
    if index not in ['Penrose', 'Banzhaf', 'Shapley-Shubik', 'Johnston', 'Digen-Packel', 'Holler-Packel', 'Coleman initiative', 'Coleman preventive']:
        raise ValueError('Choose correct power index')
    if index == 'Penrose':
        index_dict = Penrose(frac, q)
    if index == 'Banzhaf':
        index_dict = Banzhaf(frac, q)
    if index == 'Shapley-Shubik':
        index_dict = Shapley_Shubik(frac, q)
    if index == 'Johnston':
        index_dict = Johnson(frac, q)
    if index == 'Digen-Packel':
        index_dict = Digen_Packel(frac, q)
    if index == 'Holler-Packel':
        index_dict = Holler_Packel(frac, q)
    if index == 'Coleman initiative':
        index_dict = initiative_index(frac, q)
    if index == 'Coleman preventive':
        index_dict = prevent_index(frac, q)
    index_dict_advance = dict()
    for i in zip_number_name:
        index_dict_advance[i[1]] = index_dict[str(i[0])]
    return index_dict_advance
