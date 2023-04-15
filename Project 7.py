import csv
from datetime import datetime
from operator import itemgetter

COLUMNS = ["date",  "average temp", "high temp", "low temp", "precipitation", \
           "snow", "snow depth"]

TOL = 0.02

BANNER = 'This program will take in csv files with weather data and compare \
the sets.\nThe data is available for high, low, and average temperatures,\
\nprecipitation, and snow and snow depth.'    


MENU = '''
        Menu Options:
        1. Highest value for a specific column for all cities
        2. Lowest value for a specific column for all cities
        3. Average value for a specific column for all cities
        4. Modes for a specific column for all cities
        5. Summary Statistics for a specific column for a specific city
        6. High and low averages for each category across all data
        7. Quit
        Menu Choice: '''
        
        
def open_files():  # sourcery skip: use-fstring-for-concatenation
    ''' Docstring'''
    city_names = input("Enter cities names: ")
    city_list = city_names.split(',')
    city_list_2, fp_list = [],[]
    for city in city_list:
        f_string = city + ".csv"
        try:
            fp_list.append(open(f_string))
            city_list_2.append(city)
        except Exception:
            print(f"\nError: File {f_string} is not found")

    return(city_list_2, fp_list)

def read_files(cities_fp):
    ''' Docstring'''
    master_list = []
    for fp in cities_fp:
        inner_list = []
        next(fp)
        next(fp)
        f_reader = csv.reader(fp)
        for row in f_reader:
            row_tuple = ()
            for value in row:
                if value == '':
                    row_tuple += (None,)
                elif value == row[0]:
                    row_tuple += (value,)
                else:
                    row_tuple += (float(value),)
            inner_list.append(row_tuple)
        master_list.append(inner_list)

    return master_list

def get_data_in_range(data, start_date_str, end__date_str):
    ''' Docstring'''
    start_date = datetime.strptime(start_date_str, "%m/%d/%Y").date()
    end_date = datetime.strptime(end__date_str,"%m/%d/%Y").date()
    data_mod = []
    for inner_list in data:
        inner_list_mod = []
        for data_tuple in inner_list:
            tuple_date = datetime.strptime(data_tuple[0],"%m/%d/%Y").date()
            if tuple_date >= start_date and tuple_date <= end_date:
                inner_list_mod.append(data_tuple)
        data_mod.append(inner_list_mod)
    return data_mod


def get_min(col, data, cities):
    ''' Docstring'''
    min_list = []
    for city_count, city in enumerate(data):
        col_value_list = [
            data_tuple[col] for data_tuple in city if data_tuple[col] != None
        ]
        min_value = min(col_value_list)
        min_list.append((cities[city_count],min_value))
    return min_list
        
def get_max(col, data, cities):
    ''' Docstring'''
    max_list = []
    for city_count, city in enumerate(data):
        col_value_list = [
            data_tuple[col] for data_tuple in city if data_tuple[col] != None
        ]
        max_value = max(col_value_list)
        max_list.append((cities[city_count],max_value))
    return max_list

def get_average(col, data, cities):
    ''' Docstring'''
    avg_list = []
    for city_count, city in enumerate(data):
        col_value_list = [
            data_tuple[col] for data_tuple in city if data_tuple[col] != None
        ]
        avg_value = round(sum(col_value_list)/len(col_value_list),2)
        avg_list.append((cities[city_count],avg_value))
    return avg_list

def get_modes(col,data,cities):
    final_list = []
    for city_name, city_data in zip(cities, data):
        column = sorted([value[col] for value in city_data if value[col] != None])
        count_list = []
        reprsentative_value = column[0]
        count = 1

        for i in range(1, len(column)):
            currentValue = column[i]

            tolerance = abs((reprsentative_value-currentValue)/reprsentative_value)

            if(tolerance < 0.02):
                count += 1
            else:
                count_list.append((count, reprsentative_value))
                reprsentative_value = column[i]
                count = 1

        count_list.append((count, reprsentative_value))

        max_count = 0
        max_list = []
        for value in count_list:
            if value[0] > max_count:
                max_count = value[0]
                max_list.clear()
            if value[0] == max_count and max_count > 1:
                max_list.append(value[1])
        
        final_list.append((city_name, max_list, max_count))

    return final_list
          
