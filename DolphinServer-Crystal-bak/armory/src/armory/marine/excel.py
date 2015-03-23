# -*- coding: UTF-8 -*-
import logging
from openpyxl import Workbook

_LOGGER = logging.getLogger('armory')


class ArmoryExcel(object):
    '''
    armory excel lib, use this lib to read and write excle
    '''
    @staticmethod
    def wirte_excel(file_path, title, sheet_value):
        '''
        write excel
        parameter: two dimension array
        result: a excel file with the data in two
        '''
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = title
        for row_num, row_value in enumerate(sheet_value):
            for column_num, column_value in enumerate(row_value):
                sheet.cell(row=row_num + 1, column=column_num + 1).value = column_value
        workbook.save(file_path)


if __name__ == '__main__':
    content = [[1, 2, 3], [4, 5, 6]]
    ArmoryExcel.write_excel('./a.xlsx', 'test', content)
