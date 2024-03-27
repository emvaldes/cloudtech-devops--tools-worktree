""" App Module: Project Workflow """

# import sys
import os
import inspect

## Importing:
from core import core_toolset as toolset

## Importing: Application Classes
from app.mod_classes import Worktree

## Global Variable(s):

## ------------------------------------------
def main(
        env_config: dict = None,
        trg_path: str = None,
        app_logging: str = None
    ) -> bool:
    """
    Objective:  Managing Git Worktree workflow
    Parameters:
        env_config  => Environment Configuration (dict)
        trg_path    => Target Path (str)
        app_logging => Application Logging (str)
    Returns:    True (bool)
    """

    toolset.trace_workflow( inspect.currentframe() )

    ## Initializing Application
    app = Worktree(
        json_object = env_config,
        trg_path = trg_path
    )

    if app.storage is not None:
        ## print( f"\nStorage: { app.storage }" )

        if app.args.display is not None:

            if "downloads" in app.args.display:
                downloaded = app.storage.list_files(
                    app.storage.importing["remote"],
                    app.storage.locations["import"]["files"]
                )
                if downloaded:
                    print( "\nListing Remote Downloads:\n" )
                    toolset.print_json( downloaded )

            if "uploads" in app.args.display:
                uploaded = app.storage.list_files(
                    app.storage.exporting["remote"],
                    app.storage.locations["export"]["files"]
                )
                if uploaded:
                    print( "\nListing Remote Uploads:\n" )
                    toolset.print_json( uploaded )

        if app.args.download is not None:
            # if app.args.verbose:
            #     print( "\nProject -> Downloading files ..." )
            app.storage.download_files()

        if app.args.upload is not None:
            # if app.args.verbose:
            #     print( "\nProject -> Uploading files ..." )
            app.storage.upload_files()

    ## --------------------------------------
    # if app_logging is not None:
    #     app.options["logging"] = app_logging
    _ = app_logging

    ## --------------------------------------
    ## Change Context -> Caller Location
    if trg_path is not None:
        os.chdir( trg_path )

    # ## --------------------------------------
    # if app.args.verbose:
    #     print( f"\nExecution: { app.trg_path }" )

    ## --------------------------------------
    if app.args.local:
        app.import_branches()

    ## --------------------------------------
    if app.args.include:
        print()
        app.include_branch(
            branch = app.args.include
        )
        print()

    ## --------------------------------------
    if app.args.display is not None:
        if "branches" in app.args.display:
            ## Listing Git Worktree
            app.display_worktree()
            print()

    ## --------------------------------------
    if app.args.reload:
        ## Prune & Reload Git Branches
        if app.args.local is False:
            app.pull_branches()

    ## --------------------------------------
    if app.args.remove:
        app.remove_branch(
            target_branch = app.args.remove
        )
        print()

    ## Managing Git Repository branches
    app.manage_branches()

    ## --------------------------------------
    if app.args.destroy:
        ## Removing Untracked Git Worktree branches
        if os.path.exists( app.worktrees ):
            branches = os.scandir( app.worktrees )
            for branch in branches:
                if branch.is_dir():
                    app.remove_branch(
                        target_branch = branch.name
                    )
        print()

    ## --------------------------------------
    if app.args.create or app.args.local:
        print()

    ## --------------------------------------
    if app.args.json:
        ## Display JSON Configuration (conf/config.json)
        toolset.print_json( content = app.json )

    if app.args.verbose:
        print()

    return True
