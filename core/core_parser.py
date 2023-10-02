""" Core Module: Arguments Parser """

# import os
import sys

import argparse
import inspect

import json

## Importing:
from core import core_module
from core import core_toolset as toolset

## ----------------------------------------------
def user_input(
        get_args: bool = True,
        input_config: dict = None
    ) -> argparse.ArgumentParser:
    """
    Objective:  Configure User-Input Arguments
    Parameters:
        get_args (bool): Get User-Input Arguments (default: True)
        json_config (dict): User-Input JSON Configuration (default: None)
    Returns:    List -> [ input_parser, input_args, rouge_args ]
    Reference:  https://docs.python.org/3/library/argparse.html
    """

    toolset.trace_workflow( inspect.currentframe() )

    input_parser = user_parser(
        parser = input_config
    )

    ## Configuring Script Features: parser["options"][*]
    parser = core_module.configure_features( input_config )

    for options in [
        parser["options"]["params"],
        parser["options"]["defaults"]
    ]:
        for _, value in options.items():
            # print( f"key: { _ } -> value: { value }", end = "\n\n" )

            ## Configure Parameter -> Param-Arguments
            args, params = core_module.configure_parameter( value )
            input_parser.add_argument( *args, **params )

    ## Aggregating all User-Input parameters
    input_args, rouge_args = input_parser.parse_known_args()

    # print(
    #     "core-module -> user-input -> input-args:",
    #     input_args
    # )
    # print(
    #     "core-module -> user-input -> rouge-args:",
    #     rouge_args
    # )

    if get_args:

        # print( get_args )
        ## No-Arguments -> Displaying Help
        # if len( sys.argv ) == 1:
        #     display_help( parser )

        ## --------------------------------------
        if input_args.version is True:
            package_version = ".".join( map( str, list(
                parser["package"]["version"].values()
            ) ) )
            print( f"Version: { package_version }" )

        ## --------------------------------------
        if input_args.params:
            ## Display User-Input parameters
            # print( input_args )

            params = {
                "params": {}
            }
            for arg in input_args.__dict__:
                # print( f"{ arg } = { input_args.__dict__[ arg ] }" )
                params["params"] |= { arg: input_args.__dict__[ arg ] }
            print()
            print( json.dumps( params, indent = 4 ) )

        return [ input_parser, input_args, rouge_args ]

    return input_parser

## ----------------------------------------------
def user_parser(
        parser: dict = None
    ) -> argparse.ArgumentParser:
    """
    Objective:  Generate argparse.ArgumentParser
    Parameters:
        parser (dict): User-Input JSON Configuration (default: None)
    Returns:    input_parser (argparse.ArgumentParser)
                parser (dict)
                <class 'argparse.Namespace'>
    """

    toolset.trace_workflow( inspect.currentframe() )

    if parser is None:
        message = "Missing User-Input JSON Configuration!"
        # display_warning(  message )
        sys.exit( message )
    # print( "user-parser:", json.dumps( parser, indent = 4 ) )

    # program = os.path.join(
    #     parser["package"]["path"],
    #     parser["package"]["script"]
    # )

    help_formatter = parser["formatter"]
    if help_formatter == "default":
        help_formatter = argparse.ArgumentDefaultsHelpFormatter

    description = parser["package"]["description"]
    if description is None:
        description = 'Processing User-Input parameters'

    input_parser = argparse.ArgumentParser(
        prog = parser["package"]["name"],
        usage = None,
        description = description,
        parents = [],
        formatter_class = help_formatter,
        prefix_chars = '-',
        fromfile_prefix_chars = None,
        argument_default = None,
        conflict_handler = 'error',
        add_help = True,
        allow_abbrev = True,
        exit_on_error = False
    )
    # input_parser = argparse.ArgumentParser( description = description )

    return input_parser

## ------------------------------------------
def process_userinput(
        question: str = None
    ) -> str:
    """
    Objective:  Parsing project parameters (input)
    Parameters:
        question (str): Configuration parameters question
    Returns:    input (str): Parsed user input
    """

    response = toolset.__empty__
    while response == toolset.__empty__:
        response = input( question )
        if response == toolset.__empty__:
            print(
                "\033[A\033[J" * len( response ),
                end = toolset.__empty__
            )

    return response
