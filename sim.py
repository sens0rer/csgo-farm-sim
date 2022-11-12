import datetime as dt
import pricehistory
from time import sleep
import pandas as pd
import random
from progressbar import print_progress_bar
import matplotlib.pyplot as plt
import numpy as np

# Constants
_min_release_date = dt.date(2013, 8, 13)
_min_rare_date = dt.date(2014, 1, 14)
_max_date = dt.date(2030, 1, 1)
_min_non_prime_date = dt.date(2019, 10, 26)

_release_dates = {'Recoil Case': dt.date(2022, 7, 1),
                  'Dreams & Nightmares Case': dt.date(2022, 1, 21),
                  'Snakebite Case':  dt.date(2021, 5, 3),
                  'Clutch Case':  dt.date(2018, 2, 15),
                  'Fracture Case':  dt.date(2020, 8, 7),
                  'Prisma 2 Case': dt.date(2020, 4, 1),
                  'Danger Zone Case': dt.date(2018, 12, 6),
                  'CS20 Case':   dt.date(2019, 10, 18),
                  'Prisma Case':   dt.date(2019, 3, 13),
                  'Horizon Case':   dt.date(2018, 8, 2),
                  'Spectrum 2 Case':   dt.date(2017, 9, 14),
                  'Operation Hydra Case':   dt.date(2017, 5, 23),
                  'Spectrum Case':   dt.date(2017, 3, 15),
                  'Glove Case':   dt.date(2019, 3, 13),
                  'Gamma Case':   dt.date(2016, 6, 15),
                  'Gamma 2 Case':   dt.date(2016, 8, 18),
                  'Chroma 3 Case':   dt.date(2016, 4, 20),
                  'Revolver Case':   dt.date(2015, 12, 8),
                  'Operation Wildfire Case':   dt.date(2016, 2, 17),
                  'Shadow Case':   dt.date(2015, 9, 17),
                  'Falchion Case':   dt.date(2015, 5, 26),
                  'Chroma Case':   dt.date(2015, 1, 8),
                  'Chroma 2 Case':   dt.date(2015, 4, 15),
                  'Operation Vanguard Weapon Case':   dt.date(2014, 11, 11),
                  'Operation Breakout Weapon Case':   dt.date(2014, 7, 1),
                  'Huntsman Weapon Case':   dt.date(2014, 5, 1),
                  'Winter Offensive Weapon Case':   dt.date(2013, 12, 18),
                  'Operation Bravo Case':   dt.date(2013, 9, 19),
                  'CS:GO Weapon Case 2':   dt.date(2013, 11, 8),
                  'CS:GO Weapon Case 3':   dt.date(2014, 2, 12),
                  'CS:GO Weapon Case':   dt.date(2013, 8, 14),
                  'Sticker Capsule': _min_release_date,
                  'Sticker Capsule 2': _min_release_date,
                  'Community Sticker Capsule 1': _min_release_date
                  }

_non_prime_start_dates = {'Gamma Case': _min_non_prime_date,
                          'Gamma 2 Case': _min_non_prime_date,
                          'Shadow Case': _min_non_prime_date,
                          'Chroma 2 Case': _min_non_prime_date,
                          'Spectrum Case': _min_non_prime_date,
                          'Revolver Case': _min_non_prime_date,
                          'Chroma 3 Case': dt.date(2020, 4, 1),
                          'Horizon Case': dt.date(2020, 4, 1),
                          'Spectrum 2 Case': dt.date(2020, 4, 1),
                          'CS20 Case': dt.date(2020, 8, 7)}

_non_prime_end_dates = {'Gamma Case': dt.date(2018, 2, 15),
                        'Gamma 2 Case': dt.date(2021, 6, 3),
                        'Shadow Case': dt.date(2016, 8, 18),
                        'Chroma 2 Case': dt.date(2017, 3, 15),
                        'Spectrum Case': dt.date(2017, 3, 15),
                        'Revolver Case': dt.date(2021, 6, 3),
                        'Chroma 3 Case': dt.date(2021, 6, 3),
                        'Horizon Case': dt.date(2021, 6, 3),
                        'Spectrum 2 Case': dt.date(2021, 6, 3),
                        'CS20 Case': dt.date(2021, 6, 3)}

_non_prime_list = list(_non_prime_start_dates.keys())

