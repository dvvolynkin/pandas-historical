from typing import Any, List, Optional

import pandas as pd


def make_value_change_events_df(
    history_df: pd.DataFrame,
    key_column: str = "key",
    date_column: str = "date",
    info_columns: Optional[List[str]] = None,
):
    sorted_history_df = history_df.sort_values([key_column, date_column])
    sorted_history_df = sorted_history_df.reset_index(drop=True)

    if not info_columns:
        info_columns = []

    info_columns_set = set(info_columns) | {date_column, key_column}
    value_columns = history_df.columns
    value_columns = list(
        filter(lambda x: x not in info_columns_set, value_columns)
    )

    prev_not_equal = pd.Series([False] * len(sorted_history_df))
    for column in value_columns:
        prev_not_equal = prev_not_equal | (sorted_history_df[column] != sorted_history_df[column].shift(1))

    return sorted_history_df[prev_not_equal].reset_index(drop=True)


def update_value_change_events_df(
    value_change_events_df: pd.DataFrame, new_history_df: pd.DataFrame
):
    return make_value_change_events_df(pd.concat([value_change_events_df, new_history_df]))


def get_historical_state(
    value_change_events_df: pd.DataFrame,
    state_date: Any = None,
    key_column: str = "key",
    date_column: str = "date",
):
    if state_date:
        _value_change_events_df = value_change_events_df[value_change_events_df[date_column] <= state_date]
    else:
        _value_change_events_df = value_change_events_df

    _value_change_events_df = _value_change_events_df.sort_values(date_column)
    _value_change_events_df[date_column] = pd.to_datetime(_value_change_events_df[date_column])
    _value_change_events_df["__rank"] = (
        _value_change_events_df.groupby(key_column)[date_column]
        .rank(method="first", ascending=False)
        .astype(int)
    )
    _value_change_events_df = _value_change_events_df[_value_change_events_df["__rank"] == 1]
    return _value_change_events_df[_value_change_events_df.columns[:-1]]
