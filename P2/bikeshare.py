import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    
    while True:
        city_list= ['chicago', 'new york', 'washington']
        city = input("Would you like to see data for Chicago, New York, or Washington?\n").lower()
        if city not in city_list:
            print('Please check city name and try again!!')
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month=input('Which month? Please Type: January, February, March, April, May,or June \n').lower()
    
        if month not in month_list:
            print('Please check month list and try again!!')
        else:
            break
         
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday) 
    while True:
        day_list=['sunday','monday','tuesday','wednesday','thursday', 'friday', 'saturday']
        day=input('Which day? Please type: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday \n').lower()
    
        if day not in day_list:
            print('Please check day list and try again!!')
        else:
            break    
        

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
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month
    # find the most popular month
    common_month = df['month'].mode()[0]
    print('Most common month:', common_month)
    # TO DO: display the most common day of week
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract date from the Start Time column to create a date column
    df['day'] = df['Start Time'].dt.date
    # find the most popular date
    common_day = df['day'].mode()[0]

    print('Most common day of week:', common_day)
    # TO DO: display the most common start hour
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start=df['Start Station'].mode()
    print('Most commonly used start station was:', common_start)
    

    # TO DO: display most commonly used end station
    common_end=df['End Station'].mode()
    print('Most commonly used end station:', common_end)

    # TO DO: display most frequent combination of start station and end station trip
    # Popular Trip is a NEW column includes Start Station and End Station
    df['Popular Trip']=df['Start Station'].str.cat(df['End Station'])
    
    # find the most frequent combination of start station and end station trip from Popular Trip column
    frequent_combination= df['Popular Trip'].mode()
    
    print('Most frequent combination of start station and end station trip:', frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total=df['Trip Duration'].sum()
    print('Total travel time:', total)

    # TO DO: display mean travel time
    avg=df['Trip Duration'].mean()
    print('Avg travel time:', avg)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    
    user_gender=df['Gender'].value_counts()
    print(user_gender)
        
        
    # TO DO: Display earliest, most recent, and most common year of birth
     
    earliest=df['Birth Year'].min()
    print('Earliest year of birth:',earliest)
    most_recent=df['Birth Year'].max()
    print('Most recent year of birth:', most_recent)
    coomn_birthyear= df['Birth Year'].mode()
    print('Most common year of birth:', coomn_birthyear)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display(df):
#'Display five lines of data when user select Yes
    row=0
    while True:
        select=input('Would you like to view individual trip data? Type Yes or No\n')
        if select.lower() == "yes":
            print(df[row:row+5])
            row+=5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        print('city: {}, month: {}, day: {}'.format(city, month, day))
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        while True:
            if city == 'chicago.csv' or city == 'new_york_city.csv':
                user_stats(df)
            else:
                break
                print('No information in this file')
        #user_stats(df)
        display(df)
        df['Popular Trip']=df['Start Station'].str.cat(df['End Station'])
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        print('Restart Again')
        

if __name__ == "__main__":
	main()
  