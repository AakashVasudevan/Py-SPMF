""" Episode Mining """

import re
from typing import List, Text, Tuple

import pandas as pd

from spmf.base import Spmf


class Episode(Spmf):
    """ Base class for Episode Mining """

    def _parse_input_dataframe(self, input_df: pd.DataFrame) -> Text:
        """ Parse Input Dataframe to string format required for Episode Mining

        :param input_df: Input Dataframe containing Itemsets in 'Itemset' column
            NOTE: If Timestamp present, dataframe should contain it 'Time points' column
        :return: Parsed String representation
        """
        df = input_df.copy()

        if self.timestamp_present:
            df['input'] = df.apply(lambda x: '|'.join([x['Itemset'], str(x['Time points'])]), axis=1)

        else:
            df['input'] = df['Itemset']

        return ('\n').join(df['input'].to_list())

    def _parse_output_file(self, **kwargs) -> Tuple[List[Text], List[int]]:
        """ Parse output txt file created by the Episode Mining algorithm

        :param kwargs: keyword arguments to read output file (delete)
        :return: Tuple of patterns and corresponding support
        """
        lines = self._read_output_file(**kwargs)
        patterns, supports = [], []

        for line in lines:
            line = line.strip().split('-1')
            patterns.append((' -> ').join([c.strip() for c in line[:-1]]))
            supports.append(re.search(r'(\d+)$', line[-1]).group(0))

        return patterns, list(map(int, supports))

    def _create_output_dataframe(self, patterns: List[Text], supports: List[int]) -> pd.DataFrame:
        """ Create Output Dataframe

        :return: Dataframe containing patterns and corresponding support
        """
        return pd.DataFrame((patterns, supports), index=['Frequent episode', 'Support']).T

    def run_pandas(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """ Run Episode Mining algorithm on Pandas Dataframe

        :param input_df: Input Dataframe containing Itemsets in 'Itemset' column
            NOTE: If Timestamp present, dataframe should contain it 'Time points' column
        :return: Dataframe containing the frequent episodes and support.
        """
        return super().run_pandas(input_df)

    def run_file(self, input_file_name: Text) -> Tuple[List[Text], List[int]]:
        """ Run Episode Mining algorithm on an input txt file

        :param input_file_name: Input txt file name
        :return: Tuple of frequent episode patterns and corresponding support
        """
        return super().run_file(input_file_name)


class EpisodeRules(Episode):
    """ Base class for Episode Rule Mining """

    def _parse_output_file(self, **kwargs) -> Tuple[List[Text], List[int], List[float]]:
        """ Parse output txt file created by the Episode Rule Mining algorithm

        :param kwargs: keyword arguments to read output file (delete)
        :return: Tuple of patterns and corresponding support and confidence
        """
        lines = self._read_output_file(**kwargs)
        patterns, supports, confidence = [], [], []
        for line in lines:
            line = line.strip().split('#')
            patterns.append(line[0].strip())
            supports.append(re.search(r'(\d+)$', line[1].strip()).group(0))
            confidence.append(re.search(r'([\d.]+)$', line[2].strip()).group(0))

        return patterns, list(map(int, supports)), list(map(float, confidence))

    def _create_output_dataframe(self, patterns: List[Text], supports: List[int], confidence: List[float]) -> pd.DataFrame:
        """ Create Output Dataframe

        :return: Dataframe containing patterns and corresponding support and confidence
        """
        return pd.DataFrame((patterns, supports, confidence), index=['Frequent episode', 'Support', 'Confidence']).T

    def run_pandas(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """ Run Episode Mining algorithm on Pandas Dataframe

        :param input_df: Input Dataframe containing Itemsets in 'Itemset' column
            NOTE: If Timestamp present, dataframe should contain it 'Time points' column
        :return: Dataframe containing the frequent episodes and support.
        """
        return super().run_pandas(input_df)

    def run_file(self, input_file_name: Text) -> Tuple[List[Text], List[int], List[float]]:
        """ Run Episode Mining algorithm on an input txt file

        :param input_file_name: Input txt file name
        :return: Tuple of frequent episode patterns and corresponding support and confidence
        """
        return super().run_file(input_file_name)


class TKE(Episode):
    """ Top K Frequent Episode Mining """

    def __init__(self, k: int, max_window: int, timestamp_present: bool = False, **kwargs) -> None:
        """ Initialize Object

        :param k:
        :param max_window:
        :param timestamp_present:
        :param kwargs: Keyword arguments to base SPMF. E.g., memory
        """
        super().__init__(**kwargs)

        self.k = k
        self.max_window = max_window
        self.timestamp_present = timestamp_present

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'TKE',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'K': str(self.k),
            'max_window': str(self.max_window),
            'Timestamp': str(not self.timestamp_present)
        }

        return list(arguments.values())


class TKERules(EpisodeRules):
    """ Episode Rule Mining using TKE """

    def __init__(self, k: int, max_window: int, timestamp_present: bool = False, min_confidence: float = 0.5, max_consequent_count: int = 1, min_support: int = 2, **kwargs) -> None:
        """ Initialize Object

        :param k:
        :param max_window:
        :param timestamp_present:
        :param min_confidence:
        :param max_consequent_count:
        :param min_support:
        :param kwargs:
        """
        super().__init__(**kwargs)

        self.k = k
        self.max_window = max_window
        self.timestamp_present = timestamp_present
        self.min_confidence = min_confidence
        self.max_consequent_count = max_consequent_count
        self.min_support = min_support

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'TKE-Rules',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'K': str(self.k),
            'max_window': str(self.max_window),
            'Timestamp': str(not self.timestamp_present),
            'min_confidence': str(self.min_confidence),
            'max_consequent_event': str(self.max_consequent_count),
            'min_support': str(self.min_support)
        }

        return list(arguments.values())


