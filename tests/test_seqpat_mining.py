""" Test Suite for Episode Mining algorithms """

import os

import pandas as pd

from spmf.seq_pat import PrefixSpan

test_file_path = os.path.join('tests', 'test_files', 'contextPrefixSpan.txt')


def create_mock_raw_dataframe() -> pd.DataFrame:
    """ Create raw mock dataframe """
    return pd.DataFrame({
        'ID': ['S1']*9 + ['S2']*7 + ['S3']*8 + ['S4']*7,
        'Time Points': [0, 1, 1, 1, 2, 2, 3, 4, 4, 5, 5, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 14, 15, 16, 16, 17, 18, 19],
        'Items': ['a', 'a', 'b', 'c', 'a', 'c', 'd', 'c', 'f', 'a', 'd', 'c', 'b', 'c', 'a', 'e', 'e', 'f', 'a', 'b', 'd', 'f', 'c', 'b', 'e', 'g', 'a', 'f', 'c', 'b', 'c'],
    })


def test_prefixspan_file() -> None:
    """ Test PrefixSpan on given example in
        https://www.philippe-fournier-viger.com/spmf/PrefixSpan.php
    """
    prefixspan = PrefixSpan(min_support=0.5)
    patterns, support = prefixspan.run_file(test_file_path)
    assert len(patterns) > 0 and len(support) > 0
    assert all(x in set(patterns) for x in {'2 3 -> 1', '6 -> 2', '6 -> 2 -> 3'})


def test_prefixspan_pandas() -> None:
    """ Test PrefixSpan on given example in
        https://www.philippe-fournier-viger.com/spmf/PrefixSpan.php
    """
    prefixspan = PrefixSpan(min_support=0.5)
    mock_df = create_mock_raw_dataframe()
    output = prefixspan.run_pandas(mock_df)
    assert len(output) > 0
    assert all(x in output['Frequent sequential pattern'].to_list() for x in {'b c -> a', 'f -> b', 'f -> b -> c'})
