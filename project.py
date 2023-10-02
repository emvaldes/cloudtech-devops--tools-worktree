#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Git Worktree Infrastructure """

import os
import sys
import inspect

## Importing:
from core import core_module
from core import core_toolset as toolset

## Importing: Application Classes
from app import mod_project as worktree

## Global Variables:

## ----------------------------------------------
def main(
        env_config: dict = None,
        trg_path: str = os.getcwd(),
        logging: str = None
    ) -> None:
    """
    Objective:  Manage Worktree Infrastructure
    Parameters:
        env_config => Environment Configuration (dict)
        trg_path   => Target Path (str)
        logging    => Application Logging (str)
    Returns:    True (bool)
    """

    toolset.trace_workflow( inspect.currentframe() )

    ## Initializing Application
    worktree.main(
        env_config = env_config,
        trg_path = trg_path,
        app_logging = logging
    )

    return True

if __name__ == "__main__":

    target_path = os.getcwd()
    if len( sys.argv ) > 1 and sys.argv[1] in [ '--git-repo' ]:
        target_path = sys.argv[2]
    # print( "\nOrigin Path:", target_path )

    toolset.script_logging(
        logs_path = target_path,
        container = 'tracer'
    )

    LOGGING = toolset.script_logging(
        logs_path = target_path,
        container = 'worktree',
        gvar_item = '__worktree__'
    )

    # print( "execute:", __file__ )
    _ = core_module.load_script( os.path.basename( __file__ ) )
    parser, args, rouge_args, config = _

    try:
        ##  Run main function
        main(
            env_config = config,
            trg_path = target_path,
            logging = LOGGING
        )

    except KeyboardInterrupt:
        try:
            print()
            sys.exit(130)
        except SystemExit:
            print()
            os._exit(130)
