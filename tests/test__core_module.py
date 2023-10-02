""" Testing: Core Module """

import os
# import sys

import json

import random
import string

import argparse
import pytest

## Importing load_script, load_config
from core import core_module

## Importing unit_test
from core import core_toolset as toolset

### Fixtures & Parameters

## ----------------------------------------------
@pytest.fixture( name='application' )
def fixture__application():
    """
    Objective:  Testing unit_test function
    Parameters: None
    Returns:    current working directory (str)
    """
    return "project.py"

## ----------------------------------------------
@pytest.fixture( name='json_config' )
def fixture__json_config():
    """
    Objective:  Testing unit_test function
    Parameters: None
    Returns:    current working directory (str)
    """

    filepath = os.path.join(
        os.path.dirname( os.path.basename( __file__ ) ),
        "exports", "config", "project.json"
    )
    ## Converting JSON to Python dictionary
    config = json.loads( core_module.import_config( filepath ) )

    return config

## ----------------------------------------------
@pytest.fixture( name='test_module' )
def fixture__test_module():
    """
    Objective:  Testing unit_test function
    Parameters: None
    Returns:    current working directory (str)
    """
    return True

## ----------------------------------------------
@pytest.fixture( name='current_directory' )
def fixture__current_directory():
    """
    Objective:  Obtain current working directory
    Parameters: None
    Returns:    current working directory (str)
    """
    return os.getcwd()

## ----------------------------------------------
@pytest.fixture( name='custom_message' )
def fixture__custom_message():
    """
    Objective:  Generating a custom random message
    Parameters: None
    Returns:    custom random message (str)
    """
    return ''.join(
      random.sample((
        string.ascii_uppercase+string.digits
      ) * 10,50 )
    )

## ----------------------------------------------
@pytest.fixture( name='args_parser' )
def fixture__args_parser():
    """
    Objective:  Provide an ArgumentParser object
    Parameters: None
    Returns:    ArgumentParser object (argparse.ArgumentParser)
    """
    return argparse.ArgumentParser()

### Unit Testing Functions

## ----------------------------------------------
def test__display_help( args_parser ):
    """
    Objective:  Testing display_help function
    Parameters: args_parser (argparse.ArgumentParser)
    Returns:    True/False (bool)
    """
    with pytest.raises( SystemExit ) as system_exit:
        core_module.display_help( args_parser )
    expect = False
    assert system_exit.type == SystemExit
    assert system_exit.value.code == expect

## ----------------------------------------------
def test__user_input( json_config ):
    """
    Objective:  Testing user_input function
    Parameters: json_config (dict)
    Returns:    True/False (bool)
    """

    parser = {
        "package": json_config["script"]["package"],
        "formatter": json_config["script"]["helper"]["formatter"],
        "options": json_config["script"]["options"]["params"]
    }
    # print(
    #     "tests--core-module -> user-input -> parser:",
    #     json.dumps( parser, indent = 4 )
    # )

    actual = core_module.user_input(
        json_config = parser
    )[1]
    # print( "test--core-module -> user-input -> actual", actual )

    input_parser = argparse.ArgumentParser()
    args, params = core_module.configure_parameter(
        json_config["script"]["options"]["params"]["version"]
    )

    parse_args = str(
        f"input_parser.add_argument( { args }, { params } )"
    )
    eval( parse_args )

    expected = input_parser.parse_known_args()[0]
    assert isinstance(
        actual, argparse.Namespace
    ) == isinstance(
        expected, argparse.Namespace
    )

    # with pytest.raises( SystemExit ) as system_exit:
    #     core_parser.user_input( json_config = parser )
    # expect = 2
    # assert system_exit.type == SystemExit
    # assert system_exit.value.code == expected

## ----------------------------------------------
def test__load_script( application, json_config ):
    """
    Objective:  Testing load_script function
    Parameters:
        application (str)
        json_config (dict)
    Returns:    True/False (bool)
    """

    actual = core_module.load_script(
        application,
        json_config = json_config
    )[-1]
    # print( "load-script: ", actual, " -> ", type( actual ) )

    expected = {}

    assert isinstance( actual, dict ) == isinstance( expected, dict )

## ----------------------------------------------
def test__module( test_module ):
    """
    Objective:  Testing unit_test function
    Parameters: test_module (bool)
    Returns:    True/False (bool)
    """

    actual = toolset.unit_test( test_module )
    expected = True
    assert actual == expected
