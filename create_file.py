import xlwt
import json
import datetime
from pytz import timezone
from datetime import date

data_in_file_total_crashes_count = [] # https://api-dash.fabric.io/graphql?relayDebugName=AppTimeseries
data_in_file_total_sessions_and_users_count = [] # https://api-dash.fabric.io/graphql?relayDebugName=SessionAndUserMetrics

with open('total_crashes_count.json') as f:
    data_in_file_total_crashes_count = json.load(f)

with open('total_sessions_and_users_count.json') as f:
    data_in_file_total_sessions_and_users_count = json.load(f)

# Work with data_in_file_total_sessions_and_users_count
data_answers = data_in_file_total_sessions_and_users_count["data"]["project"]["answers"]
total_sessions_for_builds_key = ""
dau_by_build_key = ""
for key in data_answers.keys():
    if "totalSessionsForBuild" in key:
        total_sessions_for_builds_key = key
    elif "dauByBuild" in key:
        dau_by_build_key = key
synthesized_build_version = data_answers[total_sessions_for_builds_key][0]["synthesizedBuildVersion"]

## Total session
time_list_of_total_sessions_for_builds = []
value_of_total_sessions_for_builds = []
for item in data_answers[total_sessions_for_builds_key][0]["values"]:
    time = datetime.datetime.fromtimestamp(int(item["timestamp"])).replace(tzinfo=timezone("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")
    time_list_of_total_sessions_for_builds.append(time)
    value_of_total_sessions_for_builds.append(int(item["value"]))

## Total DAU
time_list_of_dau_by_builds = []
value_of_dau_by_builds = []
for item in data_answers[dau_by_build_key]["values"]:
    time = datetime.datetime.fromtimestamp(int(item["timestamp"])).replace(tzinfo=timezone("Asia/Tokyo")).strftime('%Y-%m-%d %H:%M:%S')
    time_list_of_dau_by_builds.append(time)
    value_of_dau_by_builds.append(int(item["value"]))

# Work with data_in_file_total_crashes_count
data_crashlytics = data_in_file_total_crashes_count["data"]["project"]["crashlytics"]
app_time_series_key = ""
for key in data_crashlytics.keys():
    if "appTimeseries" in key:
        app_time_series_key = key

## Total crashed sessison
time_list_of_total_crashed_sessions = []
value_of_total_crashed_sessions = []
for item in data_crashlytics[app_time_series_key]["eventsCount"]:
    time = datetime.datetime.fromtimestamp(int(item[0])).replace(tzinfo=timezone("Asia/Tokyo")).strftime('%Y-%m-%d %H:%M:%S')
    time_list_of_total_crashed_sessions.append(time)
    value_of_total_crashed_sessions.append(int(item[1]))

## Total crashed device
time_list_of_total_crashed_devices = []
value_of_total_crashed_devices = []
for item in data_crashlytics[app_time_series_key]["impactedDevices"]:
    time = datetime.datetime.fromtimestamp(int(item[0])).replace(tzinfo=timezone("Asia/Tokyo")).strftime('%Y-%m-%d %H:%M:%S')
    time_list_of_total_crashed_devices.append(time)
    value_of_total_crashed_devices.append(int(item[1]))

if len(time_list_of_total_sessions_for_builds) != len(time_list_of_total_crashed_sessions):
    print("Data Error!")
    SystemExit

if len(time_list_of_dau_by_builds) != len(time_list_of_total_crashed_devices):
    print("Data Error!")
    SystemExit

# Create file
work_book = xlwt.Workbook()
work_sheet = work_book.add_sheet("Statistics")
style_of_title = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
## Version infor
work_sheet.write(0, 0, "Version:", style_of_title)
work_sheet.write(0, 1, synthesized_build_version, style_of_title)
## Title
column_of_datetime = 0
column_of_total_sessions = 1
column_of_crashed_sessions = 2
column_of_crash_free_sessions_percent = 3
column_of_total_users = 4
column_of_crashed_devices = 5
column_of_crashed_devices_percent = 6
work_sheet.write(1, column_of_datetime, "Datetime (Year-Month-Day)", style_of_title)
work_sheet.write(1, column_of_total_sessions, "All sessions", style_of_title)
work_sheet.write(1, column_of_crashed_sessions, "Crashes sessions", style_of_title)
work_sheet.write(1, column_of_crash_free_sessions_percent, "Crash-free sessions (%)", style_of_title)
work_sheet.write(1, column_of_total_users, "All users", style_of_title)
work_sheet.write(1, column_of_crashed_devices, "Crashes users", style_of_title)
work_sheet.write(1, column_of_crashed_devices_percent, "Crash-free users (%)", style_of_title)
## Content
### Datetime
for index, time in enumerate(time_list_of_total_sessions_for_builds):
    work_sheet.write(index + 2, column_of_datetime, time)
### All sessions
for index, value in enumerate(value_of_total_sessions_for_builds):
    work_sheet.write(index + 2, column_of_total_sessions, value)
### Crashes sessions
for index, value in enumerate(value_of_total_crashed_sessions):
    work_sheet.write(index + 2, column_of_crashed_sessions, value)
### Crash-free sessions
for index, value in enumerate(value_of_total_sessions_for_builds):
    number_of_crashed = value_of_total_crashed_sessions[index]
    result = ((value - number_of_crashed)*1.0/value) * 100.0
    work_sheet.write(index + 2, column_of_crash_free_sessions_percent, "{0:.2f}%".format(result))

### All users
for index, value in enumerate(value_of_dau_by_builds):
    work_sheet.write(index + 2, column_of_total_users, value)
### Crashes users
for index, value in enumerate(value_of_total_crashed_devices):
    work_sheet.write(index + 2, column_of_crashed_devices, value)
### Crash-free users
for index, value in enumerate(value_of_dau_by_builds):
    number_of_crashed = value_of_total_crashed_devices[index]
    result = ((value - number_of_crashed)*1.0/value)  * 100.0
    work_sheet.write(index + 2, column_of_crashed_devices_percent, "{0:.2f}%".format(result))

time_list_of_total_sessions_for_builds
file_name = "{0}~{1}.xls".format(time_list_of_total_sessions_for_builds[0], time_list_of_total_sessions_for_builds[-1])
work_book.save(file_name)
print("------------DONE------------")

# Other infor:
# Using python version: 2.7.14
# pytz install: python -m pip install pytz
#               easy_install --upgrade pytz
# xlwt: https://github.com/python-excel/xlwt
