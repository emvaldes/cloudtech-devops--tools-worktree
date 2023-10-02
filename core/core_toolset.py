""" Core Module: Custom Toolset """

from typing import Any

import os
import sys

from datetime import datetime

import re
import subprocess

import json

import inspect
import humanize

## Global Variables:

__empty__ = ''
__space__ = ' '
__tracer__ = False

datestamp = f"{ datetime.now():%y%m%d }".strip()
datetime_stamp = f"{ datetime.now():%y%m%d-%H%M%S }".strip()

## ----------------------------------------------
def activate_project(
        target_project: str=os.getcwd()
    ) -> str:
    """
    Objective:  Activating Project
    Parameters:
        target_project (str): Target Project (default: os.getcwd())
    Returns:    project (str)
    """

    trace_workflow( inspect.currentframe() )

    project = os.path.join(
        os.getcwd(),
        target_project
    )
    if os.path.isdir( project ):
        os.chdir( project )
        # print( f"\nTarget Project:\n{ project }\n" )
        # for path, subdirs, files in os.walk( project ):
        #     for name in files:
        #         print( os.path.join( path, name ) )
    else:
        print( f"Invalid Target Project: { project }" )
        sys.exit( 1 )

    return project

## ----------------------------------------------
def bucket_sizetype(
        bucket: str=None
    ) -> int:
    """
    Objective:  Identify Size-Type
    Parameters:
        bucket (str): Bucket Size (bytes)
    Returns:    int (natural_size)
    Documentation:
        Reference:  https://stackoverflow.com/a/15485265
        Package:    https://pypi.org/project/humanize
    Requirements:
        python -m pip install --upgrade humanize
        import humanize
    """

    trace_workflow( inspect.currentframe() )

    natural_size = humanize.naturalsize( bucket )
    # binary_size = humanize.naturalsize( bucket , binary=True)

    return natural_size

## ------------------------------------------
def configure_revparse(
        repo: Any = None,
        verbose: bool = False
    ) -> dict:
    """
    Objective:  Configure Git Rev-Parse
    Parameters:
        repo (Any): Git Repository (default: None)
        verbose (bool): Display Git Rev-Parse (default: False)
    Returns:    revparse (dict)
    Reference:  https://git-scm.com/book/en/v2/
                Git-Internals-Environment-Variables
    """

    trace_workflow( inspect.currentframe() )

    _ = verbose
    if repo is None:

        default = os.getcwd()
        revparse = {
            "absolute_git_dir": default,
            "git_common_dir": __empty__,
            "git_dir": __empty__,
            "bare_repository": True,
            "inside_git_dir": False,
            "inside_work_tree": False,
            "shallow_repository": True,
            "superproject": __empty__,
            "toplevel": default,
            "parent": __empty__,
            "project": default,
            "remove": __empty__
        }

    else:

        properties = [
            "absolute-git-dir",
            "git-common-dir",
            "git-dir",
            "is-bare-repository",
            "is-inside-git-dir",
            "is-inside-work-tree",
            "is-shallow-repository",
            "show-superproject-working-tree",
            "show-toplevel"
        ]

        revparse = {}

        for key in properties:

            index = str( key ).replace( "-", '_' )
            index = index.replace( r'is_', __empty__ )
            index = index.replace( r'show_', __empty__ )
            index = index.replace(
                r'superproject_working_tree',
                'superproject'
            )

            value = fetch_revparse(
                f"--{ key }",
                verbose = False
            )

            ## Extracting the .git directory from path
            if key == 'git-common-dir':
                value.stdout = value.stdout.replace(
                    '.git',
                    __empty__
                )[:-2]

            revparse[ index ] = value.stdout.strip()

        ## Correcting Git Common Directory (empty string)
        if revparse['git_common_dir'] == __empty__:
            revparse['git_common_dir'] = revparse['superproject']

        parent = os.path.basename( revparse['superproject'] )
        revparse["parent"] = parent

        ## Constructing Project Path
        project = revparse["toplevel"].replace(
            f"{ revparse['superproject'] }",
            __empty__
        )

        revparse["project"] = project
        remove = revparse['superproject'].replace(
            revparse["parent"],
            __empty__
        )
        revparse["remove"] = remove

    # ## Displaying Git Rev-Parse
    # if verbose:
    #     print()
    #     for key, value in revparse.items():
    #         print( f"{ key }: { value }" )

    return revparse

## ----------------------------------------------
def display_message(
        heading: bool = False,
        message: str = __empty__,
        newline = True
    ) -> bool:
    """
    Objective:  Display custom (heading: message)
    Parameters:
        heading (str): Message heading (default: False)
        message (str): Message body/content (default: empty string)
        newline (bool): Newline (default: True)
    Returns:    True (bool)
    """

    trace_workflow( inspect.currentframe() )

    ## Headings
    if heading not in [ False, None ]:
        heading = "Message: "
    else:
        heading = __empty__
    ## Newline
    if newline:
        newline = '\n'
    else:
        newline = __empty__
    ## Displaying message
    print( f"{ heading }{ message }", end = newline )

    return True