_rare_dates = {'Recoil Case':  _max_date,
               'Snakebite Case':  _max_date,
               'Clutch Case':  _max_date,
               'Fracture Case':  _max_date,
               'Dreams & Nightmares Case':  _max_date,
               'Prisma 2 Case': dt.date(2022, 7, 1),
               'Danger Zone Case': dt.date(2022, 1, 18),
               'CS20 Case':   dt.date(2021, 6, 3),
               'Prisma Case':   dt.date(2021, 5, 3),
               'Horizon Case':   dt.date(2021, 6, 3),
               'Spectrum 2 Case':   dt.date(2021, 6, 3),
               'Operation Hydra Case':   dt.date(2017, 11, 13),
               'Spectrum Case':   dt.date(2017, 3, 15),
               'Glove Case':   dt.date(2018, 12, 6),
               'Gamma Case':   dt.date(2018, 2, 15),
               'Gamma 2 Case':   dt.date(2021, 6, 3),
               'Chroma 3 Case':   dt.date(2021, 6, 3),
               'Revolver Case':   dt.date(2021, 6, 3),
               'Operation Wildfire Case':   dt.date(2017, 9, 14),
               'Shadow Case':   dt.date(2016, 8, 18),
               'Falchion Case':   dt.date(2015, 6, 15),
               'Chroma Case':   dt.date(2015, 9, 9),
               'Chroma 2 Case':   dt.date(2017, 3, 15),
               'Operation Vanguard Weapon Case':   dt.date(2015, 3, 31),
               'Operation Breakout Weapon Case':   dt.date(2016, 4, 20),
               'Huntsman Weapon Case':   dt.date(2016, 4, 15),
               'Winter Offensive Weapon Case':   _min_rare_date,
               'Operation Bravo Case':   dt.date(2014, 2, 5),
               'CS:GO Weapon Case 2':   _min_rare_date,
               'CS:GO Weapon Case 3':   _min_rare_date,
               'CS:GO Weapon Case':   _min_rare_date,
               'Sticker Capsule': _min_rare_date,
               'Sticker Capsule 2': _min_rare_date,
               'Community Sticker Capsule 1': _min_rare_date
               }


def get_price_data(is_new: bool = True):
    """
    Get Steam price history for each item.
    If is_new == True, gets data from Steam servers and writes them
    to files.
    If is_new == False, loads data from previously written files.
    """
    price_data = {}
    dateformat = "%Y-%m-%d %H:%M:%S"
    case_list = list(_rare_dates.keys())
    l = len(case_list)
    for i, case in enumerate(case_list):
        if is_new:
            df = pricehistory.get_df_for_item(case)
            sleep(15)
            price_data[case] = df.to_dict()
            pricehistory.write_df_to_file(df, case)
            print_progress_bar(i + 1, l,
                               prefix='Acquiring price data from Steam:',
                               suffix='Complete', length=50)

            # Convert indexed dicts to lists
            price_data[case]['Amount sold'] = list(
                price_data[case]['Amount sold'].values()
            )
            price_data[case]['Date'] = list(
                price_data[case]['Date'].values()
            )
            price_data[case]['Price(USD)'] = list(
                price_data[case]['Price(USD)'].values()
            )
            # Convert strings to floats
            price_data[case]['Price(USD)'] = [float(
                x.replace(",", ".")
            ) for x in price_data[case]['Price(USD)']]
            continue

        price_data[case] = pricehistory.read_file_to_df(case).to_dict()
        # Remove dumb artifact
        price_data[case].pop("Unnamed: 0")
        # Convert indexed dicts to lists
        price_data[case]['Amount sold'] = list(
            price_data[case]['Amount sold'].values()
        )
        price_data[case]['Date'] = list(
            price_data[case]['Date'].values()
        )
        price_data[case]['Price(USD)'] = list(
            price_data[case]['Price(USD)'].values()
        )
        # Convert strings to datetimes
        price_data[case]['Date'] = [
            dt.datetime.strptime(x, dateformat) for x
            in price_data[case]['Date']]
        # Convert strings to floats
        price_data[case]['Price(USD)'] = [float(
            x.replace(",", ".")
        ) for x in price_data[case]['Price(USD)']]
    return price_data


class DateError(Exception):
    """
    Used for inappropriate dates
    """


