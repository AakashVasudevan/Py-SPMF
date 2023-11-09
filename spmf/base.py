""" 
Python 3 Wrapper for SPMF
http://www.philippe-fournier-viger.com/spmf

"""

from typing import Dict, Text, List, Any
from pathlib import Path
from abc import ABC, abstractmethod

import pandas as pd
import os
import tempfile
import subprocess

class Spmf(ABC):
    """ Abstract Base Class for SPMF Wrapper """
    def __init__(self, memory: int = 1024, output_file_name: Text = 'output.txt') -> None:
        """ Initialize Object 

        :param memory:
        """
        self.executable_path = 'binaries\\spmf.jar'
        self.output_file_name = output_file_name
        self.memory = memory
    
    @abstractmethod
    def _parse_input_dataframe(self, input_df: pd.DataFrame) -> Text:
        """ Convert Pandas Dataframe to input string """
        pass
    
    @abstractmethod
    def _parse_output_file(self, **kwargs) -> Any:
        """ Parse output txt file created by SPMF algorithm """
        pass

    @abstractmethod
    def _create_output_dataframe(self) -> pd.DataFrame:
        """ Create Pandas Dataframe from SPMF output text file """
        pass
    
    @abstractmethod
    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """
        pass

    def run_pandas(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """ Run SPMF algorithm on Pandas Dataframe

        :param input_df: Input Dataframe            
        :return: Output Dataframe
        """
        input_file = self._convert_dataframe_to_file_object(input_df)
        self.run(input_file.name)
        self._delete_temp_file(input_file)
        return self._create_output_dataframe(*self._parse_output_file(delete=True))
    
    def run_file(self, input_file_name: Text) -> Any:
        """ Run SPMF algorithm on an input txt file

        :param input_file_name: Input txt file name
        :return: Results of the SPMF algorithm parsed from output file
        """
        
        self.run(input_file_name)        
        return self._parse_output_file(delete=True)
    
    def run(self, input_file_name: Text) -> None:
        """ Run SPMF Algorithm """

        process_arguments = self._create_subprocess_arguments(input_file_name)
        process = subprocess.check_output(process_arguments)

        if "java.lang.IllegalArgumentException" in process.decode():
            raise TypeError("java.lang.IllegalArgumentException")
        
    
    def _convert_dataframe_to_file_object(self, input_df: pd.DataFrame) -> tempfile:
        """ Convert input dataframe to text file object

        :param input_df:
        :return:
        """
        return self._create_temp_file(
            input=self._parse_input_dataframe(input_df)
        )

    def _read_output_file(self, delete: bool = False) -> List[Text]:
        """ Read output txt file created by SPMF into a list 
        
        :param delete: Set to True to delete the output file after reading
        :return: List containing each line in the output file as Text
        """

        with open(self.output_file_name, 'r') as fp:
            lines = fp.readlines()
        
        if delete:
            os.remove(self.output_file_name)

        return lines

    @staticmethod
    def _create_temp_file(input: Text, file_extension: Text = '.txt') -> tempfile:
        """ Write input text to a temp file and get file object

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
    



    



