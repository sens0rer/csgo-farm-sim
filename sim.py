import datetime as dt
import pricehistory
from time import sleep
import pandas as pd
import random

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


def get_price_data(is_new: bool):
    """
    Get Steam price history for each item.
    If is_new == True, gets data from Steam servers and writes them
    to files.
    If is_new == False, loads data from previously written files.
    """
    price_data = {}
    for case in list(_drop_pool.keys()):
        if is_new:
            df = pricehistory.get_df_for_item(case)
            sleep(15)
            price_data[case] = df.to_dict()
            pricehistory.write_df_to_file(df, case)
            continue

        price_data[case] = pricehistory.read_file_to_df(case).to_dict()
    return price_data


class DateError(Exception):
    """
    Used for inappropriate dates
    """


class FarmStructure():
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

    def _dropEvent(self):
        if random.random() < 0.01:
            return self._rare_pool[random.randint(0,
                                                  len(self._rare_pool) - 1)
                                   ]
        else:
            return self._active_pool[random.randint(0,
                                                    len(self._active_pool) - 1)
                                     ]


if __name__ == "__main__":
    x = DropManager(_drop_pool, _release_dates, dt.date(2022, 7, 1))
    x._update_drop_pool(x.date)
