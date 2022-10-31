import datetime as dt
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
import pricehistory
import time

release_dates = {'Recoil%20Case': dt.date(2022, 7, 1),
                 'Dreams%20%26%20Nightmares%20Case': dt.date(2022, 1, 21)
                 }

drop_pool = {'Recoil%20Case': dt.date(2030, 1, 1),
             'Snakebite%20Case': dt.date(2030, 1, 1),
             'Clutch%20Case': dt.date(2030, 1, 1),
             'Fracture%20Case': dt.date(2030, 1, 1),
             'Dreams%20%26%20Nightmares%20Case': dt.date(2030, 1, 1),
             'Prisma%202%20Case': dt.date(2022, 7, 1),
             'Danger%20Zone%20Case': dt.date(2022, 1, 18),
             'CS20%20Case': dt.date(2020, 1, 1),
             'Prisma%20Case': dt.date(2020, 1, 1),
             'Horizon%20Case': dt.date(2020, 1, 1),
             'Spectrum%202%20Case': dt.date(2020, 1, 1),
             'Operation%20Hydra%20Case': dt.date(2020, 1, 1),
             'Spectrum%20Case': dt.date(2020, 1, 1),
             'Glove%20Case': dt.date(2020, 1, 1),
             'Gamma%20Case': dt.date(2020, 1, 1),
             'Gamma%202%20Case': dt.date(2020, 1, 1),
             'Chroma%203%20Case': dt.date(2020, 1, 1),
             'Revolver%20Case': dt.date(2020, 1, 1),
             'Operation%20Wildfire%20Case': dt.date(2020, 1, 1),
             'Shadow%20Case': dt.date(2020, 1, 1),
             'Falchion%20Case': dt.date(2020, 1, 1),
             'Chroma%20Case': dt.date(2020, 1, 1),
             'Chroma%202%20Case': dt.date(2020, 1, 1),
             'Operation%20Vanguard%20Weapon%20Case': dt.date(2020, 1, 1),
             'Operation%20Breakout%20Weapon%20Case': dt.date(2020, 1, 1),
             'Huntsman%20Weapon%20Case': dt.date(2020, 1, 1),
             'Winter%20Offensive%20Weapon%20Case': dt.date(2020, 1, 1),
             'Operation%20Bravo%20Case': dt.date(2020, 1, 1),
             'CS:GO%20Weapon%20Case%202': dt.date(2020, 1, 1),
             'CS:GO%20Weapon%20Case%203': dt.date(2020, 1, 1),
             'CS:GO%20Weapon%20Case': dt.date(2020, 1, 1)
             }

price_data = {}
get_new_data = False
for case in list(drop_pool.keys()):
    if get_new_data:
        df = pricehistory.get_df_for_item(case)
        time.sleep(15)
        price_data[case] = df.to_dict()
        pricehistory.write_df_to_file(df, case)
    else:
        price_data[case] = pricehistory.read_file_to_df(case).to_dict()


class CSFarm():
    def __init__(self, accountNum=100, startDate=dt.datetime(2021, 6, 9, hour=0, minute=0, second=0), startBal=0):
        self.N = accountNum
        self.date = startDate
        self.balance = startBal
        self.release_dates = list(release_dates.values())
        self.Active = [x for x in drop_pool.keys() if self.date.date() < drop_pool.get(
            x) and self.date.date() > release_dates.get(x, dt.date(2020, 1, 1))]
        self.Rare = [x for x in drop_pool.keys() if self.date.date(
        ) > drop_pool.get(x) and release_dates.get(x) is None]

    def _dropEvent(self, date):
        if random.random() < 0.01:
            # return self.Rare[random.randint(0, len(self.Rare)-1)]
            pass
        else:
            return self.Active[random.randint(0, len(self.Active)-1)]

    def runOnce(self):
        dropList = []
        # if self.release_dates != []:
        #     if self.date.date() in [min(self.release_dates) - dt.timedelta(days=x) for x in range(-25,25)]:
        #         # print(self.date)
        #         self.Active = [x for x in drop_pool.keys() if self.date.date() < drop_pool.get(x) and self.date.date() > release_dates.get(x, dt.date(2020,1,1))]
        #         self.Rare = [x for x in drop_pool.keys() if self.date.date() > drop_pool.get(x) and release_dates.get(x) is None]
        #     if self.date.date() > min(self.release_dates):
        #         self.release_dates.remove(min(self.release_dates))

        for i in range(self.N):
            dropList.append(self._dropEvent(self.date))
        date = str(self.date)[0:-9]
        # TO-DO: Оптимізувати, щоб воно не по всіх датах шукало
        for case in dropList:
            if case is None:
                continue
            data = list(price_data[case]['Date'].values())
            for d in data:
                if str(d[0:-9]) == date:
                    index = data.index(d)
                    break
            price = float(list(price_data[case]['Price(USD)'].values())[
                          index].replace(",", '.'))
            self.balance += price
        self.date += dt.timedelta(7.25)

    def runTilDate(self, date):
        stats = []
        while self.date < date:
            self.runOnce()
            stats.append((self.balance, self.date - dt.timedelta(7.25)))
        return stats


class CSFarmYielder():
    def __init__(self, accountNum=100, startDate=dt.datetime(2021, 6, 9, hour=0, minute=0, second=0), startBal=0, farmAmount=100):
        self.N = accountNum
        self.date = startDate
        self.balance = startBal
        self.accountN = farmAmount

    def runTilDate(self, date):
        while True:
            self.account = CSFarm(self.N, self.date, self.balance)
            balances, dates = zip(*self.account.runTilDate(date))
            yield balances, dates


farm = CSFarmYielder(10000, startDate=dt.datetime(
    2022, 7, 2, hour=0, minute=0, second=0))
# x._dropEvent(x.date)
data = next(farm.runTilDate(dt.datetime(
    2022, 10, 29, hour=0, minute=0, second=0)))
balances, dates = data
datesRigid = np.array(dates)
balDifRigid = []
for i in range(1):
    data = next(farm.runTilDate(dt.datetime(
        2022, 10, 29, hour=0, minute=0, second=0)))
    balances, dates = data
    balancesNormalized = [n/farm.N for n in balances]
    balDif = [0]
    for i in range(len(balances)-1):
        balDif.append(
            470/37*10000/((balances[i+1]-balances[i])*0.6/7.25*30))
    balDifRigid.append(balDif)
balDifRigid = np.array(balDifRigid)

fig, ax = plt.subplots()
ax.plot_date(datesRigid, balDifRigid.T, marker='', linestyle='-')

fig.autofmt_xdate()
plt.show()
