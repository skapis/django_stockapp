# Django Stock Tracker App
In this directory is application for stock tracking in Django Framework. In app user can create one portfolio, add stocks, transactions and dividends records. User has to create account to create portfolio
App is connected to live financial API, which refresh market data after user login. Because I have only free plan of financial api, I set some limitations and plan in App.
There is limitations for companies in portfolio and for API requests. User can subscribe from 3 plans, which is different by limits.


## Dashboard
Main page is dashboard, where user can see widgets with current value of portfolio, total portfolio value, gain/loss and how many companies are in portfolio. Under the widgets are two charts. First chart shows total portfolio value in time and the second shows portfolio holdings.
At the bottom of the page is table with holdings with aggregated data of holdings. Here user can add new company to his portfolio

![Dashboard](https://github.com/skapis/appscreenshots/blob/main/Django%20-%20StockApp/Dashboard.png)

## Transactions
Another page is transactions page, where is only table with all transactions in portfolio. User can add new transaction, get detail, edit transaction or delete it. User can also export all transactions to the Excel or CSV file.

![Transactions](https://github.com/skapis/appscreenshots/blob/main/Django%20-%20StockApp/Transactions.png)

## Dividends
On the dividends page is also widgets and charts. User can see how much dividends will he receive, how much he received yet and dividend yields. User can add new dividend record and also export dividend records to excel or csv file.

![Dividends](https://github.com/skapis/appscreenshots/blob/main/Django%20-%20StockApp/Dividends.png)

## Account
In account section user can edit his profile, change password, change your plan or generate API key

![Account](https://github.com/skapis/appscreenshots/blob/main/Django%20-%20StockApp/Account.png)

### API
Every user, can use API, which returns his dividends records or transactions

![API](https://github.com/skapis/appscreenshots/blob/main/Django%20-%20StockApp/API%20-%20Documentation.png)
