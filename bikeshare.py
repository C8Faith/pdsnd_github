#import libraries and set display
import pandas as pd
import datetime as dt
import numpy as np
import time
pd.set_option('display.max_columns', 500)

def get_city():
    """Takes user input to load csv, apply month and/or day filter, and returns resulting dataframe

    INPUT:
    (str) city: user input required for city
    (dict) CITY_DATA: dictionary of cities and corresponding CSV files
    (function) choose_month: call filtering function for month

    OUTPUT:
    df: dataframe built from csv file related to city requested by user and filtered by month and day as requested.\
    Additional columns for Month and Weekday are created from 'Month Start' data.
    """
    #define dictionary of cities and corresponding CSV files
    CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

    #get user input
    city = input('What city would you like to explore? Please choose Chicago, New York City, or Washington. \n')

    while city.lower() not in CITY_DATA:
        #while loop asks for user input to select the file to load
        print('Oops! Let\'s try that again. You entered "{}"'.format(city))
        city = input('What city would you like to explore? Please choose Chicago, New York City, or Washington. ')

    else:
        # load data file into a dataframe and change Start and End time colums to datetime
        df = pd.read_csv(CITY_DATA[city.lower()], parse_dates=['Start Time', 'End Time'])
        #Create Month column from Start Time
        df['Month Start'] = pd.DatetimeIndex(df['Start Time']).month
        #Create Week Column from Start Time
        df['Weekday'] = pd.DatetimeIndex(df['Start Time']).dayofweek
        #Change name of Unnamed column to User ID
        df.rename( columns={'Unnamed: 0':'User ID'}, inplace=True )
        #Provide feedback to user to confirm actions completed
        print('Ok, let\'s explore {}!\n'.format(city.title()))
        #Pass newly created dataframe to filtering functions
        return date_filts(df)

def date_filts(df):
    """Receives user input and applies a filter to dataframe for day and month

    INPUT:
    (str) month_filt: user input Y or N
    (str) month: user input of at least the first three letters of month to use as a filter
    (dict) months_dict: dictionary of months and their numerical value (Jan - Jun only)
    (funct) choose_day: Function to receive user input to determine whether to apply a weekday filter for df

    OUTPUT:
    df: dataframe with date filters applied per user responses
    """
    months_dict = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6}

    #find out if user wants to apply a month filter
    month_filt = input('Would you like to apply a filter for a certain month? Answer Y or N:  ').lower()

    #action if user responds in the negative
    if month_filt[0] == 'n':
        print("\n Ok, no month filter will be applied! Let's move on.\n")
        #pass data frame to function that allows user to apply a weekday filter
        return choose_day(df)


    #action if user responds affirmatively
    elif month_filt[0] == 'y':
        month = input('Please type the name of the month you would like to use as a filter. You \
can choose any month between January and June.').lower()
        #compare first 3 characters of user response to dictionary of months
        while month[0:3] not in months_dict:
            #provide additional and specific guidance if user answer is not found in dictionary
            print("\nHm, let's try again. \n")
            month = input('Please type at least the first three letters of the name of the month you would like to use \
as a filter. \nYou can enter January, February, March, April, May, or June:').lower()
        else:
            #create filter
            applied_month = months_dict[month[0:3]]
            #provide feedback to user letting them know filter is applied
            print('\nA filter has been applied for month {}.'.format(applied_month))
            #apply filter
            df = df[df['Month Start'] == applied_month]
            #pass data frame to function that allows user to apply a weekday filter
            return choose_day(df)

    #error handling to have function call recursively until user provides input that moves the code to next step
    else:
        print("Please enter only Y or N.")
        return date_filts(df)


