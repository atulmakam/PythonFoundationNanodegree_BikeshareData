import datetime
import pandas as pd
import calendar


def get_city():
    '''Asks the user for the name of a city and returns the filename for that city's bikeshare data.
    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    city = input('\nHello this is Atul Makam! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n').title()
    if city == 'Chicago' or city == 'C':
        return 'chicago.csv'
    elif city == 'New York' or city == "N":
        return 'new_york_city.csv'
    elif city == 'Washington' or city == 'W':
        return 'washington.csv'
    else:
        print("\nSorry! I'm not sure which city you're referring to. Please try again.")
        return get_city()


def get_time_period():
    '''Asks the user for a time period and returns the specified filter.
    Args:
        none.
    Returns:
        (list) with two str values:
            First value: the type of filter period (i.e. month, day or none)
            Second value: the specific filter period (e.g. March, Tuesday)
    '''
    time_period = input('\nWould you like to filter the data by month, day, or not at'
                        ' all? Type "none" for no time filter.\n').lower()
    if time_period == 'month' or time_period == 'm':
        return ['month', get_month()]
    elif time_period == 'day' or time_period == 'd':
        return ['day', get_day()]
    elif time_period == 'none' or time_period == 'n':
        return ['none', 'no filter']
    else:
        print("\nSorry! I'm not sure which time period you're trying to filter by. Please try again.")
        return get_time_period()


def get_month():
    '''Asks the user for a month and returns the specified month.
    Args:
        none.
    Returns:
        (str) String representation of month number, e.g. for January it returns '01'
    '''
    month = input('\nWhich month? January, February, March, April, May, or June?\n').title()
    if month == 'January':
        return '01'
    elif month == 'February':
        return '02'
    elif month == 'March':
        return '03'
    elif month == 'April':
        return '04'
    elif month == 'May':
        return '05'
    elif month == 'June':
        return '06'
    else:
        print("\nSorry! I'm not sure which month you're trying to filter by. Please try again.")
        return get_month()

def get_day():
    '''Asks the user for a day of the week and returns the specified day.
    Args:
        none.
    Returns:
        (int) Integer represention of the day of the week, e.g. for Monday it returns 0
    '''
    day_of_week = input('\nWhich day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').title()
    if day_of_week == 'Monday':
        return 0
    elif day_of_week == 'Tuesday':
        return 1
    elif day_of_week == 'Wednesday':
        return 2
    elif day_of_week == 'Thursday':
        return 3
    elif day_of_week == 'Friday':
        return 4
    elif day_of_week == 'Saturday':
        return 5
    elif day_of_week == 'Sunday':
        return 6
    else:
        print("\nSorry! I'm not sure which day of the week you're trying to filter by. Please try again.")
        return get_day()

def pop_month(df):
    '''Given a dataframe of bikeshare data, this function returns the month with the most trips.
    Args:
        df: dataframe of bikeshare data
    Returns:
        (str) String that says which month had the most trips
    '''
    trips_by_month = df.groupby('Month')['Start Time'].count()
    return "Most popular month for start time: " + calendar.month_name[int(trips_by_month.sort_values(ascending=False).index[0])]


def pop_day(df):
    '''Given a dataframe of bikeshare data, this function returns the day of the week with the most trips.
    Args:
        df: dataframe of bikeshare data
    Returns:
        (str) String that says which day had the most trips
    '''
    trips_by_day_of_week = df.groupby('Day of Week')['Start Time'].count()
    return "Most popular day of the week for start time is: " + calendar.day_name[int(trips_by_day_of_week.sort_values(ascending=False).index[0])]


def pop_hour(df):
    '''Given a dataframe of bikeshare data, this function returns the hour of the day with the most trips.
    Args:
        df: dataframe of bikeshare data
    Returns:
        (str) String that says which hour of the day had the most trips, e.g. '05 PM' or '11 AM'
    '''
    trips_by_hour_of_day = df.groupby('Hour of Day')['Start Time'].count()
    most_pop_hour_int = trips_by_hour_of_day.sort_values(ascending=False).index[0]
    d = datetime.datetime.strptime(most_pop_hour_int, "%H")
    return "Most popular hour of the day for start time: " + d.strftime("%I %p")

def trip_duration(df):
    '''Given a dataframe of bikeshare data, this function returns the total trip duration and average trip duration
    Args:
        df: dataframe of bikeshare data
    Returns:
        (list) with two str values:
            First value: String that says the total trip duration in years, days, hours, minutes, and seconds
            Second value: String that says the average trip duration in hours, minutes, and seconds
    '''
    tot_trip_dur = df['Trip Duration'].sum()
    avg_trip_dur = df['Trip Duration'].mean()
    m, s = divmod(tot_trip_dur, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    y, d = divmod(d, 365)
    tot_trip_dur = "\nTotal trip duration is: %d years %02d days %02d hrs %02d min %02d sec" % (y, d, h, m, s)
    m, s = divmod(avg_trip_dur, 60)
    h, m = divmod(m, 60)
    avg_trip_dur = "Average trip duration is: %d hrs %02d min %02d sec" % (h, m, s)
    return [tot_trip_dur, avg_trip_dur]

def pop_stat(df):
    '''Given a dataframe of bikeshare data, this function returns the most popular start and end stations
    Args:
        df: dataframe of bikeshare data
    Returns:
        (list) with two values:
            First value: String stating the name of the most popular start station
                and how many trips started from there and what percentage of trips
                that accounted for
            Second value: String stating the name of the most popular end station
                and how many trips started from there and what percentage of trips
                that accounted for
    '''
    start_stat_counts = df.groupby('Start Station')['Start Station'].count()
    end_stat_counts = df.groupby('End Station')['End Station'].count()
    sorted_start_stat = start_stat_counts.sort_values(ascending=False)
    sorted_end_stat = end_stat_counts.sort_values(ascending=False)
    tot_trips = df['Start Station'].count()
    most_pop_start_stat = "\nMost popular start station: " + sorted_start_stat.index[0] + " (" + str(sorted_start_stat[0]) + " trips, " + '{0:.2f}%'.format(((sorted_start_stat[0]/tot_trips) * 100)) + " of trips)"
    most_pop_end_stat = "Most popular end station: " + sorted_end_stat.index[0] + " (" + str(sorted_end_stat[0]) + " trips, " + '{0:.2f}%'.format(((sorted_end_stat[0]/tot_trips) * 100)) + " of trips)"
    return [most_pop_start_stat, most_pop_end_stat]


def pop_trip(df):
    '''Given a dataframe of bikeshare data, this function returns the most popular trip (i.e. combination of start station and end station)
    Args:
        df: dataframe of bikeshare data
    Returns:
        (str) String that gives the most popular combination of start and end
        stations, how many trips that were accounted for and the percentage of trips that were taken into account
    '''
    trip_counts = df.groupby(['Start Station', 'End Station'])['Start Time'].count()
    sorted_trip_stat = trip_counts.sort_values(ascending=False)
    tot_trips = df['Start Station'].count()
    return "Most popular trip: " + "\n  Start station: " + str(sorted_trip_stat.index[0][0]) + "\n  End station: " + str(sorted_trip_stat.index[0][1]) + "\n  (" + str(sorted_trip_stat[0]) +  " trips, " + '{0:.2f}%'.format(((sorted_trip_stat[0]/tot_trips) * 100)) + " of trips)"


def users(df):
    '''Given a dataframe of bikeshare data, this function returns the number of
        trips by user type
    Args:
        df: dataframe of bikeshare data
    Returns:
        (pandas series) where the index of each row is the user type and the value
            is how many trips that user type made
    '''
    user_type_counts = df.groupby('User Type')['User Type'].count()
    return user_type_counts


def gender(df):
    '''Given a dataframe of bikeshare data, this function returns the number of
        trips by gender
    Args:
        df: dataframe of bikeshare data
    Returns:
        (pandas series) where the index of each row is the gender and the value
            is how many trips that gender made
    '''
    gender_counts = df.groupby('Gender')['Gender'].count()
    return gender_counts


def birth_years(df):
    '''Given a dataframe of bikeshare data, this function returns the oldest
        birth year, the most recent birth year, and the most common birth year
    Args:
        df: dataframe of bikeshare data
    Returns:
        (list) with three values:
            value 1: String stating the earliest birth year
            value 2: String stating the most recent birth year 
            value 3: String stating the most common birth year
    '''
    earliest_birth_year = "Earliest birth year: " + str(int(df['Birth Year'].min()))
    most_recent_birth_year = "Most recent birth year: " + str(int(df['Birth Year'].max()))
    birth_year_counts = df.groupby('Birth Year')['Birth Year'].count()
    sorted_birth_years = birth_year_counts.sort_values(ascending=False)
    tot_trips = df['Birth Year'].count()
    most_common_birth_year = "Most common birth year: " + str(int(sorted_birth_years.index[0])) + " (" + str(sorted_birth_years.iloc[0]) + " trips, " + '{0:.2f}%'.format(((sorted_birth_years.iloc[0]/tot_trips) * 100)) + " of trips)"
    return [earliest_birth_year, most_recent_birth_year, most_common_birth_year]


def display_data(df, current_line):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more.
    Continues asking until they say stop.
    Args:
        df: dataframe of bikeshare data
    Returns:
        If the user says yes then this function returns the next five lines
            of the dataframe and then asks the question again by calling this
            function again (recursive)
        If the user says no then this function returns, but without any value
    '''
    display = input('\nWould you like to view individual trip data?'
                    ' Type \'yes\' or \'no\'.\n')
    display = display.lower()
    if display == 'yes' or display == 'y':
        print(df.iloc[current_line:current_line+5])
        current_line += 5
        return display_data(df, current_line)
    if display == 'no' or display == 'n':
        return
    else:
        print("\nSorry! I'm not sure if you wanted to see more data or not. Please try again.")
        return display_data(df, current_line)