class EMMA(Episode):
    """ Frequent Episode Mining using EMMA """

    def __init__(self, min_support: int, max_window: int, timestamp_present: bool = False, **kwargs) -> None:
        """ Initialize Object

        :param min_support:
        :param max_window:
        :param timestamp_present:
        :param kwargs: Keyword arguments to base SPMF. E.g., memory
        """
        super().__init__(**kwargs)

        self.min_support = min_support
        self.max_window = max_window
        self.timestamp_present = timestamp_present

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'EMMA',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'min_support': str(self.min_support),
            'max_window': str(self.max_window),
            'Timestamp': str(not self.timestamp_present)
        }

        return list(arguments.values())


class EMMARules(EpisodeRules):
    """ Frequent Episode Mining using EMMA """

    def __init__(self, min_support: int, max_window: int, timestamp_present: bool = False, min_confidence: float = 0.5, max_consequent_count: int = 1, **kwargs) -> None:
        """ Initialize Object

        :param min_support:
        :param max_window:
        :param timestamp_present:
        :param kwargs: Keyword arguments to base SPMF. E.g., memory
        """
        super().__init__(**kwargs)

        self.min_support = min_support
        self.max_window = max_window
        self.timestamp_present = timestamp_present
        self.min_confidence = min_confidence
        self.max_consequent_count = max_consequent_count

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'EMMA-Rules',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'min_support': str(self.min_support),
            'max_window': str(self.max_window),
            'Timestamp': str(not self.timestamp_present),
            'min_confidence': str(self.min_confidence),
            'max_consequent_event': str(self.max_consequent_count),
        }

        return list(arguments.values())


class AFEM(Episode):
    """ Frequent Episode Mining using EMMA """

    def __init__(self, min_support: int, max_window: int, timestamp_present: bool = False, **kwargs) -> None:
        """ Initialize Object

        :param min_support:
        :param max_window:
        :param timestamp_present:
        :param kwargs: Keyword arguments to base SPMF. E.g., memory
        """
        super().__init__(**kwargs)

        self.min_support = min_support
        self.max_window = max_window
        self.timestamp_present = timestamp_present

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'AFEM',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'Min_Support': str(self.min_support),
            'max_window': str(self.max_window),
            'Timestamp': str(not self.timestamp_present)
        }

        return list(arguments.values())
