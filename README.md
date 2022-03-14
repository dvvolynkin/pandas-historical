---
# pandas_historical

[![codecov](https://codecov.io/gh/dvvolynkin/pandas-historical/branch/main/graph/badge.svg?token=pandas-historical_token_here)](https://codecov.io/gh/dvvolynkin/pandas-historical)
[![CI](https://github.com/dvvolynkin/pandas-historical/actions/workflows/main.yml/badge.svg)](https://github.com/dvvolynkin/pandas-historical/actions/workflows/main.yml)

Awesome pandas_historical created by dvvolynkin

## Install it from PyPI

```bash
pip install pandas_historical
```

## Usage

Let's take a table of historical values. For example currency rates.

Suppose we periodically scrap currency rates from a certain site,   
and then write the resulting value with the date of scraping to the table.
```python
import pandas as pd

currencies_scraping = pd.DataFrame([
    {
        'date': '2022-02-21',
        'key': 'DOLLAR',
        'value': 78,
        'scraping_id': 123
    },
    {
        'date': '2022-02-21',
        'key': 'EURO',
        'value': 87,
        'scraping_id': 124
    },
    {
        'date': '2022-02-22',
        'key': 'DOLLAR',
        'value': 78,
        'scraping_id': 124
    },
    {
        'date': '2022-02-28',
        'key': 'DOLLAR',
        'value': 105,
        'scraping_id': 124
    },
    {
        'date': '2022-03-07',
        'key': 'EURO',
        'value': 139,
        'scraping_id': 125
    },
    {
        'date': '2022-03-07',
        'key': 'EURO',
        'value': 148,
        'scraping_id': 125
    }
])
currencies_scraping
```
|    | date       | key    |   value |   scraping_id |
|---:|:-----------|:-------|--------:|--------------:|
|  0 | 2022-02-21 | DOLLAR |      78 |           123 |
|  1 | 2022-02-21 | EURO   |      87 |           123 |
|  2 | 2022-02-22 | DOLLAR |      78 |           124 |
|  3 | 2022-02-28 | DOLLAR |     105 |           124 |
|  4 | 2022-03-07 | EURO   |     139 |           125 |
|  5 | 2022-03-07 | EURO   |     148 |           125 |

Now let's turn this table into a table that stores only the dates when the values appeared or changed.

```python
from pandas_historical import make_value_change_events_df

value_change_events_df = make_value_change_events_df(currencies_scraping)
value_change_events_df

```
Take a look at. One of the rows is missing.

|    | date       | key    |   value |   scraping_id |
|---:|:-----------|:-------|--------:|--------------:|
|  0 | 2022-02-21 | DOLLAR |      78 |           123 |
|  1 | 2022-02-28 | DOLLAR |     105 |           124 |
|  2 | 2022-02-21 | EURO   |      87 |           123 |
|  3 | 2022-03-07 | EURO   |     139 |           125 |
|  4 | 2022-03-07 | EURO   |     148 |           125 |

Now let's add the new values we got from the last scraping.

```python
from pandas_historical import update_value_change_events_df

new_values = pd.DataFrame([
    {
        'date': '2022-03-10',
        'key': 'DOLLAR',
        'value': 105,
        'scraping_id': 127
    },
    {
        'date': '2022-03-11',
        'key': 'DOLLAR',
        'value': 113,
        'scraping_id': 127
    },
    {
        'date': '2022-03-11',
        'key': 'EURO',
        'value': 144,
        'scraping_id': 127
    }
])
value_change_events_df = update_value_change_events_df(
    value_change_events_df, new_values
)
value_change_events_df
```
You can see that of the two records with the dollar rate for 2022-02-28 and 2022-03-10, only 2022-02-28 remains  
because in the final dataframe remain only dates of changes and the first occurrence of values 

|    | date       | key    |   value |   scraping_id |
|---:|:-----------|:-------|--------:|--------------:|
|  0 | 2022-02-21 | DOLLAR |      78 |           123 |
|  1 | 2022-02-28 | DOLLAR |     105 |           124 |
|  2 | 2022-03-11 | DOLLAR |     113 |           127 |
|  3 | 2022-02-21 | EURO   |      87 |           123 |
|  4 | 2022-03-07 | EURO   |     139 |           125 |
|  5 | 2022-03-07 | EURO   |     148 |           125 |
|  6 | 2022-03-11 | EURO   |     144 |           127 |

```python
from pandas_historical import get_historical_state

get_historical_state(value_change_events_df)
```
|    | date                | key    |   value |   scraping_id |
|---:|:--------------------|:-------|--------:|--------------:|
|  2 | 2022-03-11 00:00:00 | DOLLAR |     113 |           127 |
|  6 | 2022-03-11 00:00:00 | EURO   |     144 |           127 |

```python
get_history_state(value_change_events_df, state_date='2022-03-07')
```
|    | date                | key    |   value |   scraping_id |
|---:|:--------------------|:-------|--------:|--------------:|
|  1 | 2022-02-28 00:00:00 | DOLLAR |     105 |           124 |
|  4 | 2022-03-07 00:00:00 | EURO   |     139 |           125 |

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
