""" Testing: Core Module """

import argparse
import pytest

## Importing:
from core import core_module, core_parser
from core import core_toolset as toolset

### Unit Testing Functions

## ----------------------------------------------
def test__display_help( args_parser ) -> bool:
    """
    Objective:  Testing display_help function
    Parameters:
        args_parser (argparse.ArgumentParser)
    Returns:    True/False (bool)
    """
    with pytest.raises( SystemExit ) as system_exit:
        core_module.display_help( args_parser )
    expect = False
    assert system_exit.type == SystemExit
    assert system_exit.value.code == expect

## ----------------------------------------------
def test__user_input( json_config ) -> bool:
    """
    Objective:  Testing user_input function
    Parameters:
        json_config (dict)
    Returns:    True/False (bool)
    """

    parser = {
        "package": json_config["script"]["package"],
        "formatter": json_config["script"]["helper"]["formatter"],
        "options": json_config["script"]["options"]
    }
    # print(
    #     "tests--core-module -> user-input -> parser:",
    #     json.dumps( parser, indent = 4 )
    # )

    result = core_parser.user_input(
        input_config = parser
    )
    actual = result[1]
    # print( "test--core-module -> user-input -> actual", actual )

    input_parser = argparse.ArgumentParser()

    defaults = json_config["script"]["options"]["defaults"]
    args, params = core_module.configure_parameter(
        value = defaults["version"]
    )
    input_parser.add_argument( *args, **params )

    expected = input_parser.parse_known_args()[0]
    # print( "test--core-module -> user-input -> expected", expected )

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
def test__load_script(
        application: str = "project.py",
        json_config: dict = None
    ) -> bool:
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
def test__module(
        test_module: bool = True
    ) -> bool:
    """
    Objective:  Testing unit_test function
    Parameters:
        test_module (bool)
    Returns:    True/False (bool)
    """

    actual = toolset.unit_test( test_module )
    expected = True
    assert actual == expected
