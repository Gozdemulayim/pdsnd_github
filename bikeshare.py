import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday' ]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Enter the city to be analyzed:').lower()
    while city not in CITY_DATA.keys():
        city = input(city + ' is not a valid city in the data set. They should be one of (new york city, chicago, washington):')

    # TO DO: get user input for month (all, january, february, ... , june)
    
    month = input('Enter a month to be analyzed in [january:june] or type \'all\' for all months:').lower()
    while month not in MONTHS and month != 'all' :
        month = input(month + ' is not a valid month in the data set. Enter one of (all, january, february, ... , june):').lower()
    

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Enter day of a week to be analyzed in (all, monday, tuesday, ... sunday): ').lower()
    while day not in DAYS and day != 'all' :
        day = input(day + ' is not a valid day. Don\'t you know the days of week:').lower()
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    df['trip'] = df['Start Station'] + ' -> ' + df['End Station']
    
    # if a specific month, only get its data
    if month != 'all':
        month = MONTHS.index(month) + 1
        df = df[df['month'] == month]

    # if a specific day, only get its data
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
        
    rows = df.iloc[0:5]
    print('---------------------------------')
    print('Data summary for city: ', city, ' month:', month, ' day:', day)
    print('These are the available columns in the data:')
    print(rows.columns)
    print('---------------------------------')
    print('First 5 rows of the data:')
    
#     since all columns are not shown good, only an important subset is of columns are shown. Above I showed all the columns 
#     so the user will know what is in the data
    print(rows[['Start Time', 'End Time', 'trip']])
       
    showData= input('Would you like to see the first 5 rows of the data? (No by default)')
    count=0
    while showData == 'yes' :
        count = count+1
        rows = df.iloc[count*5:count*5+5]
        print('Next 5 rows of the data:')
        print(rows[['Start Time', 'End Time', 'trip']])
        showData= input('Would you like to see the next 5 rows of the data (yes or no)? (no by default)')
    
    print('---------------------------------')
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    mc_month = df['month'].mode()[0]
    print('Most common month:', MONTHS[mc_month-1].title())


    # TO DO: display the most common day of week
    mc_weekday = df['day_of_week'].mode()[0]
    print('Most common day of week:', mc_weekday)

    # TO DO: display the most common start hour
    mc_hour = df['hour'].mode()[0]
    print('Most common start hour:', mc_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    mc_startStation = df['Start Station'].mode()[0]
    print('Most common Start Station:', mc_startStation)

    # TO DO: display most commonly used end station
    mc_endStation = df['End Station'].mode()[0]
    print('Most common End Station:', mc_endStation)

    # TO DO: display most frequent combination of start station and end station trip
    mc_trip = df['trip'].mode()[0]
    print('Most common trip:', mc_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    to_travel_time = df['Trip Duration'].sum()
    print('Total travel time:', to_travel_time, 'seconds')


    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time, 'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts().to_frame())
    print('')

    # TO DO: Display counts of gender

    if 'Gender' not in df.keys():
        print('Gender data could not be found for this city')
    else:
        print(df['Gender'].value_counts().to_frame())



    # TO DO: Display earliest, most recent, and most common year of birth
    print('')
    
    if 'Birth Year' not in df.keys():
        print('Birth Year data could not be found for this city')
    else:
        print('Earliest year of birth:', df['Birth Year'].min())
        print('Most recent year of birth:', df['Birth Year'].max())
        print('Most common year of birth:', df['Birth Year'].mode()[0])    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
