""" Application Module: Worktree Classes """

import os
import sys

# from typing import Any

import re
import subprocess

# import json
import git

# from pprint import pprint

## Importing: display_warning, display_message
from core import core_module

## Importing: ConfigClass ( JsonObject, CoreClass, etc. )
from core import core_classes

## ----------------------------------------------
class Worktree( core_classes.AppConfig ):
    """
    Objective:  Construct Worktree Class
    Parameters: AppConfig (mod_classes.AppConfig)
    Returns:    None
    """

    args = None
    discard = None
    ignore = None
    json_config = None
    repo = None
    revparse = {}
    worktrees = None

    ## Class Variables

    ## ------------------------------------------
    def __init__(
            self,
            json_object: dict=None
        ) -> None:
        """
        Objective:  Initialize Class variables
        Parameters: json_object (dict) -> None
        Returns:    None
        """

        if json_object is not None:
            if self.json is None:
                self.json = json_object
        else:
            super().missing_config( "AppConfig" )

        super().__init__( json_object )

        ## Script Input Arguments
        self.args = self.script.input.args

        ## Importing JSON Configuration (exports/config/<app>.json)
        exports = self.script.exports
        self.json_config = core_module.import_config(
            exports.config.path,
            exports.config.indent
        )

        ## Configure Environment
        self.configure_environment()

    ## ------------------------------------------
    def configure_environment(
            self
        ) -> None:
        """
        Objective:  Configure Environment
        Parameters: None
        Returns:    None
        """

        ## Discarding Protected and Pull Request Branches
        self.discard = [ 'HEAD', 'master', 'main', 'clean', 'sandbox-', '-patch-' ]

        ## List of patterns to be ignored
        self.ignore = [ '.', './', '.\\' ]
        ## Filtering relative-path parameter

        ## Configure Git Revparse (core_classes.JsonObject)
        self.revparse = core_module.configure_revparse()

        ## Configure with current path if it's not provisioned
        if self.args.git_repo is False:
            ## Using current working directory
            gitrepo = self.revparse.superproject
            if gitrepo is not self.__empty__:
                self.args.git_repo = gitrepo
            else:
                self.args.git_repo = self.revparse.toplevel
            # if self.args.verbose:
            #     core_module.display_message(
            #         message = f"Super-Project:  { self.args.git_repo }"
            #     )
            #     core_module.display_message(
            #         message = f"Git Repository: { self.revparse.toplevel }"
            #     )

        # Change the current working directory
        # print( "git-repo:", self.args.git_repo )
        os.chdir( self.args.git_repo )
        # listdir = os.listdir( self.args.git_repo )
        # if self.args.verbose:
        #     core_module.display_message(
        #         message = f"Current Working Directory: { listdir }"
        #     )

        self.repo = git.Repo( self.args.git_repo )

        ## Configure Git worktree directory
        self.worktrees = os.path.join( self.args.git_repo, self.args.worktree )
        if not os.path.exists( self.worktrees ):
            try:
                os.mkdir( self.worktrees )
            except OSError:
                core_module.display_warning(
                    f"Creating directory '{ self.worktrees }' has failed!"
                )

        # return None

    ## ------------------------------------------
    def disable_branch(
            self,
            branch
        ) -> bool:
        """
        Objective:  Disable (remove) Git Worktree Branch
        Parameters: branch (str): Git Branch
        Returns:    True/False (bool)
        """

        core_module.display_message(
            heading = False,
            message = f"Removed: { branch }",
            newline = False
        )
        ## Git Worktree removing branch
        message = "Unable to remove worktree branch!"
        # try:
        #     self.repo.git.worktree( "remove", branch )
        # except git.exc.GitCommandError as ex:
        #     core_module.display_warning( f"{ message }\n{ ex }" )
        #     return False
        try:
            _ = subprocess.run(
                [ 'git', 'worktree', 'remove', branch ],
                check=True, capture_output=True, text=True
            ).stdout
            # print( _.strip() )
            self.prune_worktrees()
        except subprocess.CalledProcessError as ex:
            core_module.display_warning( f"{ message }\n{ ex }" )
            return False

        return True

    ## ------------------------------------------
    def display_worktree(
            self,
            abort = False,
            path = os.getcwd()
        ) -> bool:
        """
        Objective:  Displaying Git Worktree
        Parameters: path (str): Path to Git Repository
        Returns:    True/False (bool)
        """

        ## Git Repository parent directory to be filtered
        dirname = os.path.dirname( path )

        # if self.args.verbose:
        core_module.display_message(
            message = "\nGit Worktree Branches:\n"
        )

        ## Git Worktree Listing
        message = "Unable to list worktree branches!"
        # try:
        #     self.repo.git.worktree( "list" )
        # except git.exc.GitCommandError as ex:
        #     core_module.display_warning( f"{ message }\n{ ex }" )
        #     return False

        try:
            _ = subprocess.run(
                [ 'git', 'worktree', 'list' ],
                check=True, capture_output=True, text=True
            ).stdout.replace( f"{ dirname }/", '' )

            ## Print/Display Git Worktree Listing
            # if self.args.verbose:
            print( _.strip().replace(
                self.revparse.remove,
                self.__empty__
            ) )

        except subprocess.CalledProcessError as ex:
            core_module.display_warning( f"{ message }\n{ ex }" )
            return False

        if abort:
            sys.exit( "Done!\n" )

        return True

    ## ------------------------------------------
    def enable_branch(
            self,
            target_branch,
            message,
            path = os.getcwd()
        ) -> bool:
        """
        Objective:  Enable (add) Git Worktree Branch
        Parameters:
            message (str): Commit Message
            path (str): Path to Git Repository
            target_branch (str): Git Branch
        Returns:    True/False (bool)
        """

        ## Creating Git Worktree Branch
        core_module.display_message(
            heading = False,
            message = f" Creating Branch: { target_branch }",
            newline = False
        )

        if not os.path.exists( path ):

            if self.args.verbose:
                core_module.display_message(
                    message = " [ adding branch ]"
                )
                core_module.display_message(
                    message = f"{ message }",
                    newline = True
                )
            message = f"Unable to add branch: { target_branch } to worktree!"
            # try:
            #     self.repo.git.worktree( "add", path, target_branch )
            # except git.exc.GitCommandError as ex:
            #     core_module.display_warning( f"{ message }\n{ ex }" )
            #     return False

            ## Git Worktree adding branch
            try:
                _ = subprocess.run(
                    [ 'git', 'worktree', 'add', '--force', path, target_branch ],
                    check=True, capture_output=True, text=True
                ).stdout
                # print( _.strip() )
            except subprocess.CalledProcessError as ex:
                core_module.display_warning( f"{ message }\n{ ex }" )
                return False

        else:
            core_module.display_message(
                message = " [ already exist! ]",
                newline = False
            )
            self.inspect_worktree( path )

        # print()

        return True

    ## ------------------------------------------
    def filter_branch(
            self,
            text,
            listing,
            pattern='/'
        ) -> str:
        """
        Objective:  Splits key/pair set and return its value
        Parameters:
            text (str): Key/Pair set
            listing (list): List of values to be discarded
            pattern (str): Pattern to be used to split key/pair set
        Returns:    value (str): Extracted value or False
        """

        origin = str( text ).split( pattern )
        value = pattern.join( origin[ 1:: ] )
        valid = True
        ## Matching HEAD, master and main only
        for item in listing[:2]:
            if item == value:
                pattern = item
                valid = False
                break
        ## Matching other patterns
        for item in listing[3:]:
            match = re.search( item, value, re.IGNORECASE )
            if match:
                pattern = item
                valid = False
                break
        ## Displaying usable values
        if valid:
            return value
        # else:
            # display_section()
            # print( f"Skipped: { value } [ { pattern } ]\n" )
            # return False

        return False

    ## ------------------------------------------
    def import_branches(
            self
        ) -> bool:
        """
        Objective:  Include All Branches into Git Worktree
        Parameters: None
        Returns:    True/False (bool)
        """

        ## Excluding specific branch prefixes
        prefixes = [ '*', '+' ]

        ## Listing All branches Git Repository branches
        branches = self.repo.git.branch( '--list' ).split( '\n' )

        if len( branches ) > 0:
            for branch in branches:
                if branch.startswith( tuple( prefixes ) ):
                    continue
                branch = branch.replace(
                    self.__space__,
                    self.__empty__
                )
                self.include_branch( branch )
                # print()

        return True

    ## ------------------------------------------
    def include_branch(
            self,
            branch: str=None
        ) -> bool:
        """
        Objective:  Include Branch into Git Worktree
        Parameters:
            branch (str): Git Branch
        Returns:    True/False (bool)
        """

        if branch is not None:
            local_branch = branch.replace( os.sep, '--' )
            location = os.path.join(
                self.worktrees,
                local_branch
            )

        # if self.args.verbose:
        #     core_module.display_message(
        #         message = f"\nIncluding: { location }\n"
        #     )

        for head in self.repo.branches:
            if head.name == branch:
                self.enable_branch(
                        local_branch,
                        self.__empty__,
                        location
                    )
                return True

        return True

    ## ------------------------------------------
    def inspect_worktree(
            self,
            path
        ) -> bool:
        """
        Objective:  Inspecting Git Worktree
        Parameters:
            path (str): Path to Git Repository
        Returns:    True/False (bool)
        """

        if os.path.exists( path ):
            os.chdir( path )

            # if self.args.verbose:
            #     print()
            #     core_module.display_warning(
            #         f"Inspecting '{ path }'\n"
            #     )

            try:
                if self.repo.is_dirty():
                    print( " -> [ dirty ]" )
                    print()
                    print( self.repo.git.status().strip() )
                else:
                    print( " -> [ clean ]" )
            except OSError as ex:
                core_module.display_warning(
                    f"Unable to inspect '{ path }'\n{ ex }"
                )
                return False
        else:
            if self.args.verbose:
                core_module.display_warning(
                    f"worktree '{ path }' does not exist!"
                )
            return False

        return True

    ## ------------------------------------------
    def manage_branches(
            self
        ) -> bool:
        """
        Objective:  Managing Git Worktree branches
        Parameters: None
        Returns:    True/False (bool)
        """

        for refs in self.repo.remote().refs:
            ## Filtering specific reference-patterns (discard: list)
            remote_branch = self.filter_branch( refs, self.discard )
            if remote_branch:
            ## Backwards compatibility with python 3.7 (3.10)
            # match remote_branch:
                # if remote_branch is not False:
                # case value if value is not False:
                local_branch = remote_branch.replace( os.sep, '--' )
                location = os.path.join(
                    self.worktrees,
                    local_branch
                )
                # print( location )
                if self.args.create:
                    message = str( refs.commit.message ).strip()
                    ## Createing a Git Worktree (fetched branches)
                    self.enable_branch(
                        remote_branch,
                        message,
                        location
                    )
                    ## Changing working directory to Git Repository
                if self.args.destroy:
                    ## Destroying Git Worktree
                    if not os.path.exists( location ):
                        target = location.replace(
                            f"{ self.revparse.superproject }{ os.sep }",
                            self.__empty__
                        )
                        message = "\nWorktree Branch: "
                        message += f"[ { target } ] does not exist!"
                        if self.args.verbose:
                            print( message )
                    else:
                        # self.disable_branch( local_branch )
                        self.remove_branch(
                            target_branch = local_branch
                        )

        return True

    ## ------------------------------------------
    def prune_worktrees(
            self
        ) -> bool:
        """
        Objective:  Pruning Git Worktree
        Parameters: worktrees (str): Path to Git Worktrees
        Returns:    True/False (bool)
        Warning:    Private method invoked by remove_worktrees()
        """

        if os.path.exists( self.worktrees ):
            # print()
            message = "Pruning Git Worktree"
            # core_module.display_message(
            #   message = f"{ message }",
            #   newline = True
            # )
            try:
                _ = subprocess.run(
                    [ 'git', 'worktree', 'prune', '--verbose' ],
                    check=True, capture_output=True, text=True
                ).stdout
                # print( _.strip() )
            except subprocess.CalledProcessError as ex:
                message = "Unable to prune worktree branches!"
                core_module.display_warning( f"{ message }\n{ ex }" )
                return False

        return True

    ## ------------------------------------------
    def pull_branches(
            self
        ) -> bool:
        """
        Objective:  Updating Git Repository branches
        Parameters: None
        Returns:    True/False (bool)
        """

        if self.args.verbose:
            core_module.display_message(
                message = "\nUpdating Git Repository branches\n"
            )

        try:
            _ = subprocess.run(
                [ 'git', 'pull', '--all', '--prune', '--verbose' ],
                check=False, capture_output=True, text=True
            ).stdout.strip()

            ## Print/Display Git Pull & Prune output
            if self.args.verbose:
                print( _.strip(), end = '\n\n' )
        except subprocess.CalledProcessError as ex:
            message = "Unable to pull & prune git branches!"
            # core_module.display_warning( message )
            sys.exit( f"{ message }\n{ ex }" )

        return True

    ## ------------------------------------------
    def remove_branch(
            self,
            target_branch: str=None
        ) -> bool:
        """
        Objective:  Removing Git Worktree directory (branch)
        Parameters: worktrees (str): Path to Git Worktrees
        Returns:    True/False (bool)
        """

        # message = f"\nGit Worktree branch { target_branch }"
        # if self.args.verbose:
        #     core_module.display_message(
        #         message = f"{ message }",
        #         newline = True
        #     )

        ## Removing Git Worktree branches
        if os.path.exists( self.worktrees ):
            branches = os.scandir( self.worktrees )
            for branch in branches:
                if branch.name == target_branch:
                    if branch.is_dir():
                        message = f"Git Worktree Branch -> { branch.name }!"
                        try:
                            if self.args.verbose:
                                core_module.display_message(
                                    message = f"\nRemoving { message }"
                                )
                            _ = subprocess.run(
                                [ 'git', 'worktree', 'remove', branch.name ],
                                check=True, capture_output=True, text=True
                            ).stdout
                            # print( _.strip() )
                        except OSError as ex:
                            core_module.display_warning(
                                f"Unable to remove { message }\n{ ex }"
                            )
                            return False

            ## Pruning Git Worktree
            self.prune_worktrees()

        return True

    ## ------------------------------------------
    ## Deprecated and/or Innactive functions/methods

    # ## ------------------------------------------
    # def __fetch_branches(
    #         self
    #     ) -> bool:
    #     """
    #     Objective:  Fetching Git remote branches
    #     Parameters: None
    #     Returns:    True/False (bool)
    #     """

    #     ## Fetching remote branches
    #     message = "Unable to fetch git branches (origin)!"
    #     try:
    #         print( subprocess.run(
    #                 [ 'git', 'fetch', '--verbose', '--', 'origin' ],
    #                 check=True, capture_output=True, text=True
    #             ).stdout.strip()
    #         )
    #     except subprocess.CalledProcessError as ex:
    #         core_module.display_warning( f"{ message }\n{ ex }" )
    #         return False

    #     return True