class Structure():
    """
    Defines farm settings
    """

    def __init__(self,
                 acc_num=100,
                 start_date=dt.date(2021, 6, 9),
                 start_bal=0):
        if start_date < dt.date(2019, 10, 27):
            exception = f"""Only use dates after 27.10.2019, using earlier
dates results in inaccurate data.

Date entered: {start_date}"""
            raise DateError(exception)

        self.acc_num = acc_num
        self.date = start_date
        self.balance = start_bal


class DropManager():
    """
    Manages drop pools and drop events
    """

    def __init__(self, drop_pool, release_dates, date):
        self._rare_dates = drop_pool
        self._release_dates = release_dates
        self._release_date_list = list(release_dates.values())
        self.date = date
        self._active_pool = []
        self._rare_pool = []
        # Initialize drop pools
        for case in self._rare_dates.keys():
            rare_date = self._rare_dates.get(case)
            release_date = self._release_dates.get(
                case, _min_release_date)
            if case in _non_prime_list:
                ignore_start = _non_prime_start_dates[case]
                ignore_end = _non_prime_end_dates[case]
                if date >= ignore_start and date < ignore_end:
                    continue
            if date < rare_date and date >= release_date:
                self._active_pool.append(case)
                continue
            if date >= release_date:
                self._rare_pool.append(case)

    def _update_rare_dates(self, date):
        # Check if it's time to update the drop pools
        run_update = False
        if self._release_date_list != []:
            first_release = min(self._release_date_list)
            if date >= first_release:
                run_update = True
                while date >= first_release:
                    self._release_date_list.remove(first_release)
                    if self._release_date_list == []:
                        break
                    first_release = min(self._release_date_list)

        # The update part
        if run_update:
            self._active_pool = []
            self._rare_pool = []
            for case in self._rare_dates.keys():
                rare_date = self._rare_dates.get(case)
                release_date = self._release_dates.get(
                    case, _min_release_date)
                if case in _non_prime_list:
                    ignore_start = _non_prime_start_dates[case]
                    ignore_end = _non_prime_end_dates[case]
                    if date >= ignore_start and date < ignore_end:
                        continue
                if date < rare_date and date >= release_date:
                    self._active_pool.append(case)
                    continue
                if date >= release_date:
                    self._rare_pool.append(case)

    def _drop_event(self):
        if random.random() < 0.01:
            return self._rare_pool[random.randint(0,
                                                  len(self._rare_pool) - 1)
                                   ]
        else:
            return self._active_pool[random.randint(0,
                                                    len(self._active_pool) - 1)
                                     ]


class Farm(Structure, DropManager):
    def __init__(self,
                 price_data,
                 acc_num=100,
                 start_date=dt.date(2021, 6, 9),
                 start_bal=0,
                 drift: int = 0,
                 steam_to_irl=0.7,
                 cases_to_sell=[],
                 delta: int = 7):
        Structure.__init__(self,
                           acc_num,
                           start_date,
                           start_bal)
        DropManager.__init__(self,
                             _rare_dates,
                             _release_dates,
                             start_date)
        self.price_data = price_data
        self.hour = 0
        # Ideal farm would run every 7 days. Real farm drifts a little
        # bit. drift lets you set by how many hours
        self.drift = drift
        # This coefficient lets you set how much cash you get for
        # 1 USD on steam
        self.steam_to_irl = steam_to_irl
        # Cases that are sold instantly(to enable you to stash others)
        self.insta_sell = cases_to_sell
        self.stash = []
        # Time between cycles of farming
        # Better left same as default value for simulation accuracy
        self.delta = delta

    def _price_for_date(self, price_data, date, hour=0):
        datetime = dt.datetime.combine(date, dt.time(hour, 0, 0))
        lower = dt.datetime.combine(date, dt.time(1, 0, 0))
        if datetime < lower:
            datetime = lower
        else:
            datetime = lower + dt.timedelta(days=1)

        dated_price_data = {}
        for case in price_data.keys():
            if case in self._active_pool or case in self._rare_pool:
                # Костиль
                try:
                    date_index = price_data[case]["Date"].index(
                        datetime)
                except ValueError:
                    date_index = price_data[case]["Date"].index(datetime
                                                                + dt.timedelta(hours=8, minutes=0))
                dated_price_data[case] = price_data[case]["Price(USD)"][date_index]

        return dated_price_data

    def run_once(self):
        # Get drops and update balance
        drops = []
        self._update_rare_dates(self.date)
        for i in range(self.acc_num):
            drops.append(self._drop_event())

        price_data = self._price_for_date(
            self.price_data, self.date, self.hour)
        for case in drops:
            if case in self.insta_sell or self.insta_sell == []:
                self.balance += price_data[case] * self.steam_to_irl
            elif self.insta_sell != [] and case not in self.insta_sell:
                self.stash.append(case)

        # Update date
        self.date += dt.timedelta(days=self.delta)
        if self.hour + self.drift > 23:
            self.date += dt.timedelta(days=1)
            self.hour = (self.hour+self.drift) % 24
        else:
            self.hour += self.drift

    def run_til_date(self, date):
        stats = {"Date": [],
                 "Balance": []
                 }
        while self.date <= date - dt.timedelta(days=self.delta):
            stats["Date"].append(self.date)
            self.run_once()
            stats["Balance"].append(self.balance)
        return stats

    def stash_value(self):
        stash_value = 0
        price_data = self._price_for_date(self.price_data, self.date)
        for case in self.stash:
            stash_value += price_data[case] * self.steam_to_irl
        return stash_value


