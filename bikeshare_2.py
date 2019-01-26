import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ["january", "february", "march", "april", "may", "june", "july", "september", "october", "november", "december"]


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    class Error(Exception):
        pass

    class CityInputError(Error):
        pass

    class MonthInputError(Error):
        pass

    class DayInputError(Error):
        pass

    while True:
        try:
            city = str(input("Choose a city to analyze: Chicago, New York City, Washington.\n > ")).lower()
            if city not in CITY_DATA.keys():
                raise CityInputError
            break
        except CityInputError:
            print("Your input doesn't match any of the city names.")
            print("Please try again.")


    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input("Choose a month or type 'all' for no filter.\n > ")).lower()
            if month not in months and month.lower() != "all":
                raise MonthInputError
            break
        except MonthInputError:
            print("Your input doesn't match a month's name nor is it 'all'.")
            print("Please try again.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    while True:
        try:
            day = str(input("Choose a day of the week or type 'all' for no filter.\n > ")).lower()
            if day not in days and day != "all":
                raise DayInputError
            break
        except DayInputError:
            print("Your input doesn't match a day of the week nor is it 'all'.")
            print("Please try again.")

    if month != "all" and day != "all":
        print("Looking up data for {}, filtered by the month of {} and {}s.".format(city.title(), month.title(), day.title()))
    elif month == "all" and day == "all":
        print("Looking up data for {}, unfiltered.".format(city.title()))
    elif month == "all":
        print("Looking up data for {}, filtered by {}s.".format(city.title(), day.title()))
    else:
        print("Looking up data for {}, filtered by the month of {}.\n".format(city.title(), month.title()))


    print('-'*40)
    print('-'*40)
    return city, month, day

def raw_data_display(df, increment=5):
    """
    Takes in a DataFrame and use input.
    Prints out several rows at a time, specified by increment.
    Continues printing until input is not yes or DataFrame ends.
    """

    with pd.option_context('display.max_rows', increment, 'display.max_columns', None):
        print("\nHere comes the firehose:\n")
        start_index = 0
        print(df[start_index:start_index+increment])
        start_index += increment
        more = str(input("\nWould you like to see {} more rows of data?\nType 'yes' or anything else to quit.\n > ".format(increment)))
        while more.lower() == "yes" and start_index < df.index.size:
            print(df[start_index:start_index+increment])
            start_index += increment
            more = str(input("\nWould you like to see {} more rows of data?\nType 'yes' or anything else to quit.\n > ".format(increment)).lower())


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    filename = CITY_DATA[city]
    df = pd.read_csv(filename)

    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["Month"] = df["Start Time"].dt.month
    df["Day_of_week"] = df["Start Time"].dt.weekday_name
    df["Hour"] = df["Start Time"].dt.hour

    if month != "all" and (months.index(month) + 1) not in df["Month"].unique():
        print("\nSorry, there is no data available for {}.".format(month))
        print("Showing data for all the available months.\n")
        month = "all"

    if month != "all":
        month = months.index(month) + 1
        df = df[df["Month"] == month]

    if day != "all":
        df = df[df["Day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    top_month = df["Month"].mode()[0]
    top_month = months[top_month - 1]
    print("\nThe most common month is {}.".format(top_month.title()))
    more_month_data = str(input("\nWould you like to see more month data?\nType 'yes' to proceed or anything else to skip.\n > ")).lower()
    if more_month_data == "yes":
        print("\nTrip duration totals by month:")
        print(df.groupby(["Month"])["Trip Duration"].sum().apply(lambda x: datetime.timedelta(seconds=int(x))))
        print("\nTrip duration averages by month:")
        print(df.groupby(["Month"])["Trip Duration"].mean().apply(lambda x: datetime.timedelta(seconds=int(x))))
        print("\nThe longest trip in each month:")
        print(df.groupby(["Month"])["Trip Duration"].max().apply(lambda x: datetime.timedelta(seconds=int(x))))
        print("\nThe shortest trip in each month:")
        print(df.groupby(["Month"])["Trip Duration"].min().apply(lambda x: datetime.timedelta(seconds=int(x))))

    print('-'*40)

    # display the most common day of week
    print("\nThe most common day of the week is {}.".format(df["Day_of_week"].mode()[0]))
    more_day_data = str(input("\nWould you like to see more day of the week data?\nType 'yes' to proceed or anything else to skip.\n > ")).lower()
    if more_day_data == "yes":
        print("\nTrip duration totals by day:")
        print(df.groupby(["Day_of_week"])["Trip Duration"].sum().apply(lambda x: datetime.timedelta(seconds=int(x))))
        print("\nTrip duration averages by day:")
        print(df.groupby(["Day_of_week"])["Trip Duration"].mean().apply(lambda x: datetime.timedelta(seconds=int(x))))
        print("\nThe longest trip on each day:")
        print(df.groupby(["Day_of_week"])["Trip Duration"].max().apply(lambda x: datetime.timedelta(seconds=int(x))))
        print("\nThe shortest trip on each day:")
        print(df.groupby(["Day_of_week"])["Trip Duration"].min().apply(lambda x: datetime.timedelta(seconds=int(x))))
    print('-'*40)

    # display the most common start hour
    print("\nThe most common start hour is {}:00.".format(df["Hour"].mode()[0]))
    more_hour_data = str(input("\nWould you like to see more hourly data?\nType 'yes' to proceed or anything else to skip.\n > ")).lower()
    if more_hour_data == "yes":
        print("\nTrip duration totals by the hour:")
        print(df.groupby(["Hour"])["Trip Duration"].sum().apply(lambda x: datetime.timedelta(seconds=int(x))))
        print("\nTrip duration averages by the hour:")
        print(df.groupby(["Hour"])["Trip Duration"].mean().apply(lambda x: datetime.timedelta(seconds=int(x))))
        print("\nThe longest trip for each hour:")
        print(df.groupby(["Hour"])["Trip Duration"].max().apply(lambda x: datetime.timedelta(seconds=int(x))))
        print("\nThe shortest trip for each hour:")
        print(df.groupby(["Hour"])["Trip Duration"].min().apply(lambda x: datetime.timedelta(seconds=int(x))))
    print('-'*40)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("\nThe most popular start station is {}.".format(df["Start Station"].mode()[0]))
    more_start_station_data = str(input("\nWould you like to see the top 10?\nType 'yes' to proceed or anything else to skip.\n > ")).lower()
    if more_start_station_data == "yes":
        ranking = df["Start Station"].value_counts(sort=True)
        print(ranking[:11])
    print('-'*40)



    # display most commonly used end station
    print("\nThe most popular end station is {}.".format(df["End Station"].mode()[0]))
    more_end_station_data = str(input("\nWould you like to see the top 10?\nType 'yes' to proceed or anything else to skip.\n > ")).lower()
    if more_end_station_data == "yes":
        ranking = df["End Station"].value_counts(sort=True)
        print(ranking[:11])
    print('-'*40)


    # display most frequent combination of start station and end station trip
    df["Route"] = df["Start Station"] + " - " + df["End Station"]
    print("\nThe most popular route is {}.".format(df["Route"].mode()[0]))
    more_route_data = str(input("\nWould you like to see the top 10?\nType 'yes' to proceed or anything else to skip.\n > ")).lower()
    if more_route_data == "yes":
        ranking = df["Route"].value_counts(sort=True)
        print(ranking[:11])
    print('-'*40)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = int(df["Trip Duration"].sum())
    print("\nTotal travel time is {:,} seconds.".format(total))
    print("Or {}.\n".format(datetime.timedelta(seconds=total)))

    # display mean travel time
    mean = int(df["Trip Duration"].mean())
    print("\nAverage travel time is {:,} seconds.".format(mean))
    print("Or {}.\n".format(datetime.timedelta(seconds=mean)))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nThe breakdown of users by type:")
    print(df["User Type"].value_counts())


    # Display counts of gender
    if city != "washington":
        print("\nThe breakdown of users by gender:")
        print(df["Gender"].value_counts())
    else:
        print("\nNo gender data available for {}.".format(city.title()))


    # Display earliest, most recent, and most common year of birth
    if city != "washington":
        print("\nThe earliest DOB is {}.".format(df["Birth Year"].min()))
        print("\nThe most recent DOB is {}.".format(df["Birth Year"].max()))
        print("\nThe most common DOB is {}.".format(df["Birth Year"].mode()[0]))
    else:
        print("\nNo DOB data available for {}.".format(city.title()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)


        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        raw_data = str(input("\nWould you like to see the raw data?\nType 'yes' to proceed or anything else to skip.\n > ")).lower()
        if raw_data == "yes":
            raw_df = load_data(city, month, day)
            raw_data_display(raw_df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
