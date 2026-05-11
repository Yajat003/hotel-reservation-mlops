import traceback
import sys

class CustomException(Exception):
    # This custom exception class extends python's built-in Exception; it captures additional debugging info. such as the file name & the line number where the error occurred.
    
    def __init__(self, error_message, error_detail: sys):
        # This Constructor accepts a custom error message and calls the parent Exception constructor and then enhances the message with detailed debugging info
        
        super().__init__(error_message)
        
        # Generate a detailed error msg. including filename & line number
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message, error_detail: sys):
        # This static method gets the current exception details using sys.exc_info() and extracts file name & line number from the traceback object, and formats a detailed message.                


        # sys.exc_info() returns (type, value, traceback)
        _, _, exc_tb = traceback.sys.exc_info()     
        # get the file name where the exception occurred
        file_name = exc_tb.tb_frame.f_code.co_filename
        # get the line number where the exception occurred
        line_number = exc_tb.tb_lineno

        return f"Error in {file_name}, line {line_number} : {error_message}"
    
    def __str__(self):
        # Overrides the default string representation of the exception and when the exception object is printed this message will be shown.

        return self.error_message