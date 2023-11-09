""" Sequential Pattern Mining """

import pandas as pd
import subprocess

from spmf.base import Spmf

class SeqPat(Spmf):
    """ Sequential Pattern Mining """
    def __init__(self, **kwargs) -> None:
        """ Initialize Object
        
        :param input_df: Input Dataframe
        :param kwargs: Keyword arguments to base SPMF. E.g., memory
        """
        super().__init__(**kwargs)
        

    
