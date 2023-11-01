import time
import pandas as pd
import numpy as np
import os
if os.name == 'nt':
    import msvcrt
elif os.name == 'posix':
    import tty, sys, termios
else: 
    print('The operating system you are using is not able to be tested, therefore, not supported.\nPlease change to Windows or Linux.\n HINT: The Udacity workspace is Linux.')
    exit()


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_LIST = ('All', 'January', 'February', 'March', 'April', 'May', 'June')
DAY_LIST = ('All','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')


def clear_terminal():
    """
    Detects os then runs the appropriate command to clear the terminal
    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def key_press():
    """
    Detects os, then asks the user if they would like to continue
    """
    print('\n\nPress any key to continue...')
    if os.name == 'nt':
        msvcrt.getch()
    else: 
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    clear_terminal()
   
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
    print('What city did you want to look at?')
    input_city = ""
    while input_city not in CITY_DATA:
        input_city = input('Type "Chicago", "New York City", or "Washington": ').lower()
    city = input_city
    # get user input for month (all, january, february, ... , june)
    input_month = ""
    while input_month not in MONTH_LIST:
        print('What month did you want to see?')
        input_month = input(f'Type a month:\n{MONTH_LIST}:\n> ').title()
    month = input_month
    # get user input for day of week (all, monday, tuesday, ... sunday)
    input_day = ""
    while input_day not in DAY_LIST:
        print('What day of the week did you want to see?')
        input_day = input(f'Type a day:\n{DAY_LIST}:\n > ').title()
    day = input_day
    clear_terminal()
    load_message = "\n\n\nLoading data for: \nCity: {}\nMonth: {}\nDay: {}\n".format(city.title(),month,day)
    print(load_message)
    print('-'*40)
    key_press()
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
    # Get the correct csv 
    df = pd.read_csv(CITY_DATA[city])
    # Convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Create columns for month and day
    df['month_name'] = df['Start Time'].dt.month_name()
    df['day_name'] = df['Start Time'].dt.day_name()
    # Filter by month and day
    if month != 'All':
        df = df[df['month_name'] == month]
    if day != 'All':
        df = df[df['day_name'] == day]
    return df

def display_data(df):
    """
    Iterates through the df 5 rows at a time
    """
    start_time = time.time()
    next_res = ('yes', 'no')
    input_next = input(f"Did you want to see the first five rows of data? \nType {next_res}> ").lower() 
    clear_terminal()
    while input_next not in next_res:
        input_next = input(f"Invalid response. Try again. Type {next_res}> ").lower()
    if input_next == 'yes': 
        start = 0
        end = 5
        rows = df.iloc[start:end]
        print(rows)
        print('_'*40)
    if input_next == 'yes':
        while input_next in next_res: 
            input_next = input(f"Show next five rows? \nType {next_res}").lower()
            while input_next not in next_res:
                input_next = input(f"Invalid response. Try again. Type {next_res}> ").lower()
            if input_next == 'yes':
                clear_terminal()
                start += 5
                end += 5
                rows = df.iloc[start:end]
                print(rows)
                print('_'*40)
            else: 
                break
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    key_press()
    clear_terminal()

def time_stats(df, city):
    """
    Displays statistics on the most frequent times of travel.
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # get the most common month
    pop_month = df['month_name'].mode()[0]
    # get the most common day of week
    pop_day = df['day_name'].mode()[0]
    # get the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    pop_hour = df['hour'].mode()[0]
    # display results
    print(f"\nThe most common month in {city.title()} is: {pop_month}")
    print(f'\nThe most common day in {city.title()} is: {pop_day}' )
    print(f'\nThe most common start hour in {city.title()} is: {pop_hour}:00')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    key_press()
    clear_terminal()

def station_stats(df,city):
    """
    Displays statistics on the most popular stations and trip.
    """    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # get the most commonly used start station
    start_station_count = df['Start Station'].value_counts()
    pop_start_station = start_station_count.head(1)
    # get most commonly used end station
    end_station_count = df['End Station'].value_counts()
    pop_end_station = end_station_count.head(1)
    # get most frequent combination of start station and end station trip
    df['trip_stations'] = df['Start Station'] + ' -> ' + df['End Station']
    trip_stations_count = df['trip_stations'].value_counts()
    pop_trip = trip_stations_count.head(1)
    # display results
    print(f"The most popular start station in {city.title()} is: \n{pop_start_station}")
    print(f"\nThe most popular end station in {city.title()} is: \n{pop_end_station}")
    print(f"\nThe most popular trip in {city.title()} is: \n{pop_trip}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    key_press()
    clear_terminal()

def trip_duration_stats(df, city):
    """
    Displays statistics on the total and average trip duration.
    """
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    # get total travel time
    sum_travel_time = sum(df['Trip Duration'])/86400
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()/60
    # Display Results
    print(f"The total travel time in {city.title()} was: {int(sum_travel_time)} Days")
    print(f"The mean travel time in {city.title()} was: {int(mean_travel_time)} Minutes") 
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    key_press()
    clear_terminal()

def user_stats(df,city):
    """
    Displays statistics on bikeshare users.
    """
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # get counts of user types
    user_type = df['User Type'].value_counts()
    # get counts of gender
    if 'Gender' in df.columns: 
        gender_count = df['Gender'].value_counts()
    else: 
        gender_count = f"Gender: \nThis data is not available in {city.title()}"
    # get earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns: 
        yob_youngest = int(df['Birth Year'].max())
        yob_oldest = int(df['Birth Year'].min())
        yob_common = int(df['Birth Year'].mode()[0])
    else: 
        yob_youngest = f"Youngest Birth Year Unavailable in {city.title()}"
        yob_oldest = f"Oldest Birth Year Unavailable in {city.title()}"
        yob_common = f"Most Common Birth Year Unavailable in {city.title()}"
    # Display Results
    print(f"{user_type}\n")
    print(f"\n{gender_count}\n")
    print(f"Birth Years: \n Youngest: {yob_youngest}\n Oldest: {yob_oldest}\n Most Common: {yob_common}")
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        clear_terminal()
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df, city)
        station_stats(df, city)
        trip_duration_stats(df, city)
        user_stats(df,city)

        restart_choice = ('yes','no')
        restart = input(f'\nWould you like to restart? Enter {restart_choice}\n').lower()
        while restart not in restart_choice:
            restart = input(f'\nInvalid Choice. Type: {restart_choice}').lower()
        if restart == 'no':
            break 
        
if __name__ == "__main__":
	main()
