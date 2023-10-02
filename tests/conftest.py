""" Unit Testing Configuration File """

import random
import string
import sys
import os

import json
import argparse
import pytest

## Importing:
from core import core_module

### Fixtures & Parameters

## ----------------------------------------------
@pytest.fixture( name='application' )
def fixture__application() -> str:
    """
    Objective:  Testing unit_test function
    Parameters:
        application (str)
    Returns:    current working directory (str)
    """
    return "project.py"

## ----------------------------------------------
@pytest.fixture( name='json_config' )
def fixture__json_config() -> dict:
    """
    Objective:  Testing unit_test function
    Parameters:
        json_config (dict)
    Returns:    current working directory (str)
    """

    filepath = os.path.join(
        os.path.dirname( os.path.basename( __file__ ) ),
        "tests", "configs", "project.json"
    )

    if os.path.isfile( filepath ):
        ## Converting JSON to Python dictionary
        config = json.loads( core_module.import_config( filepath ) )
    else:
        message = f"Missing JSON Configuration: { filepath }"
        sys.exit( message )

    ## Adding abspath to JSON object
    config["script"]["package"]["abspath"] = os.getcwd()

    ## Removing Enable/Disable Storage
    if "storage" in config:
        del config["storage"]

    ## Disabling Input Arguments (enable/disable storage)
    if "enable" in config["script"]["input"]["args"]:
        config["script"]["input"]["args"]["enable"] = None

    # toolset.print_json( config )

    return config

## ----------------------------------------------
@pytest.fixture( name='test_module' )
def fixture__test_module() -> bool:
    """
    Objective:  Testing unit_test function
    Parameters:
        test_module (bool)
    Returns:    current working directory (str)
    """
    return True

## ----------------------------------------------
@pytest.fixture( name='current_directory' )
def fixture__current_directory() -> str:
    """
    Objective:  Obtain current working directory
    Parameters:
        current_directory (str)
    Returns:    current working directory (str)
    """
    return os.getcwd()

## ----------------------------------------------
@pytest.fixture( name='custom_message' )
def fixture__custom_message() -> str:
    """
    Objective:  Generating a custom random message
    Parameters:
        custom_message (str)
    Returns:    custom random message (str)
    """
    return ''.join(
      random.sample((
        string.ascii_uppercase+string.digits
      ) * 10,50 )
    )

## ----------------------------------------------
@pytest.fixture( name='args_parser' )
def fixture__args_parser() -> argparse.ArgumentParser:
    """
    Objective:  Provide an ArgumentParser object
    Parameters:
        args_parser (argparse.ArgumentParser)
    Returns:    ArgumentParser object (argparse.ArgumentParser)
    """
    return argparse.ArgumentParser()
