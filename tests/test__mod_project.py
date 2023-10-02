""" Testing: Application Module """

# import os
# import sys

# import json
# from pprint import pprint

# import pytest

### Fixtures & Parameters

# @pytest.fixture( name='current_directory' )
# def fixture__current_directory():
#     """
#     Objective:  Obtain current working directory
#     Parameters: None
#     Returns:    current working directory (str)
#     """
#     return os.getcwd()

### Unit Testing Functions

# def test__display_worktree( current_directory ):
#     """
#     Objective:  Testing display_worktree function
#     Parameters: current_directory (str)
#     Returns:    True/False (bool)
#     """
#     actual = worktree.display_worktree(
#       abort = False, path = current_directory
#     )
#     expected = True
#     assert actual == expected

### https://medium.com/python-pandemonium/
### testing-sys-exit-with-pytest-10c6e5f7726f
# def test__manage_worktree():
#     """
#     Objective:  Testing manage_worktree function
#     Parameters: None
#     Returns:    True/False (bool)
#     """
#     with pytest.raises( SystemExit ) as system_exit:
#         worktree.manage_worktree()
#     expected = 2
#     assert system_exit.type == SystemExit
#     assert system_exit.value.code == expected
