import classes

'''
Make UI
Don't forget about "day satifactory"
'''

'''day1 = classes.Day({1: 'abc'})
day2 = classes.Day({1: 'abc'})


timetable1 = [
    ((6,3), (7, 11)) , ((8,35), (9,43)), ((9,52),(10,52)), ((11,6), (12,51)), ((13,15),(13,42))
]

timetable2 = [
    ((6,54),(7,29)), ((8,32), (10,24)), ((10,58), (12,21)), ((12,48),(13,41)), ((15,11), (16,6))
]

for timestamp in timetable1:
    day1.add_time(1, classes.TimeStamp(*timestamp))

for timestamp in timetable2:
    day2.add_time(1, classes.TimeStamp(*timestamp))



week = classes.Week({1: "abc"})

week.add_time(day1)
week.add_time(day2)


# day1.show_time_distribution(1)
# day2.show_time_distribution(1)
week.show_time_distribution(1)
'''
time_stat = classes.TimeStatistics(["Work"])
time_stat.begin_day()

timetable1 = [
    ((6,3), (7, 11)) , ((8,35), (9,43)), ((9,52),(10,52)), ((11,6), (12,51)), ((13,15),(13,42))
]

for timestamp in timetable1:
    time_stat.add_timestamp("Work", classes.TimeStamp(*timestamp))

time_stat.end_day()
time_stat.begin_day()

timetable2 = [
    ((6,54),(7,29)), ((8,32), (10,24)), ((10,58), (12,21)), ((12,48),(13,41)), ((15,11), (16,6))
]

for timestamp in timetable2:
    time_stat.add_timestamp("Work", classes.TimeStamp(*timestamp))

time_stat.end_day()

time_stat.show_time_distribution("Work", "years")
# time_stat.show_time_distribution("Work", "months")
time_stat.show_time_distribution("Work", "weeks")
# time_stat.show_time_distribution("Work", "days")
time_stat.show_time_distribution("Work", "days", 1)

