```console
Help on module core_parser:

NAME
    core_parser - Core Module: Arguments Parser

FUNCTIONS
    process_userinput(question: str = None) -> str
        Objective:  Parsing project parameters (input)
        Parameters:
            question (str): Configuration parameters question
        Returns:    input (str): Parsed user input
    
    user_input(get_args: bool = True, input_config: dict = None) -> argparse.ArgumentParser
        Objective:  Configure User-Input Arguments
        Parameters:
            get_args (bool): Get User-Input Arguments (default: True)
            json_config (dict): User-Input JSON Configuration (default: None)
        Returns:    List -> [ input_parser, input_args, rouge_args ]
        Reference:  https://docs.python.org/3/library/argparse.html
    
    user_parser(parser: dict = None) -> argparse.ArgumentParser
        Objective:  Generate argparse.ArgumentParser
        Parameters:
            parser (dict): User-Input JSON Configuration (default: None)
        Returns:    input_parser (argparse.ArgumentParser)
                    parser (dict)
                    <class 'argparse.Namespace'>

FILE
    core/core_parser.py
```