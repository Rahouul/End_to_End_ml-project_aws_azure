
# provides access to system-specific parameters and functions. any error that will controlled, the sys library has that information.
import sys  #Which error occurred, Where it occurred and Full traceback
from src.logger import logging # import logging file to save error of code in logger file


def error_message_detail(error, error_detail:sys):
    
    _,_, exc_tb = error_detail.exc_info() # This return exception type, exception object(value), and traceback obj(exc_tb)
    file_name = exc_tb.tb_frame.f_code.co_filename # syntax for Which Python file caused error
    error_message = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)      
        
        
        )
    
    
    return error_message
    
    
    
class CustomException(Exception): # Exception this is the parent class 
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail = error_detail)
        
    def __str__(self):
        return self.error_message
    

