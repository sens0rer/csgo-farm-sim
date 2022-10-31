import datetime as dt
import pricehistory
from time import sleep
import pandas as pd
import random
from progressbar import print_progress_bar


def get_price_data(is_new: bool = False):
    """
    Get Steam price history for each item.
    If is_new == True, gets data from Steam servers and writes them
    to files.
    If is_new == False, loads data from previously written files.
    """
    price_data = {}
    dateformat = "%Y-%m-%d %H:%M:%S"
    case_list = list(_drop_pool.keys())
    l = len(case_list)
    for i, case in enumerate(case_list):
        if is_new:
            df = pricehistory.get_df_for_item(case)
            sleep(15)
            price_data[case] = df.to_dict()
            pricehistory.write_df_to_file(df, case)
            print_progress_bar(i + 1, l,
                               prefix='Acquiring price data from Steam:\n',
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


# Constants
_min_date = dt.date(2020, 1, 1)
_max_date = dt.date(2030, 1, 1)
_release_dates = {'Recoil Case': dt.date(2022, 7, 1),
                  'Dreams & Nightmares Case': dt.date(2022, 1, 21)
                  }
_drop_pool = {'Recoil Case':  _max_date,
              'Snakebite Case':  _max_date,
              'Clutch Case':  _max_date,
              'Fracture Case':  _max_date,
              'Dreams & Nightmares Case':  _max_date,
              'Prisma 2 Case': dt.date(2022, 7, 1),
              'Danger Zone Case': dt.date(2022, 1, 18),
              'CS20 Case':   _min_date,
              'Prisma Case':   _min_date,
              'Horizon Case':   _min_date,
              'Spectrum 2 Case':   _min_date,
              'Operation Hydra Case':   _min_date,
              'Spectrum Case':   _min_date,
              'Glove Case':   _min_date,
              'Gamma Case':   _min_date,
              'Gamma 2 Case':   _min_date,
              'Chroma 3 Case':   _min_date,
              'Revolver Case':   _min_date,
              'Operation Wildfire Case':   _min_date,
              'Shadow Case':   _min_date,
              'Falchion Case':   _min_date,
              'Chroma Case':   _min_date,
              'Chroma 2 Case':   _min_date,
              'Operation Vanguard Weapon Case':   _min_date,
              'Operation Breakout Weapon Case':   _min_date,
              'Huntsman Weapon Case':   _min_date,
              'Winter Offensive Weapon Case':   _min_date,
              'Operation Bravo Case':   _min_date,
              'CS:GO Weapon Case 2':   _min_date,
              'CS:GO Weapon Case 3':   _min_date,
              'CS:GO Weapon Case':   _min_date,
              'Sticker Capsule': _min_date,
              'Sticker Capsule 2': _min_date,
              'Community Sticker Capsule 1': _min_date
              }
_newData = False
_price_data = get_price_data(_newData)


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
        if start_date < dt.date(2021, 5, 4):
            exception = f"""Only use dates after 04.05.2021, using earlier
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
        self._drop_pool = drop_pool
        self._release_dates = release_dates
        self._release_date_list = list(release_dates.values())
        self.date = date
        self._active_pool = []
        self._rare_pool = []
        for case in self._drop_pool.keys():
            removal_date = self._drop_pool.get(case)
            release_date = self._release_dates.get(case, _min_date)
            if date < removal_date and date >= release_date:
                self._active_pool.append(case)
                continue
            if date >= release_date:
                self._rare_pool.append(case)

    def _update_drop_pool(self, date):
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

        if run_update:
            self._active_pool = []
            self._rare_pool = []
            for case in self._drop_pool.keys():
                removal_date = self._drop_pool.get(case)
                release_date = self._release_dates.get(case, _min_date)
                if date < removal_date and date >= release_date:
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
                 acc_num=100,
                 start_date=dt.date(2021, 6, 9),
                 start_bal=0,
                 drift: int = 0,
                 ):
        Structure.__init__(self,
                           acc_num,
                           start_date,
                           start_bal)
        DropManager.__init__(self,
                             _drop_pool,
                             _release_dates,
                             start_date)
        self.hour = 0
        # Ideal farm would run every 7 days. Real farm drifts a little
        # bit. drift lets you set by how many hours
        self.drift = drift

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
                date_index = price_data[case]["Date"].index(datetime)
                dated_price_data[case] = price_data[case]["Price(USD)"][date_index]

        return dated_price_data

    def run_once(self):
        # Get drops and update balance
        drops = []
        self._update_drop_pool(self.date)
        for i in range(self.acc_num):
            drops.append(self._drop_event())

        price_data = self._price_for_date(
            _price_data, self.date, self.hour)
        for case in drops:
            self.balance += price_data[case]

        # Update date
        self.date += dt.timedelta(days=7)
        if self.hour + self.drift > 23:
            self.date += dt.timedelta(days=1)
            self.hour = (self.hour+self.drift) % 24
        else:
            self.hour += self.drift


if __name__ == "__main__":
    for i in range(10):
        farm1 = Farm()
        farm1.run_once()
        print(farm1.balance)