def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.
    Args:
        none.
    Returns:
        none.
    '''
    # Filter by city (Chicago, New York, Washington)
    city = get_city()
    print('Loading data...')
    city_df = pd.read_csv(city)

    def get_day_of_week(str_date):
        '''Takes a date in the format yyyy-mm-dd and returns an integer
            represention of the day of the week, e.g. for Monday it returns 0
        Args:
            str_date: date in the format yyyy-mm-dd
        Returns:
            (int) Integer represention of the day of the week,
                e.g. for Monday it returns 0
        '''
    #parse string in format yyyy-mm-dd and create date object based on those values.
        date_obj = datetime.date(int(str_date[0:4]), int(str_date[5:7]), int(str_date[8:10]))
        return date_obj.weekday()
    city_df['Day of Week'] = city_df['Start Time'].apply(get_day_of_week)
    city_df['Month'] = city_df['Start Time'].str[5:7]
    city_df['Hour of Day'] = city_df['Start Time'].str[11:13]

    # Filter by time period that the user specifies (month, day, none)
    time_period = get_time_period()
    filter_period = time_period[0]
    filter_period_value = time_period[1]
    filter_period_label = 'No filter'

    if filter_period == 'none':
        filtered_df = city_df
    elif filter_period == 'month':
        filtered_df = city_df.loc[city_df['Month'] == filter_period_value]
        filter_period_label = calendar.month_name[int(filter_period_value)]
    elif filter_period == 'day':
        filtered_df = city_df.loc[city_df['Day of Week'] == filter_period_value]
        filter_period_label = calendar.day_name[int(filter_period_value)]

    #Print a heading that specifies which city this data is for and any filters that were applied
    print('\n')
    print(city[:-4].upper().replace("_", " ") + ' -- ' + filter_period_label.upper())
    print('-------------------------------------')

    #print the total number of trips for this city and filter
    print('Total trips: ' + "{:,}".format(filtered_df['Start Time'].count()))

    #most popular month for start time
    if filter_period == 'none' or filter_period == 'day':
        print(pop_month(filtered_df))

    #most popular day of week for start time
    if filter_period == 'none' or filter_period == 'month':
        print(pop_day(filtered_df))

    #most popular hour of day for start time?
    print(pop_hour(filtered_df))

    #total trip duration and average trip duration
    trip_duration_stats = trip_duration(filtered_df)
    print(trip_duration_stats[0])
    print(trip_duration_stats[1])

    #most popular start station and most popular end station
    most_popular_stations = pop_stat(filtered_df)
    print(most_popular_stations[0])
    print(most_popular_stations[1])

    #most popular trip
    print(pop_trip(filtered_df))

    #counts of each user type?
    print('')
    print(users(filtered_df))

    if city == 'chicago.csv' or city == 'new_york_city.csv':
        #counts of gender
        print('')
        print(gender(filtered_df))
        # What are the earliest, most recent and most popular birth years?
        birth_years_data = birth_years(filtered_df)
        print('')
        print(birth_years_data[0])
        print(birth_years_data[1])
        print(birth_years_data[2])

    # Display five lines of data at a time if user specifies that they would like to
    display_data(filtered_df, 0)

    # Restart?
    def restart_question():
        '''Conditionally restarts the program based on the user's input
        Args:
            none.
        Returns:
        '''
        restart = input('\nWould you like to restart? Type \'yes\' or \'no\'. (If you say no the program will terminate.)\n')
        if restart.lower() == 'yes' or restart.lower() == 'y':
            statistics()
        elif restart.lower() == 'no' or restart.lower() == 'n':
            return
        else:
            print("\nI'm not sure if you wanted to restart or not. Please try again.")
            return restart_question()

    restart_question()


if __name__ == "__main__":
    statistics()