def high_low_averages(data, cities, categories):
    ''' Docstring'''
    final_list = []
    for category in categories:
        if category in COLUMNS:
            index = COLUMNS.index(category)
            high_avg, low_avg = 0,999999999
            for data_tuple in get_average(index,data,cities):
                if data_tuple[1] > high_avg:
                    high_avg = data_tuple[1]
                    high_avg_city = data_tuple[0]
                if data_tuple[1] < low_avg:
                    low_avg = data_tuple[1]
                    low_avg_city = data_tuple[0]
            category_list = [(low_avg_city, low_avg), (high_avg_city, high_avg)]
            final_list.append(category_list)
        else:
            final_list.append(None)

    return final_list

def display_statistics(col,data, cities):
    ''' Docstring'''
    pass   # remove this line
             
def main():
    print(BANNER)
    city_list, fp_list = open_files()
    master_list = read_files(fp_list)
    choice = int(input(MENU))
    while True:
        if choice == 1:
            start_date = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_date = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            category = input("\nEnter desired category: ").lower()
            if category in COLUMNS:
                categoy_index = COLUMNS.index(category)
                max_list = get_max(categoy_index, get_data_in_range(master_list,start_date,end_date), city_list)
                print(f"\n\t{category}: ")
                for index in range(len(city_list)):
                    print(f"\tMax for {max_list[index][0]:s}: {max_list[index][1]:.2f}")
            else:
                print(f"\n\t{category} category is not found.")
            choice = int(input(MENU))

        elif choice == 2:
            start_date = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_date = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            category = input("\nEnter desired category: ").lower()
            if category in COLUMNS:
                categoy_index = COLUMNS.index(category)
                min_list = get_min(categoy_index, get_data_in_range(master_list,start_date,end_date), city_list)
                print(f"\n\t{category}: ")
                for index in range(len(city_list)):
                    print(f"\tMin for {min_list[index][0]:s}: {min_list[index][1]:.2f}")
            else:
                print(f"\n\t{category} category is not found.")
            choice = int(input(MENU))

        elif choice == 3:
            start_date = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_date = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            category = input("\nEnter desired category: ").lower()
            if category in COLUMNS:
                categoy_index = COLUMNS.index(category)
                avg_list = get_average(categoy_index, get_data_in_range(master_list,start_date,end_date), city_list)
                print(f"\n\t{category}: ")
                for index in range(len(city_list)):
                    print(f"\tAverage for {avg_list[index][0]:s}: {avg_list[index][1]:.2f}")
            else:
                print(f"\n\t{category} category is not found.")
            choice = int(input(MENU))

        elif choice == 4:
            start_date = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_date = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            category = input("\nEnter desired category: ").lower()
            if category in COLUMNS:
                categoy_index = COLUMNS.index(category)
                mode_list = get_modes(categoy_index, get_data_in_range(master_list,start_date,end_date), city_list)
                print(f"\n\t{category}: ")
                for index in range(len(city_list)):
                    print(f"\tMost common repeated values for {mode_list[index][0]:s} ({mode_list[index][2]:d} occurrences): {mode_list[index][1]:s}\n")
            else:
                print(f"\n\t{category} category is not found.")
            choice = int(input(MENU))

        elif choice == 6:
            start_date = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_date = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            category_list = (input("\nEnter desired categories seperated by comma: ").lower()).split(',')
            high_low_avg_list = high_low_averages(get_data_in_range(master_list,start_date,end_date), city_list, category_list)

            print("\nHigh and low averages for each category across all data.")

            for category_count, category in enumerate(category_list):
                if category in COLUMNS:
                    categoy_index = COLUMNS.index(category)
                    print(f"\n\t{category}: ")
                    print(f"\tLowest Average: {high_low_avg_list[category_count][0][0]:s} = {high_low_avg_list[category_count][0][1]:.2f} Highest Average: {high_low_avg_list[category_count][1][0]:s} = {high_low_avg_list[category_count][1][1]:.2f}")
                else:
                    print(f"\n\t{category} category is not found.")
            choice = int(input(MENU))

        if choice == 7:
            print("\nThank you using this program!")
            break

#DO NOT CHANGE THE FOLLOWING TWO LINES OR ADD TO THEM
#ALL USER INTERACTIONS SHOULD BE IMPLEMENTED IN THE MAIN FUNCTION
if __name__ == "__main__":
    main()
            
