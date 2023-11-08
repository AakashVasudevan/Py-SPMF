""" 
Python 3 Wrapper for SPMF
http://www.philippe-fournier-viger.com/spmf

"""

from typing import Dict, Text
from pathlib import Path
from abc import ABC, abstractmethod

import pandas as pd
import os
import tempfile

class Spmf(ABC):
    """ Abstract Base Class for SPMF Wrapper """
    def __init__(self, memory: int = 1024) -> None:
        """ Initialize Object 

        :param memory:
        """
        self.executable_path = Path('../binaries/spmf.jar')
        self.memory = memory
    
    @abstractmethod
    def _parse_input_dataframe(self) -> Text:
        """ Convert Pandas Dataframe to input required by the algorithm """
        pass

    @abstractmethod
    def _create_output_dataframe(self) -> pd.DataFrame:
        """ Create Pandas Dataframe from SPMF output text file """
        pass
    
    @abstractmethod
    def run(self) -> pd.DataFrame:
        """ Run SPMF Algorithm """
        pass

    @staticmethod
    def _get_temp_file(input: Text, file_extension: Text = '.txt') -> tempfile:
        """ Write input text to a temp file and get filename 

        :param input: Text to write to temp file
        :param file_extension: Extension for temp file. Default = "txt"
        :return: Temp file object
        """
        temp_file = tempfile.NamedTemporaryFile(suffix=file_extension, delete=False)
        temp_file.write(bytes(input, 'UTF-8'))
        return temp_file
    
    @staticmethod
    def _delete_temp_file(temp_file: tempfile) -> None:
        """ Delete temporary file

        :param temp_file: tempfile object to delete
        """
        temp_file.close()
        os.unlink(temp_file)
    



    



