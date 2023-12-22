import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import datetime

'''
Была идея держать отдельно дни, недели, месяца и т.п., но я подумал, что достаточно просто деражать дни и всё. 
А для вывода графика брать нужное число дней.
'''

class Schedule:
    '''
    Class for storing all time data 

    num_activity_types: number of activity types
    days: list of days
    months: list of months
    years: list of years
    '''
    def __init__(self, activity_names):
        self.activity_names = activity_names

        self.current_day = None

        self.days = [] # up to 6 days
        self.weeks = [] # up to 4 weeks
        self.months = [] # up to 12 months
        self.years = []

    def begin_day(self):
        '''
        Creating new day
        '''
        self.current_day = Day(self.activity_names)

    def end_day(self):
        '''
        Adding current day to schedule and starting new day
        '''
        self.add_day(self.current_day)
        self.current_day = None


    def add_timestamp(self, activity, time_stamp):
        '''
        Adding timestamp to the current day in the schedule

        activity: name of activity
        time_stamp: TimeStamp object
        '''
        self.current_day.add_time(activity, time_stamp)

        
    def add_day(self, day):
        '''
        Adding day to schedule

        day: Day object
        '''
        self.days.append(day)
        if len(self.days) == 7:
            self.weeks.append(Week(self.activity_names))
            while self.days:
                self.weeks[-1].add_time(self.days.pop(0))
            self.days = []

        if len(self.weeks) == 5:
            self.months.append(Month(self.activity_names))
            while self.weeks:
                self.months[-1].add_time(self.weeks.pop(0))
            self.weeks = []

        if len(self.months) == 13:
            self.years.append(Year(self.activity_names))
            while self.months:
                self.years[-1].add_time(self.months.pop(0))
            self.months = []

    def show_time_distribution(self, activity, time_scale, position = 0):
        '''
        Show plot of activity's time distribution

        activity: name of activity
        time_scale: number of days to show; either "days" or "weeks" or "months" or "years"
        position: how many "time_scale"s to skip
        
        '''
        '''
        Добавь проверки. Сделай нормальное добавление дней в недели, чтобы можна было смотреть не полные недели и т.п.
        '''


        getattr(self, time_scale)[-1 - position].show_time_distribution(activity)


class TimeStamp:
    '''
    Class for storing time  
    '''
    def __init__(self, start, finish):
        self.start = start
        self.finish = finish

    def make_time_distribution(self, activity):
        '''
        Converting timestamp into range of minutes and adding it to distribution list

        activity: dummy argument to make it compatible with TimeLable-like object
        '''
        # Converting timestamp into range of minutes to catch activity's time distribution
        begining, end = self.start[0] * 60 + self.start[1], self.finish[0] * 60 + self.finish[1]
        return range(begining, end)


class TimeLable:
    def __init__(self):
        self.spended_time = []

    def add_time(self, time):
        '''
        Adding either timestamp (for class Day) or TimeLeble-like (for class Week, Month, Year) object to corresponding activity list
        '''
        self.spended_time.append(time)


    def make_time_distribution(self, activity):
        '''
        Converting timestamps (TimeLable-like object or timestamp) into range of minutes and adding them to distribution list
        '''
        distribution = []

        # Converting timestamps into range of minutes to catch activity's time distribution
        for lowerTimeLableInstance in self.spended_time:
            distribution.extend(lowerTimeLableInstance.make_time_distribution(activity))

        return distribution


    def show_time_distribution(self, activity):
        '''
        Show plot of activity's time distribution
        '''
        # Calculate the bin edges for 24 hours
        bin_edges = np.linspace(0, 1440, 25, endpoint=True)

        # Calculate distribution
        distribution = self.make_time_distribution(activity)

        # Calculate the bin centers to represent hours from 0 to 24
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        # Plot itself
        # sns.histplot(distribution) # add more bins for better visualization
        # sns.kdeplot(distribution)
        sns.displot(distribution, kind='hist', kde=True)

        # Adding proper x-axis ticks
        plt.xticks(bin_centers, [f"{i}:00" for i in range(24)])

        plt.xlabel("Time of day")
        plt.ylabel("Frequency")
        plt.title("Timetable")
        plt.show()


class Day(TimeLable):
    def __init__(self, activity_names):
        super().__init__()
        self.spended_time = {activity : [] for activity in activity_names}
        self.date = datetime.date.today().strftime("%d-%m-%YYYY")

    def add_time(self, activity, time):
        '''
        time: TimeStamp object
        '''
        self.spended_time[activity].append(time)
        
    
    def make_time_distribution(self, activity):
        '''
        Converting timestamps (TimeLable-like object or timestamp) into range of minutes and adding them to distribution list
        '''
        distribution = []

        # Converting timestamps into range of minutes to catch activity's time distribution
        for lowerTimeLableInstance in self.spended_time[activity]:
            distribution.extend(lowerTimeLableInstance.make_time_distribution(activity))

        return distribution

    def get_date(self):
        return self.date


class Week(TimeLable):
    def __init__(self):
        super().__init__()

    
class Month(TimeLable):
    def __inti__(self):
        super().__init__()
    

class Year(TimeLable):
    def __init__(self):
        super().__init__()