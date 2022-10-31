import datetime
import pandas as pd
import requests


def list_to_dict(data_list):
    """
    Converts a list of stats to a list of dictionaries with needed stats
    """
    month_list = [None,
                  'Jan',
                  'Feb',
                  'Mar',
                  'Apr',
                  'May',
                  'Jun',
                  'Jul',
                  'Aug',
                  'Sep',
                  'Oct',
                  'Nov',
                  'Dec']
    index = 0
    for entry in data_list:

        # Date and time
        date_time = entry[0]
        date_time = date_time.split(" ")
        month = month_list.index(date_time[0])
        day = int(date_time[1])
        year = int(date_time[2])
        hour = int(date_time[3].split(":")[0])
        date_time = datetime.datetime(
            year, month, day, hour=hour, minute=0, second=0)

        # Price
        price = str(entry[1]).replace('.', ',')

        # Amount sold
        sold = entry[2]

        # compile dictionary and add it back to the list
        data_dict = {
            "Date": date_time,
            "Price(USD)": price,
            "Amount sold": sold
        }
        data_list[index] = data_dict

        index += 1

    return data_list


def get_df_for_item(item_name):
    item_name = item_name.replace(" ", "%20")
    item_name = item_name.replace("&", "%26")
    url = "https://steamcommunity.com/market/listings/730/" + item_name
    steam_str = requests.get(url).text
    steam_str = steam_str[steam_str.find("line1")+6:]
    steam_str = steam_str[0:steam_str.find("]];")+2]
    data_list = eval(steam_str)
    data_list = list_to_dict(data_list)
    df = pd.DataFrame.from_dict(data_list)
    return df


def write_df_to_file(df, item_name):
    file = open(item_name.replace(":", "") + '.csv', 'w')
    file.write(df.to_csv())
    file.close()


def read_file_to_df(item_name):
    item_name = item_name.replace(" ", "%20")
    item_name = item_name.replace("&", "%26")
    return pd.read_csv(item_name.replace(":", "") + ".csv")
