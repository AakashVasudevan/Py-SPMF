""" Test Suite for Episode Mining algorithms """

import os
from typing import Text

import pandas as pd

from spmf.episode import AFEM, EMMA, TKE, EMMARules, TKERules

test_file_path = os.path.join('tests', 'test_files', 'contextEMMA.txt')


def create_mock_dataframe(file_path: Text) -> pd.DataFrame:
    """ Create mock dataframe from file """
    with open(file_path, 'r') as fp:
        lines = [(line.strip().split('|')) for line in fp]

    return pd.DataFrame(lines, columns=['Itemset', 'Time points'])


def test_tke_example_file() -> None:
    """ Test TKE on given example in
        https://www.philippe-fournier-viger.com/spmf/TKEepisodes.php
    """
    tke = TKE(k=6, max_window=2, timestamp_present=True)
    patterns, support = tke.run_file(test_file_path)
    assert len(patterns) > 0 and len(support) > 0
    assert set(patterns) == {'1', '2', '1 2', '1 -> 1', '1 -> 2', '1 -> 1 2'}
    assert set(support) == {5, 3, 2, 3, 2, 2}


def test_tke_example_pandas() -> None:
    """ Test TKE on given example in
        https://www.philippe-fournier-viger.com/spmf/TKEepisodes.php
    """
    tke = TKE(k=6, max_window=2, timestamp_present=True)
    mock_df = create_mock_dataframe(test_file_path)
    output = tke.run_pandas(mock_df)
    assert len(output) > 0
    assert set(output['Frequent episode'].to_list()) == {'1', '2', '1 2', '1 -> 1', '1 -> 2', '1 -> 1 2'}
    assert set(output['Support'].to_list()) == {5, 3, 2, 3, 2, 2}


def test_tke_rules_example_file() -> None:
    """ Test TKE Rules on given example in
        https://www.philippe-fournier-viger.com/spmf/standard_episode_rules.php
    """
    tke_rules = TKERules(k=6, max_window=2, timestamp_present=True,
                         min_confidence=0.2, max_consequent_count=1, min_support=2)
    patterns, support, confidence = tke_rules.run_file(test_file_path)
    assert len(patterns) > 0 and len(support) > 0 and len(confidence) > 0
    assert set(patterns) == {f'{{1}} ==> {{2}}', f'{{1}} ==> {{1,2}}', f'{{1}} ==> {{1}}'}
    assert set(support) == {2, 2, 3}
    assert set(confidence) == {0.4, 0.6, 0.4}


def test_tke_rules_example_pandas() -> None:
    """ Test TKE Rules on given example in
        https://www.philippe-fournier-viger.com/spmf/standard_episode_rules.php
    """
    tke_rules = TKERules(k=6, max_window=2, timestamp_present=True,
                         min_confidence=0.2, max_consequent_count=1, min_support=2)
    mock_df = create_mock_dataframe(test_file_path)
    output = tke_rules.run_pandas(mock_df)
    assert len(output) > 0
    assert set(output['Frequent episode'].to_list()) == {f'{{1}} ==> {{2}}', f'{{1}} ==> {{1,2}}', f'{{1}} ==> {{1}}'}
    assert set(output['Support'].to_list()) == {2, 2, 3}
    assert set(output['Confidence'].to_list()) == {0.4, 0.6, 0.4}


def test_emma_example_file() -> None:
    """ Test EMMA on given example in
        https://www.philippe-fournier-viger.com/spmf/EMMA.php
    """
    emma = EMMA(min_support=2, max_window=2, timestamp_present=True)
    patterns, support = emma.run_file(test_file_path)
    assert len(patterns) > 0 and len(support) > 0
    assert set(patterns) == {'1', '2', '1 2', '1 -> 1', '1 -> 2', '1 -> 1 2'}
    assert set(support) == {5, 3, 2, 3, 2, 2}


def test_emma_example_pandas() -> None:
    """ Test EMMA on given example in
        https://www.philippe-fournier-viger.com/spmf/EMMA.php
    """
    emma = EMMA(min_support=2, max_window=2, timestamp_present=True)
    mock_df = create_mock_dataframe(test_file_path)
    output = emma.run_pandas(mock_df)
    assert len(output) > 0
    assert set(output['Frequent episode'].to_list()) == {'1', '2', '1 2', '1 -> 1', '1 -> 2', '1 -> 1 2'}
    assert set(output['Support'].to_list()) == {5, 3, 2, 3, 2, 2}


def test_emma_rules_example_file() -> None:
    """ Test EMMA Rules on given example in
        https://www.philippe-fournier-viger.com/spmf/standard_episode_rules.php
    """
    emma_rules = EMMARules(max_window=2, timestamp_present=True, min_confidence=0.2,
                           max_consequent_count=1, min_support=2)
    patterns, support, confidence = emma_rules.run_file(test_file_path)
    assert len(patterns) > 0 and len(support) > 0 and len(confidence) > 0
    assert set(patterns) == {f'{{1}} ==> {{2}}', f'{{1}} ==> {{1,2}}', f'{{1}} ==> {{1}}'}
    assert set(support) == {2, 2, 3}
    assert set(confidence) == {0.4, 0.6, 0.4}


def test_emma_rules_example_pandas() -> None:
    """ Test EMMA Rules on given example in
        https://www.philippe-fournier-viger.com/spmf/standard_episode_rules.php
    """
    emma_rules = EMMARules(max_window=2, timestamp_present=True, min_confidence=0.2,
                           max_consequent_count=1, min_support=2)
    mock_df = create_mock_dataframe(test_file_path)
    output = emma_rules.run_pandas(mock_df)
    assert len(output) > 0
    assert set(output['Frequent episode'].to_list()) == {f'{{1}} ==> {{2}}', f'{{1}} ==> {{1,2}}', f'{{1}} ==> {{1}}'}
    assert set(output['Support'].to_list()) == {2, 2, 3}
    assert set(output['Confidence'].to_list()) == {0.4, 0.6, 0.4}


def test_afem_example_file() -> None:
    """ Test AFEM on given example in
        https://www.philippe-fournier-viger.com/spmf/AFEM_temporal.php
    """
    afem = AFEM(min_support=2, max_window=2, timestamp_present=True)
    patterns, support = afem.run_file(test_file_path)
    assert len(patterns) > 0 and len(support) > 0
    assert set(patterns) == {'1', '2', '1 2', '1 -> 1', '1 -> 2', '1 -> 1 2'}
    assert set(support) == {5, 3, 2, 3, 2, 2}


def test_afem_example_pandas() -> None:
    """ Test AFEM on given example in
        https://www.philippe-fournier-viger.com/spmf/AFEM_temporal.php
    """
    afem = AFEM(min_support=2, max_window=2, timestamp_present=True)
    mock_df = create_mock_dataframe(test_file_path)
    output = afem.run_pandas(mock_df)
    assert len(output) > 0
    assert set(output['Frequent episode'].to_list()) == {'1', '2', '1 2', '1 -> 1', '1 -> 2', '1 -> 1 2'}
    assert set(output['Support'].to_list()) == {5, 3, 2, 3, 2, 2}
