import datetime

import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)


def load_dataset():
    df = pd.read_csv("./archive/data.csv")
    # cleaning dataframe
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df = df.dropna(subset=['CustomerID'], how='all')
    df = df[df['Quantity'] > 0]
    # fe
    df['TotalSum'] = df['Quantity'] * df['UnitPrice']
    d = {'TotalSum': 'sum', 'Quantity': 'sum', 'CustomerID': 'first',
         'InvoiceDate': 'first'}
    invoices = df.groupby("InvoiceNo", as_index=False).agg(d)
    return invoices


def get_time_since_last_purchase(df: pd.DataFrame, customer_id: int,
                                 query_date: datetime.datetime) -> int:
    customer_filtered = df[df["CustomerID"] == customer_id]
    last_date = \
    customer_filtered[customer_filtered["InvoiceDate"] < query_date][
        "InvoiceDate"].max()

    delta = query_date - last_date
    return delta.days


def get_average_time_between_purchases(df: pd.DataFrame, customer_id: int,
                                       query_date: datetime.datetime,
                                       days: int):
    customer_filtered = df[df["CustomerID"] == customer_id]
    start_date = query_date - datetime.timedelta(days=days)
    last_invoices = customer_filtered[customer_filtered["InvoiceDate"] >
                                      start_date]
    last_invoices["days_between"] =last_invoices["InvoiceDate"].diff().dt.days
    return last_invoices["days_between"].mean()


def get_features(customer_id: int, query_date: str):
    invoices = load_dataset()
    """
    Time between "query date" and previous purchase
    Average time between purchases in the last 6 months or something
    """
    query_date = datetime.datetime.strptime(query_date, '%Y-%m-%d')
    days_since_last_purchase = get_time_since_last_purchase(
        df=invoices,
        customer_id=customer_id,
        query_date=query_date,
    )

    average_time_between_purchases = get_average_time_between_purchases(
        df=invoices,
        customer_id=customer_id,
        query_date=query_date,
        days=30*6
    )
    return {
        "days_since_last_purchase": days_since_last_purchase,
        "average_time_between_purchases": average_time_between_purchases
    }


if __name__ == '__main__':
    print(get_features(customer_id=17850, query_date="2021-05-12"))
