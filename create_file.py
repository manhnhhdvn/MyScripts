import xlwt
import json

from datetime import datetime

data_of_total_events_count = [] # crashes count
data_of_total_sessions_for_builds = [] # all session and user count

with open('total_events_count.json') as f:
    data_of_total_events_count = json.load(f)

with open('total_sessions_for_builds.json') as f:
    data_of_total_sessions_for_builds = json.load(f)

# Work with data_of_total_sessions_for_builds
data_answers = data_of_total_sessions_for_builds["data"]["project"]["answers"]
list_keys = data_answers.keys()

# style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
#     num_format_str='#,##0.00')
# style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

# wb = xlwt.Workbook()
# ws = wb.add_sheet('A Test Sheet')

# ws.write(0, 0, 1234.56, style0)
# ws.write(1, 0, datetime.now(), style1)
# ws.write(2, 0, 1)
# ws.write(2, 1, 1)
# ws.write(2, 2, xlwt.Formula("A3+B3"))

wb.save('example.xls')

# https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
# https://stackoverflow.com/questions/13437727/python-write-to-excel-spreadsheet
# https://github.com/python-excel/xlwt
# https://stackoverflow.com/questions/15789059/python-json-only-get-keys-in-first-level