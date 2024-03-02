from datetime import datetime
from datetime import date


class Interval:
    def __init__(self, start_time, end_time, entity):
        self.start_time = start_time
        self.end_time = end_time
        self.entity = entity
        self.childs = set()

    def remove(self, child):
        self.childs.remove(child)


class IntervalChild:
    def __init__(self, name, interval):
        self.name = name
        self.interval = interval

    def delete(self):
        self.interval.remove(self)


# interval = Interval(0, 1, "st")
# child = IntervalChild("dummy", interval)
# child1 = IntervalChild("dummy1", interval)
# interval.childs.add(child)
# interval.childs.add(child1)
# for child in interval.childs:
#     print(child, child.name)
# child1.delete()
# print()
# for child in interval.childs:
#     print(child, child.name)


class Template:
    def __init__(self, day):
        self.day = day
        self.time_intervals = []


intervals = [
    [[1, 10], [2, 30]],
    [[5, 0], [7, 0]],
    [[8, 0], [8, 30]],
    [[10, 0], [12, 0]],
    [[12, 30], [1, 30]],
    [[2, 00], [2, 45]],
    [[4, 40], [8, 30]]
]
# print(datetime.today())
# print(date.today())
# start_time = list(map(int, input("Enter session start time (hh:mm [24hr format]): ").split(':')))
# end_time = list(map(int, input("Enter session end time (hh:mm [24hr format]): ").split(':')))
# print(start_time, end_time)
print(str(date.today()))



