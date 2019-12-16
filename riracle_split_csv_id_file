import csv

MAX_NUMBER_OF_ID_IN_FILE = 9000

csv_content = []

# -*- coding: utf-8 -*-

### Read file
with open('491_1801706.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue
        else:
            csv_content.append(row[0])
            line_count += 1
    # print(csv_content)
    print("Processed read {0} ids.".format(len(csv_content)))

### Group files
all_content_to_write = []
element_count = 0
tmp_file_content = []
for element in csv_content:
    if element_count < MAX_NUMBER_OF_ID_IN_FILE: # and len(csv_content) > 0
        tmp_file_content.append(element)
        element_count += 1
    else:
        all_content_to_write.append(tmp_file_content)
        element_count = 0
        tmp_file_content = []
        tmp_file_content.append(element)
        element_count += 1
if len(tmp_file_content) > 0:
    all_content_to_write.append(tmp_file_content)

# print("{0}".format(len(all_content_to_write)))
### Write files

file_count = 0
for result_file_content in all_content_to_write:
    file_count += 1
    file_name = "results/test_result_{0}.csv".format(file_count)
    with open(file_name, mode='w') as employee_file:
        file_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(['customer_id'])
        line_count = 0
        for element in result_file_content:
            file_writer.writerow([element])
            line_count += 1
        print("Processed wrote {0} ids to file {1}.".format(line_count, file_name))

# with open('results/test_result.csv', mode='w') as employee_file:
#     file_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     file_writer.writerow(['customer_id'])
#     line_count = 0
#     for element in csv_content:
#         file_writer.writerow([element])
#         line_count += 1
#     print("Processed wrote {0} ids.".format(line_count))