def get_deep_stats(stats,
                   acc_pr=15,
                   acc_num=100,
                   drift=0):
    """
    Coefficients:
    acc_pr - account price in USD
    acc_num - amount of accounts(same as your farm)
    drift - Ideal farm would run every 7 days. Real farm drifts a little
            bit. drift lets you set by how many hours(same as your farm)
    """
    stats_new = stats.copy()

    stats_new["Profit"] = []
    last_balance = 0
    for i, balance in enumerate(stats_new["Balance"]):
        if i == 0:
            stats_new["Profit"].append(balance)
        else:
            stats_new["Profit"].append(balance - last_balance)
        last_balance = balance

    stats_new["Monthly profit"] = []
    for profit in stats_new["Profit"]:
        stats_new["Monthly profit"].append(profit*30 / (7+drift/24))

    stats_new["Time till moneyback"] = []
    for profit in stats_new["Monthly profit"]:
        stats_new["Time till moneyback"].append(
            acc_num*acc_pr/profit)

    stats_new["Balance normalized"] = []
    for value in stats_new["Balance"]:
        stats_new["Balance normalized"].append(value/acc_num)

    stats_new["Profit normalized"] = []
    for value in stats_new["Profit"]:
        stats_new["Profit normalized"].append(value/acc_num)

    stats_new["Monthly profit normalized"] = []
    for value in stats_new["Monthly profit"]:
        stats_new["Monthly profit normalized"].append(value/acc_num)

    return stats_new


def plot(stats, mode=0):
    """
    Modes:
    0 - balance
    1 - balance normalized
    2 - profit of each run
    3 - profit of each run normalized
    4 - average monthly profit
    5 - average monthly profit normalized
    6 - time till you make your money back(in months)
    """
    modes = ["Balance",
             "Balance normalized",
             "Profit",
             "Profit normalized",
             "Monthly profit",
             "Monthly profit normalized",
             "Time till moneyback"]
    if type(stats) == dict:
        x = stats["Date"]
        y = np.array(stats[modes[mode]])
    else:
        x = stats[0]["Date"]
        y = [stats[i][modes[mode]] for i in range(len(stats))]
        y = np.array(y)

    fig, ax = plt.subplots()
    ax.plot_date(x, y.T, marker='', linestyle='-')
    fig.autofmt_xdate()
    plt.show()


if __name__ == "__main__":
    price_data = get_price_data(False)
    farm1 = Farm(price_data,
                 acc_num=10000,
                 start_date=dt.date(2019, 10, 27),
                 start_bal=0,
                 drift=0,
                 steam_to_irl=0.6,
                 cases_to_sell=[],
                 delta=7)
    stats = farm1.run_til_date(dt.date(2022, 11, 8))
    stats = get_deep_stats(stats,
                           acc_pr=11.5,
                           acc_num=farm1.acc_num,
                           drift=farm1.drift)
    modes = [0, 1, 2, 3, 4, 5, 6]
    for mode in modes:
        plot(stats, mode)
    print(farm1.stash_value())
    stash = farm1.stash
