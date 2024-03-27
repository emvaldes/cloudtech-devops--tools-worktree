```console
Help on module test__core_module:

NAME
    test__core_module - Testing: Core Module

FUNCTIONS
    test__display_help(args_parser) -> bool
        Objective:  Testing display_help function
        Parameters:
            args_parser (argparse.ArgumentParser)
        Returns:    True/False (bool)

    test__load_script(application: str = 'project.py', json_config: dict = None) -> bool
        Objective:  Testing load_script function
        Parameters:
            application (str)
            json_config (dict)
        Returns:    True/False (bool)

    test__module(test_module: bool = True) -> bool
        Objective:  Testing unit_test function
        Parameters:
            test_module (bool)
        Returns:    True/False (bool)

    test__user_input(json_config) -> bool
        Objective:  Testing user_input function
        Parameters:
            json_config (dict)
        Returns:    True/False (bool)

FILE
    tests/test__core_module.py
```