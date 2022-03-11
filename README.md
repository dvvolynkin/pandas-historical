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
        'scraping_id': 123
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
|  2 | 2022-02-28 | DOLLAR |     105 |           124 |
|  3 | 2022-03-07 | EURO   |     139 |           125 |
|  4 | 2022-03-07 | EURO   |     148 |           125 |

```python
from pandas_historical import make_historical_df

historical_df = make_historical_df(currencies_scraping)
historical_df
```
|    | date       | key    |   value |   scraping_id |
|---:|:-----------|:-------|--------:|--------------:|
|  0 | 2022-02-21 | DOLLAR |      78 |           123 |
|  1 | 2022-02-28 | DOLLAR |     105 |           124 |
|  2 | 2022-02-21 | EURO   |      87 |           123 |
|  3 | 2022-03-07 | EURO   |     139 |           125 |
|  4 | 2022-03-07 | EURO   |     148 |           125 |

```python
from pandas_historical import update_historical_df
new_values = pd.DataFrame([
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
historical_df = update_historical_df(
    historical_df, new_values
)
historical_df
```
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
from pandas_historical import get_history_state
get_history_state(historical_df)
```
|    | date                | key    |   value |   scraping_id |
|---:|:--------------------|:-------|--------:|--------------:|
|  2 | 2022-03-11 00:00:00 | DOLLAR |     113 |           127 |
|  6 | 2022-03-11 00:00:00 | EURO   |     144 |           127 |

```python
get_history_state(historical_df, state_date='2022-03-07')
```
|    | date                | key    |   value |   scraping_id |
|---:|:--------------------|:-------|--------:|--------------:|
|  1 | 2022-02-28 00:00:00 | DOLLAR |     105 |           124 |
|  4 | 2022-03-07 00:00:00 | EURO   |     139 |           125 |

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
