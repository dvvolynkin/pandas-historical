from typing import Any, List, Optional

import pandas as pd


def make_historical_df(
    changes_history_df: pd.DataFrame,
    key_column: str = "key",
    date_column: str = "date",
    info_columns: Optional[List[str]] = None,
):
    df2 = changes_history_df.sort_values([key_column, date_column])
    df2 = df2.reset_index(drop=True)

    if not info_columns:
        _info_columns = []
    else:
        _info_columns = info_columns

    _info_columns_set = set(_info_columns) | {date_column, key_column}
    value_columns = changes_history_df.columns
    value_columns = list(
        filter(lambda x: x not in _info_columns_set, value_columns)
    )

    prev_not_equal = pd.Series([False] * len(df2))
    for column in value_columns:
        prev_not_equal = prev_not_equal | (df2[column] != df2[column].shift(1))

    return df2[prev_not_equal].reset_index(drop=True)


def update_historical_df(
    historical_df: pd.DataFrame, new_changes_df: pd.DataFrame
):
    return make_historical_df(pd.concat([historical_df, new_changes_df]))


def get_history_state(
    historical_df: pd.DataFrame,
    state_date: Any = None,
    key_column: str = "key",
    date_column: str = "date",
):
    if state_date:
        df2 = historical_df[historical_df[date_column] <= state_date]
    else:
        df2 = historical_df

    df2 = df2.sort_values(date_column)
    df2[date_column] = pd.to_datetime(df2[date_column])
    df2["__rank"] = (
        df2.groupby(key_column)[date_column]
        .rank(method="first", ascending=False)
        .astype(int)
    )
    df2 = df2[df2["__rank"] == 1]
    return df2[df2.columns[:-1]]
