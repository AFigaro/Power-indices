# All additional functions to process the datasets and write them

import sys
sys.path.append(r'C:\\Python files\\Power indices\\')


import pandas as pd
from indices.power_indices import *
from utils.preprocessing import *
import xlsxwriter

def dataFrame_construct(data, i):

    '''Create a dataframe for a single country'''

    new_dictionary = OrderedDict_over_YearCountry(data)[i]
    party_names = list(new_dictionary.keys())
    party_names = Remove_element(party_names, 'quota')
    party_names = Remove_element(party_names, 'year')
    party_names = Remove_element(party_names, 'country')
    frac = []
    for name in party_names:
        frac += [new_dictionary[name]]
    q = new_dictionary['quota'] - 1
    list_Ban = Banzhaf(frac, q)
    list_Sh_Sh = Shapley_Shubik(frac, q)
    list_Hol_pack = Holler_Packel(frac, q)
    list_john = Johnson(frac, q)
    list_Dig_pack = Digen_Packel(frac, q)
    list_Penrose = Penrose(frac, q)
    list_col_prev = prevent_index(frac, q)
    list_col_init = initiative_index(frac, q)
    df = pd.DataFrame(data = frac, index = party_names, columns = ['Num_of_voters'])
    df['Banzhaf'] = list_Ban.values()
    df['Digen-Packel'] = list_Dig_pack.values()
    df['Holler-Packel'] = list_Hol_pack.values()
    df['Johnson'] = list_john.values()
    df['Shapley-Shubik'] = list_Sh_Sh.values()
    df['Penrose'] = list_Penrose.values()
    df['Coleman initiative'] = list_col_init.values()
    df['Coleman preventive'] = list_col_prev.values()
    return df

def DataFrame_builder_one_country(data, country, threshold, path):

    '''Build an excel file for one country with all indices except for Penrose and Coleman'''

    list_of_names = permut_names(country)
    all_countries = OrderedDict_over_YearCountry(data)
    needed_countries = []
    writer = pd.ExcelWriter(path + country + '.xlsx', engine='xlsxwriter')
    start_row = 0
    for country in all_countries:
        if country['country'] in list_of_names:
            needed_countries += [country]
    for new_dictionary in needed_countries:
        party_names = list(new_dictionary.keys())
        party_names = Remove_element(party_names, 'quota') # Тут написал свою функцию, так как remove удалял по непонятной причине все элементы
        party_names = Remove_element(party_names, 'year')
        party_names = Remove_element(party_names, 'country')
        frac = []
        for name in party_names:
            frac += [new_dictionary[name]]
        q = new_dictionary['quota'] - 1
        list_Ban = Banzhaf(frac, q)
        list_Sh_Sh = Shapley_Shubik(frac, q)
        list_Hol_pack = Holler_Packel(frac, q)
        list_john = Johnson(frac, q)
        list_Dig_pack = Digen_Packel(frac, q)
        list_Penrose = Penrose(frac, q)
        list_col_prev = prevent_index(frac, q)
        list_col_init = initiative_index(frac, q)
        df = pd.DataFrame(index = party_names, columns = ['Num_of_voters', 'Banzhaf', 'Digen-Packel', 'Holler-Packel', 'Johnson','Shapley-Shubik', 'Description'])
        df.Num_of_voters = frac
        for i in range(len(frac)):
            df['Banzhaf'][i] = list(list_Ban.values())[i]
            df['Digen-Packel'][i] = list(list_Dig_pack.values())[i]
            df['Holler-Packel'][i] = list(list_Hol_pack.values())[i]
            df['Johnson'][i] = list(list_john.values())[i]
            df['Shapley-Shubik'][i] = list(list_Sh_Sh.values())[i]
            df['Penrose'][i] = list(list_Penrose.values())[i]
            df['Coleman initiative'][i] = list(list_col_init.values())[i]
            df['Coleman preventive'][i] = list(list_col_prev.values())[i]
        df['Description'][0] = ['quota:', new_dictionary['quota'] - 1, 'year:', new_dictionary['year'], 'country:', new_dictionary['country']]
        df = df.append({'Num_of_voters' : 'Num of key parties', 'Banzhaf' : Num_key_index(list_Ban.values(), threshold), 'Digen-Packel': Num_key_index(list_Dig_pack.values(), threshold),
                  'Holler-Packel' : Num_key_index(list_Hol_pack.values(), threshold), 'Johnson' : Num_key_index(list_john.values(), threshold),
                  'Shapley-Shubik' : Num_key_index(list_Sh_Sh.values(), threshold), 'Penrose' : Num_key_index(list_Penrose.values(), threshold),
                  'Coleman initiative' : Num_key_index(list_col_init.values(), threshold), 'Coleman preventive' : Num_key_index(list_col_prev.values(), threshold)}, ignore_index=True)
        df.to_excel(writer, sheet_name='Sheet1', startrow = start_row)
        start_row += df.shape[0] + 2
    writer.save()
    return 'Successful!'

