```console
Help on module conftest:

NAME
    conftest - Unit Testing Configuration File

FUNCTIONS
    fixture__application() -> str
        Objective:  Testing unit_test function
        Parameters:
            application (str)
        Returns:    current working directory (str)
    
    fixture__args_parser() -> argparse.ArgumentParser
        Objective:  Provide an ArgumentParser object
        Parameters:
            args_parser (argparse.ArgumentParser)
        Returns:    ArgumentParser object (argparse.ArgumentParser)
    
    fixture__current_directory() -> str
        Objective:  Obtain current working directory
        Parameters:
            current_directory (str)
        Returns:    current working directory (str)
    
    fixture__custom_message() -> str
        Objective:  Generating a custom random message
        Parameters:
            custom_message (str)
        Returns:    custom random message (str)
    
    fixture__json_config() -> dict
        Objective:  Testing unit_test function
        Parameters:
            json_config (dict)
        Returns:    current working directory (str)
    
    fixture__test_module() -> bool
        Objective:  Testing unit_test function
        Parameters:
            test_module (bool)
        Returns:    current working directory (str)

FILE
    tests/conftest.py
```