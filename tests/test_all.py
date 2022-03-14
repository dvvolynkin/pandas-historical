import pandas as pd
import pytest
from pandas import Timestamp

from pandas_historical import (
    make_value_change_events_df,
    update_value_change_events_df,
    get_historical_state,
)


def test_parameterized():
    currencies_scraping = pd.DataFrame(
        [
            {
                "date": "2022-02-21",
                "key": "DOLLAR",
                "value": 78,
                "scraping_id": 123,
            },
            {
                "date": "2022-02-21",
                "key": "EURO",
                "value": 87,
                "scraping_id": 123,
            },
            {
                "date": "2022-02-28",
                "key": "DOLLAR",
                "value": 105,
                "scraping_id": 124,
            },
            {
                "date": "2022-03-07",
                "key": "EURO",
                "value": 139,
                "scraping_id": 125,
            },
            {
                "date": "2022-03-07",
                "key": "EURO",
                "value": 148,
                "scraping_id": 125,
            },
        ]
    )
    historical_df = make_value_change_events_df(currencies_scraping)
    assert historical_df.to_dict() == {
        "date": {
            0: "2022-02-21",
            1: "2022-02-28",
            2: "2022-02-21",
            3: "2022-03-07",
            4: "2022-03-07",
        },
        "key": {0: "DOLLAR", 1: "DOLLAR", 2: "EURO", 3: "EURO", 4: "EURO"},
        "value": {0: 78, 1: 105, 2: 87, 3: 139, 4: 148},
        "scraping_id": {0: 123, 1: 124, 2: 123, 3: 125, 4: 125},
    }

    new_values = pd.DataFrame(
        [
            {
                "date": "2022-03-11",
                "key": "DOLLAR",
                "value": 113,
                "scraping_id": 127,
            },
            {
                "date": "2022-03-11",
                "key": "EURO",
                "value": 144,
                "scraping_id": 127,
            },
        ]
    )

    historical_df = update_value_change_events_df(historical_df, new_values)

    assert historical_df.to_dict() == {
        "date": {
            0: "2022-02-21",
            1: "2022-02-28",
            2: "2022-03-11",
            3: "2022-02-21",
            4: "2022-03-07",
            5: "2022-03-07",
            6: "2022-03-11",
        },
        "key": {
            0: "DOLLAR",
            1: "DOLLAR",
            2: "DOLLAR",
            3: "EURO",
            4: "EURO",
            5: "EURO",
            6: "EURO",
        },
        "value": {0: 78, 1: 105, 2: 113, 3: 87, 4: 139, 5: 148, 6: 144},
        "scraping_id": {
            0: 123,
            1: 124,
            2: 127,
            3: 123,
            4: 125,
            5: 125,
            6: 127,
        },
    }

    assert get_historical_state(
        historical_df, state_date="2022-03-10"
    ).to_dict() == {
        "date": {
            1: Timestamp("2022-02-28 00:00:00"),
            4: Timestamp("2022-03-07 00:00:00"),
        },
        "key": {1: "DOLLAR", 4: "EURO"},
        "value": {1: 105, 4: 139},
        "scraping_id": {1: 124, 4: 125},
    }

    assert get_historical_state(historical_df).to_dict() == {
        "date": {
            2: Timestamp("2022-03-11 00:00:00"),
            6: Timestamp("2022-03-11 00:00:00"),
        },
        "key": {2: "DOLLAR", 6: "EURO"},
        "value": {2: 113, 6: 144},
        "scraping_id": {2: 127, 6: 127},
    }