def key_parties_over(new_dict_data, path_write, threshold):

    '''Create an excel table with significant parties for each country on the sheet'''

    list_names = []
    for country in new_dict_data:
        list_names += [country['country']]
    list_names = set(sorted(list_names))
    list_years = range(1992, 2021)
    df = pd.DataFrame(index = sorted(list_names), columns = list_years)
    dict_ban_data = dict()
    dict_Sh_Sh_data = dict()
    dict_Hol_data = dict()
    dict_John_data = dict()
    dict_Dig_data = dict()
    dict_Penrose = dict()
    dict_col_prev = dict()
    dict_col_init = dict()
    for country in list_names:
        now_c = []
        for dict_country in new_dict_data:
            if country == dict_country['country']:
                now_c += [dict_country]
        dict_year_per_country_ban = dict()
        dict_year_per_country_Sh_Sh = dict()
        dict_year_per_country_Hol = dict()
        dict_year_per_country_John = dict()
        dict_year_per_country_Dig = dict()
        dict_year_per_country_Pen = dict()
        dict_year_per_country_prev = dict()
        dict_year_per_country_init = dict()
        for election in now_c:
            party_names = list(election.keys())
            party_names = Remove_element(party_names, 'quota')
            party_names = Remove_element(party_names, 'year')
            party_names = Remove_element(party_names, 'country')
            frac = []
            for name in party_names:
                frac += [election[name]]
            q = election['quota']

            list_Ban = Banzhaf(frac, q)
            list_Sh_Sh = Shapley_Shubik(frac, q)
            list_Hol_pack = Holler_Packel(frac, q)
            list_john = Johnson(frac, q)
            list_Dig_pack = Digen_Packel(frac, q)
            list_Penrose = Penrose(frac, q)
            list_col_prev = prevent_index(frac, q)
            list_col_init = initiative_index(frac, q)

            ban_data = Num_key_index(list_Ban.values(), threshold)
            Sh_Sh_data = Num_key_index(list_Sh_Sh.values(), threshold)
            Hol_data = Num_key_index(list_Hol_pack.values(), threshold)
            John_data = Num_key_index(list_john.values(), threshold)
            Dig_data = Num_key_index(list_Dig_pack.values(), threshold)
            Pen_data = Num_key_index(list_Penrose.values(), threshold)
            Col_init =  Num_key_index(list_col_init.values(), threshold)
            Col_prev =  Num_key_index(list_col_prev.values(), threshold)

            year = election['year']
            dict_year_per_country_ban[str(year)] = ban_data
            dict_year_per_country_Sh_Sh[str(year)] = Sh_Sh_data
            dict_year_per_country_Hol[str(year)] = Hol_data
            dict_year_per_country_John[str(year)] = John_data
            dict_year_per_country_Dig[str(year)] = Dig_data
            dict_year_per_country_Pen[str(year)] = Pen_data
            dict_year_per_country_prev[str(year)] = Col_prev
            dict_year_per_country_init[str(year)] = Col_init

            dict_ban_data[country] = dict_year_per_country_ban
            dict_Sh_Sh_data[country] = dict_year_per_country_Sh_Sh
            dict_Hol_data[country] = dict_year_per_country_Hol
            dict_John_data[country] = dict_year_per_country_John
            dict_Dig_data[country] = dict_year_per_country_Dig
            dict_Penrose[country] = dict_year_per_country_Pen
            dict_col_prev[country] = dict_year_per_country_prev
            dict_col_init[country] = dict_year_per_country_init

            writer = pd.ExcelWriter(path_write, engine='xlsxwriter')
            start_row = 0
            df_ban = pd.DataFrame(data = dict_ban_data).transpose()
            df_ban.to_excel(writer, sheet_name='Sheet1', startrow = start_row)
            start_row += df_ban.shape[0] + 3
            df_Sh_Sh = pd.DataFrame(data = dict_Sh_Sh_data).transpose()
            df_Sh_Sh.to_excel(writer, sheet_name='Sheet1', startrow = start_row)
            start_row += df_Sh_Sh.shape[0] + 3
            df_Hol = pd.DataFrame(data = dict_Hol_data).transpose()
            df_Hol.to_excel(writer, sheet_name='Sheet1', startrow = start_row)
            start_row += df_Hol.shape[0] + 3
            df_John = pd.DataFrame(data = dict_John_data).transpose()
            df_John.to_excel(writer, sheet_name='Sheet1', startrow = start_row)
            start_row += df_John.shape[0] + 3
            df_Dig = pd.DataFrame(data = dict_Dig_data).transpose()
            df_Dig.to_excel(writer, sheet_name='Sheet1', startrow = start_row)
            start_row += df_Dig.shape[0] + 3
            df_Pen = pd.DataFrame(data = dict_Penrose).transpose()
            df_Pen.to_excel(writer, sheet_name='Sheet1', startrow = start_row)
            start_row += df_Pen.shape[0] + 3
            df_init = pd.DataFrame(data = dict_col_init).transpose()
            df_init.to_excel(writer, sheet_name='Sheet1', startrow = start_row)
            start_row += df_init.shape[0] + 3
            df_prev = pd.DataFrame(data = dict_col_prev).transpose()
            df_prev.to_excel(writer, sheet_name='Sheet1', startrow = start_row)
    writer.save()
    return 'Success'

