# The functions to preprocess the excel file to dict format

import sys
sys.path.append(r'C:\\Python files\\Power indices\\indices')
sys.path.append(r'C:\\Python files\\Power indices\\utils')

from collections import OrderedDict


def dict_construct_over_data(data):

    '''Create a dictionary from excel file. The excel file must have the special format,
       described in Readme.'''

    data_len = len(data)
    all_parties = []
    for i in range(0, data_len-1, 3):
        year = data[i][0]
        parties_names = data[i][1 : len(data[i]) - 6]
        country = data[i + 1][0]
        parties_data = data[i + 1][1 : len(data[i + 1]) - 2]
        quota = data[i + 1][-1]
        country_dict = dict()
        country_dict['year'] = year
        country_dict['country'] = country
        country_dict['quota'] = quota
        for i in range(len(parties_names)):
            country_dict[parties_names[i]] = int(parties_data[i])
        all_parties += [country_dict]
    return all_parties

def OrderedDict_over_YearCountry(data):

    '''Create an Ordered dict to provide the information to power indices functions'''

    data_dictionary = dict_construct_over_data(data)
    new_dictionary = []
    for element in data_dictionary:
        new_dictionary += [dict(sorted(element.items(), key=lambda t: t[0]))]
    return new_dictionary

def Remove_element(lst, val):
    return [value for value in lst if value != val]

def Num_key_index(sample, threshold):

    '''Find the number of significant parties in the parliament.
    As input it takes the dictionary of output from index functions'''

    k = 0
    for index in sample:
        if index >= threshold:
            k += 1
    return k

def permut_names(country):

    '''Add all possible headers for the country (if there where second elections in the same year
       they are denoted as /1, the third with /2 and the forth with the /3)'''

    return [str(country), str(country) + '/1', str(country) + '/2',
                    str(country) + '/3',str(country) + ' (without president support)', str(country) + '/1 (without president support)',
                    str(country) + '/2 (without president support)']
