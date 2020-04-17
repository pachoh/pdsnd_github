import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

cities = ['chicago', 'new york city', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = str(input('Which of these three cities would you like to analyze? "Chicago", "New York City" or "Washington"? Please enter your desired city: ')).lower()

    if city not in cities:
        while city not in cities:
            city = str(input('We are sorry, please select one of the three cities: ')).lower()
            if city in cities:
                print('You have selected the city of: ' + city + '.')
                break
    else:
        print('You have selected the city of: ' + city + '.')

    # get user input for month (all, january, february, ... , june)
    month = str(input('Would you like to filter by a certain month? If yes, please state a month between "January" and "June". If not, please return "all": ')).lower()

    if month == 'all':
        print('No filter for months will be applied.')
    elif month not in months:
        while month not in months:
            month = str(input('We are sorry, please type out a valid month: ')).lower()
            if month in months:
                print('You have selected the month of: ' + month + '.')
                break
    else:
        print('You have selected the month of: ' + month + '.')

    #: get user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input('Would you like to filter by a certain day of the week? If yes, please state a day between "Monday" and "Sunday". If not, please return "all": ')).lower()

    if day == 'all':
        print('No filter for days will be applied')
    elif day not in days:
        while day not in days:
            day = str(input('We are sorry, please type out a valid day: ')).lower()
            if day in days:
                print('You have selected the following day of the week: ' + day + '.')
                break
    else:
        print('You have selected the following day of the week: ' + day + '.')

    print('-'*40)
    return city, month, day


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
    # Note for reviewer: for this function I have used the solution for Practice Problem #3

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = months[df['month'].mode()[0] - 1].capitalize()
    print('Most common month: ', common_month)


    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('Most common day: ', common_day)


    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common start hour: ', common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most common start station: ', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most common end station: ', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + ' - ' + df['End Station']
    common_route = df['route'].mode()[0]
    print('Most common route: ', common_route)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # display total travel time
    travel_time = abs(df['End Time'] - df['Start Time'])
    total_travel_time = travel_time.sum()
    print('The total duration of the trips is: ', total_travel_time)

    # display mean travel time
    mean_travel_time = travel_time.mean()
    print('The average travel time per trip is: ', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_types = df['User Type'].value_counts()
    print('The count per user type is the following:\n', user_types)


    # display counts of gender
    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print('The count per gender is the following: \n', gender_count)

    # display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_yob = df['Birth Year'].min()
        most_recent_yob = df['Birth Year'].max()
        most_common_yob = df['Birth Year'].mode()[0]

        print('The earliest year of birth is: ', str(earliest_yob)[:4])
        print('The most recent year of birth is: ', str(most_recent_yob)[:4])
        print('The most common year of birth is: ', str(most_common_yob)[:4])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    user_input = input('Do you want to see raw data? Please state "yes" or "no".').lower()
    while user_input == 'yes':
        print(df.head())
        user_input = input('Do you want to see raw data? Please state "yes" or "no".').lower()
        if user_input == 'no':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
