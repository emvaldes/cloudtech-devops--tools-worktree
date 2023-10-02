#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Git Worktree Infrastructure """

import os
import sys

## Importing: load_script
from core import core_module

## Importing: Application Classes
from app import mod_project as worktree

def main(
        env_config: dict = None,
        trg_path: str = os.getcwd()
    ) -> None:
    """
    Objective:  Manage Worktree Infrastructure
    Parameters: None
    Returns:    True (bool)
    """

    ## Initializing Application
    worktree.main(
        env_config = env_config,
        trg_path = trg_path
    )

    return True

if __name__ == "__main__":

    if sys.argv[1] in [ '--git-repo' ]:
        origin_path = sys.argv[2]
    else:
        origin_path = os.getcwd()
    # print( "\nOrigin Path:", origin_path )

    ## Change context -> local
    # print( "execute:", __file__ )
    _ = core_module.load_script( os.path.basename( __file__ ) )
    parser, args, rouge_args, config = _

    ##  Run main function
    main( config, origin_path )