def signific_parties_names(data, threshold, index):

    '''Write the names of the significant parties'''

    dict_data = data
    new_dict_data = []
    # For African countries
    for country in dict_data:
        if country['country'] != 'Congo - Kinshasa' and country['country'] != 'Morocco' and country['country'] != 'Madagascar' and country['country'] != 'Kenya' and country['country'] != 'Chad' and country['country'] != 'Algeria':
            new_dict_data += [country]

    indeces = ['Banzhaf', 'Shapley-Shubik', 'Johnston', 'Digen-Packel', 'Holler-Packel', 'Penrose', 'Coleman preventive', 'Coleman initiative']
    if index not in indeces:
        raise ValueError('Choose correct index name')
    list_names = []
    for country in new_dict_data:
        list_names += [country['country']]
    index_dict = dict()
    for country in list_names:
        now_country = []
        for dict_country in new_dict_data:
            if country == dict_country['country']:
                now_country += [dict_country]
        dict_year_per_country_index = dict()
        for i in range(1990, 2019):
            dict_year_per_country_index[str(i)] = -1
        for election in now_country:
            party_names = list(election.keys())
            party_names = Remove_element(party_names, 'quota') # Эта функция написано мной выше
            party_names = Remove_element(party_names, 'year')
            party_names = Remove_element(party_names, 'country')
            frac = dict()
            for i in party_names:
                frac[i] = election[i]
            q = election['quota']
            if index == 'Banzhaf':
                index_distrib = PowerIndex(frac, q, 'Banzhaf')
            if index == 'Holler-Packel':
                index_distrib = PowerIndex(frac, q, 'Holler-Packel')
            if index == 'Shapley-Shubik':
                index_distrib = PowerIndex(frac, q, 'Shapley-Shubik')
            if index == 'Digen-Packel':
                index_distrib = PowerIndex(frac, q, 'Digen-Packel')
            if index == 'Johnston':
                index_distrib = PowerIndex(frac, q, 'Johnston')
            if index == 'Penrose':
                index_distrib = PowerIndex(frac, q, 'Penrose')
            if index == 'Coleman preventive':
                index_distrib = PowerIndex(frac, q, 'Coleman preventive')
            if index == 'Coleman initiative':
                index_distrib = PowerIndex(frac, q, 'Coleman initiative')
            index_data = Num_key_index_names(index_distrib, threshold)
            year = election['year']
            dict_year_per_country_index[str(year)] = index_data
            index_dict[country] = dict_year_per_country_index
    df = pd.DataFrame.from_dict(index_dict, orient = 'columns').transpose().fillna(-1)
    return df
    
