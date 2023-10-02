""" App Module: Project Workflow """

import os

## Importing: Application Classes
from app import mod_classes as classes

## ------------------------------------------
def main(
        env_config: dict = None,
        trg_path: str = None
    ) -> bool | None:
    """
    Objective:  Managing Git Worktree workflow
    Parameters: None
    Returns:    True (bool)
    """

    ## Initializing Application
    app = classes.Worktree( env_config )

    ## --------------------------------------
    ## Change Context -> Caller Location
    if trg_path is not None:
        os.chdir( trg_path )

    ## --------------------------------------
    if app.args.local:
        print()
        app.import_branches()

    ## --------------------------------------
    if app.args.include:
        print()
        app.include_branch(
            branch = app.args.include
        )
        print()

    ## --------------------------------------
    if app.args.list:
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
    if app.args.json:
        ## Display JSON Configuration (conf/config.json)
        print( app.json_config )

    # return None