## ----------------------------------------------
def display_warning(
        message: str=None
    ) -> bool:
    """
    Objective:  Display warning message
    Parameters:
        message (str): Message body/content (default: empty string)
    Returns:    True (bool)
    """

    trace_workflow( inspect.currentframe() )

    display_message(
        heading = None,
        message = f"Warning: { message }"
    )

    return True

## ------------------------------------------
def execute_command(
        command: list = None,
        message: str = "Unable to execute shell command!",
        verbose: bool = False
    ) -> Any:
    """
    Objective:  Execute Shell Command
    Parameters:
        command => Shell Command (list)
        message => Error Message (str)
        verbose => Display Shell Command (bool)
    Returns:    output (str)
    """

    trace_workflow( inspect.currentframe() )

    if command is not None:
        try:
            output = subprocess.run(
                command,
                check=False, capture_output=False, text=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            output.status = True
        except subprocess.CalledProcessError as error:
            output.status = False
            output.error = error
            display_warning( f"{ message }\n{ output.error }" )

    if verbose:
        debug = f"Status -> { output.status }\n"
        debug += f"Params -> { output.args }\n"
        debug += f"Return -> { output.returncode }\n"
        debug += f"Output -> { output.stdout.strip() }\n"
        debug += f"Errors -> { output.stderr }"

        print()
        display_message( heading = None, message = debug )

    # logging_content(
    #     output = output.stdout
    # )

    return output

## ------------------------------------------
def fetch_revparse(
        command: str = None,
        verbose: bool = False
    ) -> list | bool:
    """
    Objective:  Executing System Process
    Parameters:
        command (str): Git Rev-Parse Command
        verbose (bool): Display Git Rev-Parse (default: False)
    Returns:    revparse (list)
    Reference:  https://git-scm.com/docs/git-rev-parse
    """

    trace_workflow( inspect.currentframe() )

    message = f"Unable to determine '{ command }'!"
    output = execute_command(
        command = [ 'git', 'rev-parse', command ],
        message = message,
        verbose = verbose
    )

    return output

## ----------------------------------------------
def get_filestat(
        srcfile: str=None
    ) -> str:
    """
    Objective:  Extracting File Statistics
    Parameters:
        srcfile (str): Source File (default: None)
    Returns:    report (str)
    """

    trace_workflow( inspect.currentframe() )

    filesize = 0
    if os.path.exists( srcfile ):
        try:
            # filesize = os.path.getsize( srcfile )
            stats = os.stat(
                srcfile,
                follow_symlinks=False
            ).st_size
            filesize = stats
        except FileNotFoundError:
            print( "File not found." )
        except OSError:
            print( "OS error occurred." )

    return bucket_sizetype( filesize )

## ------------------------------------------
def logging_content(
        output: str = None,
        options: dict = None,
        verbose: bool = True
    ) -> bool:
    """
    Objective:  Logging Application Content
    Parameters:
        output => Output Content (str)
        options => Logging Options (dict)
        verbose => Display Output Content (bool)
    Returns:    None
    """

    if verbose:
        print( f"\n{ output.strip() }", end = "\n" )

    # print( "self->logging:", self.logging )
    if options["logging"] is not False:
        if os.path.isfile( options["logging"] ):
            try:
                with open(
                    options["logging"],
                    "a",
                    encoding = "utf8"
                ) as logfile:
                    logfile.write( output )
            except OSError as error:
                print( f"OS Error: { error }" )
                raise
        else:
            print( f"Missing Content: { options['logging'] }" )

    return True

## ----------------------------------------------
def name_iterator (
        location: str=os.getcwd(),
        file_name: str="file",
        file_type: str='',
        indexing: bool=True
    ) -> str:
    """
    Objective: Ensure unique file naming
    Parameters:
        location (str): File location (default: os.getcwd())
        file_name (str): File name (default: "file")
        file_type (str): File type (default: '')
        indexing (bool): Indexing (default: True)
    Returns: string
    """

    trace_workflow( inspect.currentframe() )

    if indexing is True:
        regex = r'^.*-(\d{6})-(\d{3})(\.\w+)?$'
        index = 2
    else:
        regex = r'^.*-(\d{3})(\.\w+)?$'
        index = 1

    name = file_name.strip()
    ## Parsing file type
    if len( file_type.strip() ) > 0:
        file_type = f".{ file_type.strip() }"
    else:
        name, file_type = os.path.splitext( name )
        file_type = f".{ file_type[1:].strip() }"
    file_type = file_type.replace( '..', '.' )
    # print( name, file_type )

    ## Setup file object
    fileset = {
        "name": "",
        "type": file_type,
        "version": "000"
    }

    if isinstance( location, str ):
        fileset['name'] = os.path.join(
            str( location ).strip(),
            f"{ name }-{ datestamp }"
        )
        files = sorted( os.listdir( location ) )

    if isinstance( location, list ):
        fileset['name'] = f"{ name }-{ datestamp }"
        files = location

    ## Filter files by regex
    # files = [ file for file in files if re.match( regex, file ) ]

    latest = datestamp
    for file in files:
        match = re.search( regex, file )
        if match:
            latest = file.split( '-' )[-2]
            counter = int( match.group( index ) )
            fileset['version'] = str( counter + 1 ).zfill( 3 )

    if latest < datestamp:
        fileset['version'] = '000'
    sufix = f"{ fileset['version'] }{ fileset['type'] }"
    fileset['path'] = f"{ fileset['name'] }-{ sufix }"
    # print( fileset["path"] )

    return fileset['path']

## ------------------------------------------
def print_json(
        content: dict = None
    ) -> bool:
    """
    Objective:  Displaying JSON Content
    Parameters:
        content (dict): JSON Content (default: None)
    Returns:    None
    """

    # print()
    # toolset.display_message(
    #     heading = None,
    #     message = "Displaying JSON Content"
    # )

    if content is not None:

        print(
            json.dumps(
                content,
                indent = 4
            )
        )

    return True

## ----------------------------------------------
def script_logging(
        logs_path: str = os.getcwd(),
        logs_name: str = "logs",
        container: str = __empty__,
        file_name: str = __empty__,
        gvar_item: str = '__tracer__'
    ) -> bool:
    """
    Objective:  Initialize Script Logging
    Parameters:
        logs_path (str): Logs Path (default: os.getcwd())
        logs_name (str): Logs Name (default: "logs")
        container (str): Container Name (default: '')
        file_name (str): File Name (default: '')
        gvar_item (str): Global Variable (default: '__tracer__')
    Returns:    True (bool)
    """

    logs_path = os.path.join(
        logs_path,
        logs_name,
        container
    )
    # print( logs_path )

    try:
        if not os.path.exists( logs_path ):
            os.makedirs(
                logs_path,
                exist_ok = True
            )
    except OSError as error:
        print( f"OS Error: { error }" )
        raise

    if file_name == __empty__:
        if container is not __empty__:
            file_name = f"{ container }.log"
        else:
            file_name = 'project.log'

    globals()[ gvar_item ] = name_iterator(
        location = logs_path,
        file_name = file_name
    )
    # print(
    #     f"globals()[ { gvar_item } ] <-",
    #       globals()[ gvar_item ]
    # )

    try:
        with open(
            globals()[ gvar_item ],
            "w",
            encoding = "utf8"
        ) as logfile:
            logfile.write( f"Timestamp: { datetime_stamp }\n" )
    except OSError as error:
        print( f"OS Error: { error }" )
        raise

    trace_workflow( inspect.currentframe() )

    return globals()[ gvar_item ]

## ----------------------------------------------
def trace_workflow(
        frame: inspect.FrameInfo = None
    ) -> bool:
    """
    Objective:  Trace Workflow/Execution
    Parameters:
        frame (inspect.FrameInfo): Frame Information (default: None)
    Returns:    True (bool)
    """

    # co_filename = inspect.currentframe().f_code.co_filename
    # co_names = inspect.currentframe().f_code.co_names

    # for info in inspect.stack():
    #     # frame -> frame, file, line, code
    #     print( info[0] )
    #     # filename
    #     # lineno
    #     # function
    #     # code_context
    #     # index
    #     # positions

    inspect_info = [
        frame.f_code.co_filename,
        frame.f_code.co_name,
        frame.f_lineno
    ]

    # print( __tracer__ )
    if __tracer__ is not False:

        mod_file, mod_func, mod_line = inspect_info

        # mod_file = mod_file.replace(
        #     __revparse__["git_common_dir"],
        #     __empty__
        # )

        toplevel = os.getcwd()
        if __revparse__.get( "toplevel" ):
            toplevel = __revparse__["toplevel"]
        mod_file = mod_file.replace(
            toplevel,
            __empty__
        )

        if mod_file.startswith( os.sep ):
            mod_file = mod_file[1:]

        output = f"\nModule: { mod_file } -> { mod_func } ({ mod_line })"

        if os.path.isfile( __tracer__ ):
            try:
                with open(
                    __tracer__,
                    "a",
                    encoding = "utf8"
                ) as logfile:
                    logfile.write( output )
            except OSError as error:
                print( f"OS Error: { error }" )
                raise
        else:
            print( "Missing Debugger Inspect-FrameInfo" )

    return True

## ----------------------------------------------
def unit_test(
        value: False
    ) -> True | False:
    """
    Objective:  Unit Testing function
    Parameters:
        value (bool): Value (default: False)
    Returns:    value (bool)
    """

    trace_workflow( inspect.currentframe() )

    return value

## ----------------------------------------------

__revparse__ = configure_revparse(
    repo = None,
    verbose = False
)
# print( f"\n{ __revparse__ }" )
