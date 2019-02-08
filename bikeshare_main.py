import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_choose_list = {"january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "all": "all"}
day_choose_list = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6, "all": "all"}
restart_choose_list = ["yes", "no"]

def user_input_check(user_input, choose_list, category):
    base_text = "Please choose "
    while user_input not in choose_list:
        if category == "city":
            user_input = input(base_text + "a valid city! : ").lower()
        elif category == "month":
            user_input = input(base_text + "a valid month! : ").lower()
        elif category == "day_of_week":
            user_input = input(base_text + "a valid day of the week! : ").lower()
        elif category == "yes_or_no":
            user_input = input(base_text + "either 'yes' or 'no' : ").lower()

    return user_input


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
    user_city_input = input("Which city would you like to analyze ? \nChoose chicago, new york city, washington : ").lower()
    user_city_input = user_input_check(user_city_input, CITY_DATA, "city")
    city = CITY_DATA[user_city_input]

    # get user input for month (all, january, february, ... , june)
    user_month_input = input("Which month would you like to analyze ? \nChoose any month from january to june. Choose 'all' if you want to see every month : ").lower()
    user_month_input = user_input_check(user_month_input, month_choose_list, "month")
    month = month_choose_list[user_month_input]

    # get user input for day of week (all, monday, tuesday, ... sunday)
    user_day_input = input("Which day of the week would you like to analyze ? \nChoose any day of the week. Choose 'all' if you want to see all : ").lower()
    user_day_input = user_input_check(user_day_input, day_choose_list, "day_of_week")
    day = day_choose_list[user_day_input]

    print("\n" + '-'*40)
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

    df = pd.read_csv(city)
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.dayofweek

    if month != "all":
        df = df[df["month"] == month]

    if day != "all":
        df = df[df["day_of_week"] == day]

    df = df.reset_index(drop = True)
    return df, city, month, day


def time_stats(df, city, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == "all":
        common_month = df["month"].mode()
        common_month_count = df["month"].value_counts().max()

        for key, value in month_choose_list.items():
            if value == common_month[0]:
                print("The most common month is {}. A total of {} trips were made".format(key, common_month_count))

    # display the most common day of week
    if day == "all":
        common_day = df["day_of_week"].mode()
        common_day_count = df["day_of_week"].value_counts().max()

        for key, value in day_choose_list.items():
            if value == common_day[0]:
                print("The most common day of the week is {}. A total of {} trips were made".format(key, common_day_count))

    # display the most common start hour
    common_starthour = df["Start Time"].dt.hour.mode()
    common_starthour_count = df["Start Time"].dt.hour.value_counts().max()
    print("The most common starting hour of the trip is the {}th hour. A total of {} trips were made".format(common_starthour[0], common_starthour_count))

    # display the most common end hour
    common_endhour = df["End Time"].dt.hour.mode()
    common_endhour_count = df["End Time"].dt.hour.value_counts().max()
    print("The most common ending hour of the trip is the {}th hour. A total of {} trips were made".format(common_endhour[0], common_endhour_count))

    # display the average duration of all trips
    average_duration = df["Trip Duration"].mean() / 60
    print("The average duration of the trips is {} minutes".format(round(average_duration)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_startstation = df["Start Station"].mode()
    common_startstation_count = df["Start Station"].value_counts().max()
    print("The most common starting station is {}. A total of {} trips were made".format(common_startstation[0], common_startstation_count))

    # display most commonly used end station
    common_endstation = df["End Station"].mode()
    common_endstation_count = df["End Station"].value_counts().max()
    print("The most common ending station is {}. A total of {} trips were made".format(common_endstation[0], common_endstation_count))

    # display most frequent combination of start station and end station trip
    journeys_df = df["Start Station"].str.cat(df["End Station"], sep = "__")
    common_journey = journeys_df.mode()[0].split("__")
    common_journey_count = journeys_df.value_counts().max()

    print("The most common trips start from {} and end at {}. A total of {} trips were made".format(common_journey[0], common_journey[1], common_journey_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum() / (60 * 60)
    print("The total travel time is {} hours".format(int(round(total_travel_time))))

    # display mean travel time
    average_travel_time = df["Trip Duration"].mean() / 60
    print("The average travel time per trip is {} minutes".format(int(round(average_travel_time))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts().keys().tolist()
    user_type_counts = df["User Type"].value_counts()
    print("The types of users and their quantities are :\n")

    for index in user_types:
        print("{}: {}".format(index, user_type_counts[index]))

    print("\n")

    # Display counts of gender
    if "Gender" in df:
        df["Gender"] = df["Gender"].fillna("Gender not specified")
        gender_types = df["Gender"].value_counts().keys().tolist()
        gender_type_counts = df["Gender"].value_counts()
        print("The number of Male & Female bikers are :\n")

        for gender_index in gender_types:
            print("{}: {}".format(gender_index, gender_type_counts[gender_index]))

        print("\n")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        datetime_now = datetime.datetime.now()

        def get_age(birth_year):
            age = datetime_now.year - birth_year
            return int(age)

        def print_user_stats(year, age, index, category):
            gender_name = "The person"
            if "Gender" in df:
                if df["Gender"][index].lstrip().rstrip().lower() == "male":
                    gender_name = "He"
                elif df["Gender"][index].lstrip().rstrip().lower() == "female":
                    gender_name = "She"

                print("The {} person to bike is {} years old. ".format(category, age) + gender_name + " was born in {}".format(year))
            else:
                print("The {} person to bike is {} years old. ".format(category, age) + gender_name + " was born in {}".format(year))

        # data for the earliest year
        earliest_year = df["Birth Year"].min()
        oldest_age = get_age(earliest_year)
        earliest_year_index = df["Birth Year"].idxmin()
        #print(df["Gender"][earliest_year_index])
        print_user_stats(int(earliest_year), oldest_age, earliest_year_index, "oldest")

        # data for the latest year
        latest_year = df["Birth Year"].max()
        youngest_age = get_age(latest_year)
        latest_year_index = df["Birth Year"].idxmax()
        print_user_stats(int(latest_year), youngest_age, latest_year_index, "youngest")

        # data for the most common
        most_common_year = df["Birth Year"].mode()[0]
        most_common_age = get_age(most_common_year)
        print("The most common age for biking is {}. The person was likely born in {}".format(most_common_age, int(most_common_year)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    city, month, day = get_filters()
    df, city, month, day = load_data(city, month, day)
    time_stats(df, city, month, day)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)
    raw_trip_data(df, 0)


def raw_trip_data(df, check):
    if check == 0:
        user_choice_raw_trip = input("\nWould you like to view individual trip data ? : ").lower()
        user_choice_raw_trip = user_input_check(user_choice_raw_trip, restart_choose_list, "yes_or_no")
    elif check > 0:
        user_choice_raw_trip = input("\nWould you like to see the next six rows ? : ").lower()
        user_choice_raw_trip = user_input_check(user_choice_raw_trip, restart_choose_list, "yes_or_no")

    show_raw_trip_data(df, user_choice_raw_trip, check)


def show_raw_trip_data(df, user_choice, check):
    if user_choice == "yes":
        print(df.ix[check : check + 5])
        check = check + 5
        raw_trip_data(df, check)
    else:
        restart_program()


def restart_program():

    user_choice = input("\nWould you like to restart the program ? : ").lower()

    while user_choice not in restart_choose_list:
        user_choice = input("\nPlease choose 'yes' or 'no' ! : ").lower()

    if user_choice == "yes":
        main()
    else:
        print("\nHope you liked my programming skills ! \nMade with passion, by Gladston\n")
        exit()

if __name__ == "__main__":
	main()