def choose_day(df):
    """Applies a weekday filter for dataframe based on user input

    INPUT:
    (str) day_filt: user input Y or N
    (str) day_value: user input of at least the first three letters of the day of the week to use as a filter
    (dict) weekday_dict: dictionary of weekdays and their value 0-6 (Monday - Sunday)
    (dict) weekday_print: dictionary with abbreviations and full names of weekdays


    OUTPUT:
    df: original dataframe or dataframe filtered by weekday per user input
    """
    weekday_dict = {'mon':0, 'tue':1, 'wed':2, 'thu':3, 'fri':4, 'sat':5, 'sun':6}
    weekday_print = {'mon':'monday', 'tue':'tuesday', 'wed':'wednesday', 'thu':'thursday', 'fri':'friday', 'sat':'saturday',\
    'sun':'sunday'}

    #Find out if user would like to apply a filter for weekday
    day_filt = input('Would you like to apply a filter for a weekday? Answer Y or N:  ').lower()

    #action if user responds in negative
    if day_filt[0] == 'n':
        print("\n Ok, no weekday filter will be applied! Let's move on.\n")
        return df

    #action if user responds affirmatively
    elif day_filt[0] == 'y':
        day_value = input('\nPlease type the name of the day you would like to use as a filter:  ').lower()
        #error handling in case user did not respond in recognizable terms
        while day_value[0:3] not in weekday_dict:
            day_value = input("\nLet's try that again. Enter the name of the day you would like to use as a filter:   ").lower()
        else:
            #create variable for value of filter for weekday
            applied_day = weekday_dict[day_value[0:3]]
            print(applied_day)
            #Print a readable message to confirm for user that the filter has been received and applied
            print('\nA filter has been applied for {}.'.format(weekday_print[day_value[0:3]].title()))
            #apply filter and return filtered dataframe
            df = df[df['Weekday'] == applied_day]
            return df
    #function calls itself until user provides input that moves the code to next step
    else:
        print("Please enter only Y or N.")
        return choose_day(df)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Travel Times...\n')
    start_time = time.time()

    # determine the most common month and format result
    mode_month = df['Month Start'].mode()[0]
    mode_month = pd.to_datetime(mode_month,format='%m')

    # determine the most common day of week
    mode_day = df['Weekday'].mode()[0]
    #create a variable of the date value to use in user feedback by pulling day_name from timestamp
    dayname = df.loc[df['Weekday'] == mode_day, 'Start Time'].iloc[0]

    #provide response to user
    print('\nThe most popular month for bicycle rides is {}, \nand the most popular day of the week to ride is {}.'\
          .format(mode_month.month_name(),dayname.day_name()))

    # display the most common start hour
    #Create a new column with only the starting hour from Start Time
    df['Hour Start'] = pd.DatetimeIndex(df['Start Time']).hour
    #define variable to contain the most common starting hour
    mode_hour = df['Hour Start'].mode()[0]
    #provide formatted data to user in terms of AM and PM
    if mode_hour <1:
        print('\nThe most common time to start travel is 12:00 am. That\'s early!')
    elif mode_hour > 12:
        mode_hour = mode_hour-12
        print('\nThe most common time to start travel is {}:00 pm.'.format(mode_hour))
    else:
        print('\nThe most common time to start travel is {}:00 am.'.format(mode_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def popular_trips(df):
    """Displays the most popular routes of travel."""

    print('\nLooking up the most popular routes...')
    start_time = time.time()

    # determine the most common starting location
    pop_start = df['Start Station'].mode()
    print('\nThere are {} different starting stations.'.format(len(pd.unique(df['Start Station']))))

    # determine the most common ending location
    pop_end = df['End Station'].mode()
    print('And there are {} different ending stations.'.format(len(pd.unique(df['End Station']))))

    #determine the most common combination of start and end stations
    pop_route = df.groupby(['Start Station', 'End Station']).size().idxmax()


    #share data with user
    if pop_start[0] == pop_end[0]:
        print('\nFor this data, the most popular place to start AND to end a trip is {}!\n'.format(pop_start[0]))
    else:
        print('\nFor this data, the most popular starting station is {}, \nand the most popular place ending station is {}.\n'\
        .format(pop_start[0], pop_end[0]))

    print('The most popular complete route to take is from {} to {}.'.format(pop_route[0], pop_route[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    #create a new column for trip times by subtracting the ending time stamp from the beginning
    df['Total Time'] = df['End Time'] - df['Start Time']
    #Get the sum of all values in this column as a variable
    all_time = df['Total Time'].sum()

    print('The total travel time for all trips in this dataset is {} hours.'.format(all_time))

    # display mean travel time
    print('The average travel time for the trips in this dataset is {} hours.'.format(df['Total Time'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    #find the number of unique values for each response in User Type column
    user_count = df['User Type'].value_counts()
    #create a variable that holds those values as relative frequencies
    sub_pct = df['User Type'].value_counts(normalize=True)

    print('The number of subscribing users is {:,}, compared to {:,} non-subscribing customers.'\
          .format(user_count['Subscriber'], user_count['Customer']))
    #Express the # of subscribers as a percentage
    print('{}% of the users who provided an answer in this dataset are subscribers.'\
          .format(round(sub_pct['Subscriber']*100)))
    print('The number of N/A responses is: {}.'.format(df['User Type'].isna().sum()))

    # Display counts of gender
    if 'Gender' in df.columns:
        #Address N/A values by showing there was no answer
        df['Gender'] = df['Gender'].fillna('No Answer')
        gender = df['Gender'].value_counts()
        print('There are {:,} male users, {:,} female users, and {:,} people did not respond with gender information.'\
.format(gender['Male'], gender['Female'], gender['No Answer']))

    else:
        print('There is no information identifying users by gender in this dataset.')# Display counts of gender

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nThe earliest listed year of birth for the customers in this dataset is {}.'.format(int(df['Birth Year'].min())))
        print('The most recent birth year is {}, and the most commonly reported birth year is {}.'\
              .format(int(df['Birth Year'].max()), int(df['Birth Year'].mode())))
    else:
        pass

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw(df):
    """Takes user input to determine whether or not to display 5 rows of raw data. If user says yes,
    dataframe is sliced and displayed. Each time the user responds affirmitavely, 5 more rows are displayed.
    User input is evaluated by the first letter of their response.

    INPUT:
    (str) display: user input Y or N
    (int) start: value of starting slice, set at 0, manipulated by loop
    (int) stop: value of ending slice, set at 5, manipulated by loop

    OUTPUT:
    Rows of raw data in dataframe, displayed in sets of 5
    """
    display = input("Would you like to see 5 rows of raw data? Enter Y or N:").lower()
    start = 0
    stop = 5


    #use while loop to manipulate start and stop variables to add 5 each time user responds in the affirmative

    #Use Try and Except blocks to catch errors and continue running this function until no errors occur

    while display[0] == "y":
        print(df.iloc[start:stop])
        start+=5
        stop+=5
        #if statement to address the end of the data set
        if stop>len(df):
            stop = len(df)+1
            print(df.iloc[start:stop])
            print('You have reached the end of the data set')
            break
        else:
            display = input("\nWould you like to see 5 more rows of raw data? Enter Y or N:\n").lower()
            if display[0] == 'n':
                print('\nOk, you\'ve had your fill of data, I see.')
                break
            else:
                continue
    else:
        try:
            if display[0] == "n":
                print('\nNo data for you!')
            elif display[0] != "y" and display[0] != "n":
                print('\nHm. We ran into a problem understanding your response.')
                display_raw(df)
        except:
            print('\nWe ran into an error. Let\'s check that question again.')
            display_raw(df)


def main():
    while True:
        #load the CSV file for user-selected city
        active_df = get_city()
        print('There are {} rows in this dataset.'.format(active_df.shape[0]))

        #display time statistics
        time_stats(active_df)

        #display route popularity
        popular_trips(active_df)

        #display statistics about the duration of trips
        trip_duration_stats(active_df)

        #display statistics about users
        user_stats(active_df)

        #Display raw data if user is interested
        display_raw(active_df)

        #find out if user would like to restart
        go_again = input('Would you like to reset the filters and start over? Enter Y or N:  ').lower()

        while go_again[0] == 'y':
              main()
        else:
            if go_again[0] != 'y' and go_again[0] != 'n':
                print('Please enter "Yes" or "No" to restart or exit, respectively.')
                go_again = input('Would you like to reset the filters and start over? Enter Y or N:  ').lower()
            else:
                print('Okay! Thanks for joining in, and have a great day!')
                break

if __name__ == "__main__":
	main()