def signific_parties(data, threshold, index):

    '''Find the number of significant parties with accordance to given index'''

    dict_data = data
    new_dict_data = []
    # For African countries
    for country in dict_data:
        if country['country'] != 'Congo - Kinshasa' and country['country'] != 'Morocco' and country['country'] != 'Madagascar' and country['country'] != 'Kenya' and country['country'] != 'Chad' and country['country'] != 'Algeria':
            new_dict_data += [country]
    indeces = ['Banzhaf', 'Shapley-Shubik', 'Johnston', 'Digen-Packel', 'Holler-Packel', 'Penrose', 'Coleman preventive', 'Coleman initiative']
    if index not in indeces:
        raise ValueError('Choose correct index name')
    list_names = []
    for country in new_dict_data:
        list_names += [country['country']]
    index_dict = dict()
    for country in list_names:
        now_country = []
        for dict_country in new_dict_data:
            if country == dict_country['country']:
                now_country += [dict_country]
        dict_year_per_country_index = dict()
        for i in range(1990, 2021):
            dict_year_per_country_index[str(i)] = -1
        for election in now_country:
            party_names = list(election.keys())
            party_names = Remove_element(party_names, 'quota') # Эта функция написано мной выше
            party_names = Remove_element(party_names, 'year')
            party_names = Remove_element(party_names, 'country')
            frac = dict()
            for i in party_names:
                frac[i] = election[i]
            q = election['quota']
            if index == 'Banzhaf':
                index_distrib = PowerIndex(frac, q, 'Banzhaf')
            if index == 'Holler-Packel':
                index_distrib = PowerIndex(frac, q, 'Holler-Packel')
            if index == 'Shapley-Shubik':
                index_distrib = PowerIndex(frac, q, 'Shapley-Shubik')
            if index == 'Digen-Packel':
                index_distrib = PowerIndex(frac, q, 'Digen-Packel')
            if index == 'Johnston':
                index_distrib = PowerIndex(frac, q, 'Johnston')
            if index == 'Penrose':
                index_distrib = PowerIndex(frac, q, 'Penrose')
            if index == 'Coleman preventive':
                index_distrib = PowerIndex(frac, q, 'Coleman preventive')
            if index == 'Coleman initiative':
                index_distrib = PowerIndex(frac, q, 'Coleman initiative')
            index_data = Num_key_index(index_distrib.values(), threshold)
            year = election['year']
            dict_year_per_country_index[str(year)] = index_data
            index_dict[country] = dict_year_per_country_index
    df = pd.DataFrame.from_dict(index_dict, orient = 'columns').transpose().fillna(-1).astype(int)
    return df

def DataFrameWriter(df, path):

    '''Write a dataframe to excel table with given path'''

    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', startrow = 0)
    writer.save()
    return 'Success'