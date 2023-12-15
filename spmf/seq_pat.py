""" Sequential Pattern Mining """

import re
from typing import List, Text, Tuple

import pandas as pd

from spmf.base import Spmf


class SeqPat(Spmf):
    """ Base class for Sequential Pattern Mining """

    def _transform_input_dataframe(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """ Transform input dataframe to the format required by SPMF

        :param input_df: Input Dataframe containing Sequences in 'Sequences' column
            NOTE: If Timestamp present, dataframe should contain it in 'Time points' column
        :return: Transformed dataframe
        """

        df = input_df.copy()

        df['Event_ID'] = (df.groupby('Items').ngroup()+1).astype(str)
        self.mapping = str.maketrans(df[['Items', 'Event_ID']].set_index('Event_ID', drop=True).to_dict()['Items'])

        return df.pipe(pd.DataFrame.groupby, by='Time Points') \
            .pipe(pd.core.groupby.generic.DataFrameGroupBy.agg, {'ID': 'first', 'Event_ID': (' ').join}) \
            .pipe(pd.DataFrame.reset_index) \
            .pipe(pd.DataFrame.groupby, by='ID') \
            .pipe(pd.core.groupby.generic.DataFrameGroupBy.agg, {'Event_ID': (' -1 ').join}) \
            .pipe(pd.DataFrame.reset_index) \
            .pipe(pd.DataFrame.rename, {'Event_ID': 'input'}, axis=1)

    def _parse_input_dataframe(self, input_df: pd.DataFrame) -> Text:
        """ Parse Input Dataframe to string format required for Sequential Pattern Mining

        :param input_df: Input Dataframe containing Sequence IDs in 'ID' column, time in
            'Time Points' column and items in 'Items' column.
            NOTE: Items in the same Itemset must have the same value in the 'Time Points' column
            NOTE: Items in the same sequence must have the same value in the 'ID' column
        :return: Parsed String representation
        """
        df = self._transform_input_dataframe(input_df)
        return (' -1 -2\n').join(df['input'].to_list()) + ' -1 -2'

    def _parse_output_file(self, **kwargs) -> Tuple[List[Text], List[int]]:
        """ Parse output txt file created by the Episode Mining algorithm

        :param kwargs: keyword arguments to read output file (delete)
        :return: Tuple of patterns and corresponding support
        """
        lines = self._read_file(**kwargs)
        patterns, supports = [], []

        for line in lines:
            line = line.strip().split('-1')
            patterns.append((' -> ').join([c.strip() for c in line[:-1]]))
            supports.append(re.search(r'(\d+)$', line[-1]).group(0))

        return patterns, list(map(int, supports))

    def _create_output_dataframe(self, patterns: List[Text], supports: List[int]) -> pd.DataFrame:
        """ Create Output Dataframe

        :param patterns: Frequent Episode Patterns return by the episode mining algorithm
        :param supports: Corresponding supports for each pattern
        :return: Dataframe containing patterns and corresponding support
        """
        patterns_mapped = [pattern.translate(self.mapping) for pattern in patterns]
        return pd.DataFrame((patterns_mapped, supports), index=['Frequent sequential pattern', 'Support']).T

    def run_pandas(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """ Run Episode Mining algorithm on Pandas Dataframe

        :param input_df: Input Dataframe containing Sequence IDs in 'ID' column, time in
            'Time Points' column and items in 'Items' column.
            NOTE: Items in the same Itemset must have the same value in the 'Time Points' column
            NOTE: Items in the same sequence must have the same value in the 'ID' column
        :return: Dataframe containing the frequent sequential patterns and support.
        """
        return super().run_pandas(input_df)

    def run_file(self, input_file_name: Text) -> Tuple[List[Text], List[int]]:
        """ Run Episode Mining algorithm on an input txt file

        :param input_file_name: Input txt file name
        :return: Tuple of frequent sequential patterns and corresponding support
        """
        return super().run_file(input_file_name)


class PrefixSpan(SeqPat):
    """ PrefixSpan Sequential Pattern Mining """

    def __init__(self, min_support: float, max_pattern_length: int = 0, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/PrefixSpan.php

        :param min_support: minimum occurence frequency
        :param max_pattern_length (optional): maximum number of items that patterns found should contain
        """
        super().__init__(**kwargs)
        self.min_support = min_support
        self.max_pattern_length = max_pattern_length

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'PrefixSpan',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'min_support': str(self.min_support)
        }

        if self.max_pattern_length > 0:
            arguments.update({'max_pattern_length': str(self.max_pattern_length)})

        return list(arguments.values())
