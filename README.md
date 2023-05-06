# Django Stock Tracker App
In this directory is an application for stock tracking in Django Framework. Users can create one portfolio and add stocks, transactions and dividends records. The user has to create an account to create a portfolio.
The app is connected to live financial API, which refreshes market data after user login. Because I have only a free plan of financial API, I set some limitations and plan.
There are limitations for companies in the portfolio and for API requests. User can subscribe from 3 plans, which is different by limits.

## Dashboard
The main page is the dashboard, where users can see widgets with the current value of the portfolio, total portfolio value, gain/loss and total number of companies in the portfolio. Under the widgets there are two charts. The first chart shows total portfolio value in time and the second shows portfolio holdings.
At the bottom of the page is a table with holdings with aggregated data of holdings. Here user can add a new company to his portfolio.

![Dashboard](https://github.com/skapis/appscreenshots/blob/main/Django%20-%20StockApp/Dashboard.png)

## Transactions
Another page is the transactions page. There is only a table with all transactions in the portfolio. Users can add a new transaction, edit a transaction or delete it. Users can also export all transactions to the Excel or CSV file.

![Transactions](https://github.com/skapis/appscreenshots/blob/main/Django%20-%20StockApp/Transactions.png)

## Dividends
On the dividends page is also widgets and charts. Users can see total expected dividends, received dividends and dividend yields. User can add new dividend record and also export dividend records to excel or csv file.

![Dividends](https://github.com/skapis/appscreenshots/blob/main/Django%20-%20StockApp/Dividends.png)

## Account
In the account section users can edit their profile, change password, change plan or generate an API key.

![Account](https://github.com/skapis/appscreenshots/blob/main/Django%20-%20StockApp/Account.png)

### API
Every user can use API which returns his dividends records or transactions.

![API](https://github.com/skapis/appscreenshots/blob/main/Django%20-%20StockApp/API%20-%20Documentation.png)
