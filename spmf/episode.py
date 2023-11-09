""" Episode Mining """

from typing import Any, List, Text, Tuple

import pandas as pd
import subprocess
import re

from spmf.base import Spmf

class TKE(Spmf):
    """ Top K Frequent Episode Mining """
    def __init__(self, k :int, max_window: int, timestamp_present: bool = False, **kwargs) -> None:
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
            'Subprocess' : 'java',
            'Memory' : f'-Xmx{self.memory}m',
            'Binary_Format' : '-jar',
            'Binary_File' : self.executable_path,
            'Command' : 'run',
            'Algorithm' : 'TKE',
            'Input' : input_file_name,
            'Output' : self.output_file_name,
            'K' : str(self.k),
            'max_window' : str(self.max_window),
            'Timestamp' : str(not self.timestamp_present)
        }

        return list(arguments.values())

    def _parse_input_dataframe(self, input_df: pd.DataFrame) -> Text:
        """ Parse Input Dataframe to string format required by SPMF 

        :param input_df: Input Dataframe containing Itemsets in 'Itemset' column
            NOTE: If present, Timestamp column must be set as index
        :return: Parsed String representation in the format required by SPMF
        """
        df = input_df.copy()

        if self.timestamp_present:
            df['input'] = df.apply(lambda x: '|'.join([x['Itemset'], str(x.name)]), axis=1)

        else:
            df['input'] = df['Itemset']
        
        return df['input'].to_string(header=False, index=False)
    
    def _parse_output_file(self, **kwargs) -> Tuple[List[Text], List[int]]:
        """ Parse output txt file created by the TKE algorithm

        :param kwargs: keyword arguments to read output file (delete)
        :return: Tuple of patterns and corresponding support
        """
        lines = self._read_output_file(**kwargs)
        patterns, supports = [], []

        for line in lines:
            line = line.strip().split("-1")
            patterns.append((' -> ').join([c.strip() for c in line[:-1]]))
            supports.append(re.search(r'(\d+)$', line[-1]).group(0))
        
        return patterns, list(map(int,supports))
    
    def _create_output_dataframe(self, patterns: List[Text], supports: List[int]) -> pd.DataFrame:
        """ Create Output Dataframe 

        :return: Dataframe containing patterns and corresponding support
        """
        return pd.DataFrame((patterns, supports), index=['patterns', 'support']).T

    def run_pandas(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """ Run TKE algorithm on Pandas Dataframe

        :param input_df: Input Dataframe containing Itemsets in 'Itemset' column
            NOTE: If present, Timestamp column must be set as index
        :return: Dataframe containing the k episodes with highest frequency of occurence.
        """
        return super().run_pandas(input_df)

    
    def run_file(self, input_file_name: Text) -> Tuple[List[Text], List[int]]:
        """ Run TKE algorithm on an input txt file

        :param input_file_name: Input txt file name
        :return: Tuple of patterns and corresponding support
        """
        return super().run_file(input_file_name)
        


        
        
        
         
        

