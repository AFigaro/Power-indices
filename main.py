import sys
sys.path.append(r'C:\\Python files\\Power indices\\indices')
sys.path.append(r'C:\\Python files\\Power indices\\utils')

from indices.power_indices import *
from utils.preprocessing import *
from utils.index_utils import *
from utils.data_constructor import *

import pyexcel_xlsx as py_ex
import xlsxwriter

path_dat = r'C:\Python files\Power distribution\North Countries.xlsx'
path_write = r'C:\Python files\Power distribution\_test.xlsx'

data = py_ex.get_data(path_dat)[u'\u041b\u0438\u0441\u04421'] # This stands for Russian language Лист1
dict_data = OrderedDict_over_YearCountry(data)

sign_part = signific_parties_names(dict_data, 0.1, 'Banzhaf')
DataFrameWriter(sign_part, path_write)
