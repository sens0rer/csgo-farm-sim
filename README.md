# The project is abandoned due to changes to how CS cases are dropped
# CS:GO Case Farm Simulator
This package allows you to simulate a CS:GO Case Farm.

## **What's a CS:GO Case Farm?**
Counter-Strike: Global Offensive has sellable items, and one example of those are cases. There is a system that drops cases to players once a week. Those cases can then be sold for a profit. You can have multiple accounts and use them to farm cases.

## **What is the functionality of this package?**
The package lets you create a simulation with given parameters such as amount of accounts, starting date, cases you want to hold/sell and so on. Then it lets you simulate case drops and gets you relevant stats using Steam price history. There is also a simple plotter included.

## **Installation**
Clone the repository and install everything from `requirements.txt` and you're good to go.

## **Usage**
Start by importing `sim.py`.

    import sim

First you need to get price history for the cases from Steam. 

#### `get_price_data(is_new)`
Loads price history for cases.
 - `is_new` is set to **True** by default. This will get new price history from Steam and save it to your directory;
 - when `is_new` is set to **False**, this will load existing price history from your directory.
     
 ```
 import sim
 price_data = sim.get_price_data(False) # loads existing price history from the directory
price_data = sim.get_price_data(True) # gets new price history from steam and saves it to your directory
price_data = sim.get_price_data() # same as the line above
```

After that you want to initialize your farm
#### `Farm()`
###### `Farm (price_data, acc_num, start_date, start_bal, drift, steam_to_irl, cases_to_sell, delta)`
- `price_data` is the price history dictionary you get by running `get_price_data()`
- `acc_num` is the amount of accounts. Defaults to **100**
- `start_date` is the starting date of your farm.  **Has to be a datetime.date object**. Defaults to **June, 9 2021**. Using dates before October, 27, 2019 raises an error because simulation is inaccurate before this date.
- `start_bal`is the starting balance in USD. Defaults to **0**.
- `drift` is used to account for the fact that while it is possible to run the farm exactly every 7 days, there is usually some offset. Measured in hours. Defaults to **0**.
- `steam_to_irl` is the conversion rate between Steam USD balance and cash value. Defaults to **0.7**.
- `cases_to_sell` is a list of cases that are sold, all the other cases will be stashed. When passing an empty list or left as a default value, defaults to selling every case when it's dropped.
- `delta` determines the length of the drop cycle. Normally, every account can receive a drop every 7 days. But you might want to change that if you want to get data with higher resolution, for example. Defaults to **7**.
