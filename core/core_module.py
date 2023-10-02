""" Core Module: Objects, Functions """

import os
import sys

import re
import subprocess

import hashlib
import datetime

import ast
import codecs

import argparse

import json
import git

# from pprint import pprint

## Importing Global Variables
from core import core_classes

## Importing Global Variables
from core import core_toolset as toolset

config = {}
version = {}

__empty__ = ''
__space__ = ' '
__dot__ = '.'

repo = git.Repo( __dot__, search_parent_directories = True )

## ----------------------------------------------
def activate_project(
        target_project: str=os.getcwd()
    ) -> str:
    """
    Objective:  Activating Project
    Parameters:
        target_project (str): Target project path
    Returns:    project (str)
    """

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
def configure_gitrepo() -> bool:
    """
    Objective:  Extract Git Repository Configuration
    Parameters: None
    Returns:    True (bool)
    """

    ## Git Repository Configuration
    if repo:
        ## Git Repository Details
        repo_url = repo.remotes.origin.url
        ## Git Repository Origin
        repo_origin = repo_url.split( '.git' )[0].split( '/' )
        domain, account, repository = [
            repo_origin[ index ] for index in ( 2, 3, 4 )
        ]
        ## Script Info-Repo Configuration
        config["script"]["info"]["repo"] = {
            "url": repo_url,
            "domain": domain,
            "account": account,
            "repo": repository
        }
    else:
        config["script"]["info"]["repo"] = {}
        display_warning( "Unable to identify Git Repository" )

    return True

## ----------------------------------------------
def configure_parameter(
        value: dict=None,
        parser: dict=None
    ) -> list:
    """
    Objective:  Configure User-Input Parameter
    Parameters: value (dict)
    Returns:    True (bool)
    """

    params = []
    for index in value:
        # print( f"key: { index } -> value: { value[ index ] }" )

        ## Resolving configuration issues (e.g.: action/const)
        if index == "action":
            if value[ index ] != "store":
                matches = [
                    "action", "const", "default", "dest",
                    "help", "metavar", "nargs", "required", "type"
                ]
            else:
                matches = [
                    "action", "default", "dest",
                    "help", "required"
                ]

        if "name" in index:
            # args = [ f"'{ index }'" for index in value["name"] ]
            # for arg in args:
            #     params.append( arg )
            pass
        elif any( param in index for param in matches ):
            params.append(
                inspect_parameter( index, value[ index ], parser )
            )
        elif "type" in index:
            params.append(
                inspect_parameter( index, value[ index ], parser )
            )
        else:
            pass

    # print( f"\n{ params }" )
    args = ", ".join( [ f"'{ key }'" for key in value["name"] ] )
    params = ", ".join( params )

    return [ args, params ]

## ----------------------------------------------
def display_help(
        argparser: argparse.ArgumentParser=None
    ) -> bool:
    """
    Objective:  Displaying Help
    Parameters:
        argparser (argparse.ArgumentParser)
    Returns:    sys.exit( False )
    """

    print()
    argparser.print_help()
    print()

    sys.exit( False )

## ----------------------------------------------
def display_message(
        heading = False,
        message = __empty__,
        newline = True
    ) -> bool:
    """
    Objective:  Display custom (heading: message)
    Parameters:
        heading (str): Message heading (default: False)
        message (str): Message body/content
        newline (bool): Newline (default: True)
    Returns:    True (bool)
    """

    ## Headings
    if heading:
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
        message (str): Message body/content
    Returns:    True (bool)
    """
    display_message( heading = "Warning: ", message = message )
    return True

## ------------------------------------------
def configure_revparse(
        verbose: bool=False
    ) -> core_classes.JsonObject:
    """
    Objective:  Configure Git Rev-Parse
    Parameters: None
    Returns:    revparse (core_classes.JsonObject)
    Reference:  https://git-scm.com/book/en/v2/
                Git-Internals-Environment-Variables
    """

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
        value = fetch_revparse( f"--{ key }" )
        revparse[ index ] = value
    parent = os.path.basename( revparse['superproject'] )
    revparse["parent"] = parent
    ## Constructing Project Path
    project = revparse["toplevel"].replace(
        f"{ revparse['superproject'] }{ os.sep }",
        __empty__
    )
    revparse["project"] = project
    remove = revparse['superproject'].replace(
        revparse["parent"],
        __empty__
    )
    revparse["remove"] = remove

    ## Displaying Git Rev-Parse
    if verbose:
        print()
        for key, value in revparse.items():
            print( f"{ key }: { value }" )

    return core_classes.JsonObject( revparse )

## ------------------------------------------
def fetch_revparse(
        command: str=None
    ) -> list | bool:
    """
    Objective:  Executing System Process
    Parameters: None
    Returns:    revparse (list)
    Reference:  https://git-scm.com/docs/git-rev-parse
    """

    message = f"Unable to determine '{ command }'!"
    try:
        output = str( subprocess.run(
                [ 'git', 'rev-parse', command ],
                check=True, capture_output=True, text=True
            ).stdout ).strip()
    except subprocess.CalledProcessError as ex:
        display_warning( f"{ message }\n{ ex }" )
        return False

    return output

## ----------------------------------------------
def get_filestat(
        srcfile: str=None
    ) -> str:
    """
    Objective:  Extracting File Statistics
    Parameters:
        srcfile (str): Source File (resource)
    Returns:    report (str)
    """

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

    return toolset.bucket_sizetype( filesize )

## ----------------------------------------------
def get_version(
        config_file: str=None
    ) -> str:
    """
    Objective:  Get Package Version (.package file)
    Parameters:
        configfile (str): Parent directory
    Returns:    version (str)
    """

    for line in read_version( config_file ).splitlines():
        if line.startswith( '__version__' ):
            delim = '"' if '"' in line else "'"
            return line.split( delim )[1]
        raise RuntimeError( "Unable to find package version." )

## ----------------------------------------------
def import_config(
        srcfile: str=None,
        spaces: int = 4
    ) -> bool:
    """
    Objective:  Import Configuration
    Parameters:
        srcfile (str): JSON Configuration File (resource)
        spaces (int): Indentation (default: 4)
    Returns:    False (bool) | json_config (str)
    """

    if srcfile is not None:
        if os.path.exists( srcfile ):
            try:
                with open(
                    srcfile,
                    "r",
                    encoding='utf-8'
                ) as json_file:
                    data = json.load( json_file )
            except FileNotFoundError as ex:
                print( f"Warning Error: { ex }" )
                return False
            # print( f"Loaded JSON Configuration\n{ srcfile }" )
            json_config = json.dumps(
                data,
                indent = spaces
            )
            # print( json_config )
            return json_config
        display_warning( "JSON Configuration does not exist!" )
    else:
        display_warning( "Missing Import-Config JSON Configuration!" )

    return False

## ----------------------------------------------
def inspect_parameter(
        index: str=None,
        content: str=None,
        parser: dict=None
    ) -> str:
    """
    Objective:  Inspect Parameter/Argument Value
    Parameters:
        index   (str): Argument index
        content (str): Argument value
    Returns:    content (str)
    """

    # print( "\nOriginal:", index, " -> ", content )

    ## Inspecting for regex in parameter value
    match = re.search(
        r'^(\{){2}(\ ?)(.*)(\}){2}$',
        str( content ).replace( " ", __empty__ )
    )
    if match:
        content = match.group( 3 )
        parameter, attribute = str( content ).split( __dot__ )
        content = f"{ parser[ parameter ][ attribute ] }"

    ## Warning: Inspecting for malformed parameter value
    try:
        # report = ast.dump( ast.parse( f"{ args }, { params }" ) )
        _ = ast.literal_eval( content )
    except (ValueError, SyntaxError):
        pass

    ## Configuring parameter's enclosing state
    enclose = True
    if content in [ True, False ] or index == "type":
        # print( "\nIndex [ ", index, " ] -> ", content, end="\n\n" )
        enclose = False

    ## Enclosing parameter value in single-quotes
    if enclose:
        output = f"{ index }=\'{ content }\'"
    else:
        output = f"{ index }={ content }"
    content = output

    # print( f"Parameter: [ { content } ]" )

    return content

## ----------------------------------------------
def list_config(
        json_config: dict=None
    ) -> bool:
    """
    Objective:  Listing Script Configuration
    Parameters:
        app (dict): Script Configuration
    Returns:    sys.exit()
    """

    if isinstance( json_config, dict ):
        print( json.dumps(
            json_config,
            indent = config.script.exports.json.indent
        ) )
    sys.exit()

## ----------------------------------------------
def list_helper() -> bool:
    """
    Objective:  Displaying Custom Help
    Parameters: None
    Returns:    bool (True)
    """

    return True

## ----------------------------------------------
def load_assets(
        srcfile: str="project.json",
        project: dict=None
    ) -> core_classes.AppConfig:
    """
    Objective:  Loading Custom Configuration
    Parameters: None
    Returns:    True (bool)
    """

    dirname = os.path.dirname( srcfile )
    try:
        if dirname[0] == __dot__:
            dirname = os.getcwd()
    except IndexError:
        dirname = os.getcwd()

    basename = os.path.basename( srcfile )
    # print( f"load_assets -> Basename: { basename }" )

    filename = os.path.splitext( basename )
    # print( f"load_assets -> Filename: { filename[0] }" )

    source = os.path.join(
        project["abspath"],
        f"{ filename[0] }.json"
    )
    # print( f"load_assets -> Configuration: { asset }" )

    ## Loading Default Configurations
    load_config(
        srcdict = config,
        srcfile = source,
        project = project["prjpath"]
    )

    message = f"File { srcfile } does not exist!"
    if "assets" in config:
        if len( config["assets"] ) > 0:
            # print( f"Loading Assets: { config['assets'] }" )
            for config_file in config["assets"]:
                # print( f"Loading: { config_filse }" )
                source = os.path.join(
                    project["abspath"],
                    project["configs"],
                    config_file[ "file" ]
                )
                # print( f"Assets: File { srcfile }" )
                if os.path.exists( srcfile ):
                    load_config(
                        srcdict = config,
                        srcfile = source,
                        project = os.path.join(
                            project["prjpath"],
                            project["configs"]
                        ),
                        bucket = config_file[ "bucket" ]
                    )
                else:
                    display_warning( message )
                    del config_file[ "bucket" ]
            ## Purging "assets" key from dictionary
            del config["assets"]

    return config

## ----------------------------------------------
def load_buckets() -> dict:
    """
    Objective:  Loading Custom Configuration
    Parameters: None
    Returns:    True (bool)
    """

    srcfile = os.path.join(
        os.path.dirname(
            os.path.dirname( os.path.abspath( __file__ ) )
        ),
        "core",
        "core_buckets.json"
    )
    imported = import_config( srcfile = srcfile )
    if isinstance( imported, str ):

        core_buckets = json.loads( imported )
        if isinstance( core_buckets, dict ):

            if core_buckets["buckets"]:
                # print( json.dumps( core_buckets["buckets"], indent = 4 ) )
                return core_buckets["buckets"]

    return None

## ----------------------------------------------
def load_config(
        srcdict: dict=None,
        srcfile: str=None,
        project: str=None,
        bucket: str=None
    ) -> dict:
    """
    Objective:  Loading Script Configuration
    Parameters:
        srcdict  (dict): Source dictionary (default: None)
        srcfile (str): JSON Configuration File (resource)
        bucket   (str): Target bucket (default: None)
    Returns:    srcdict (dict)
    """

    ## Aborting execution if srcfile is missing
    if srcfile is None:
        display_warning( "Load Config - Missing Script Configuration!" )
        return False

    ## Initialize Source Dictionary (srcdict)
    if srcdict is None:
        srcdict = {}

    dirname = os.path.dirname( srcfile )
    try:
        if dirname[0] == __dot__:
            dirname = os.getcwd()
    except IndexError:
        dirname = os.getcwd()
    # print( f"load_config -> Dirname: { dirname }" )

    basename = os.path.basename( srcfile )
    # print( f"load_config -> Basename: { basename }" )

    filename = os.path.splitext( basename )
    # print( f"load_config -> Filename: { filename[0] }" )

    confile = os.path.join( dirname, f"{ filename[0] }.json" )
    # print( f"load_config -> Configuration: { confile }" )

    ## Loading Project Configuration

    # print( config )
    message = f"File { confile } does not exist!"
    # print( confile )
    if os.path.exists( confile ):

        try:
            with open(
                confile,
                "r",
                encoding='utf-8'
            ) as file:
                if bucket is None:
                    # srcdict = json.load( file )
                    srcdict.update( json.load( file ) )
                else:
                    if __dot__ in bucket:
                        script, options = bucket.split( __dot__ )
                        srcdict[ script ][ options ] = json.load( file )
                    else:
                        srcdict[ bucket ] = json.load( file )
                        # print( srcdict[bucket] )
            ## Appending file details
            filesize = get_filestat( confile )

        except FileNotFoundError as ex:
            display_warning( f"{ message }\n{ ex }" )

        try:
            with open(
                confile,
                "rb"
            ) as rbinary:
                filehash = hashlib.md5(
                    rbinary.read()
                ).hexdigest()
            filedate = datetime.datetime.fromtimestamp(
                os.path.getmtime( confile )
            )
            fileset = { "file": {
                "path": project,
                "name": filename[0],
                "type": "json",
                "size": f"{ filesize }",
                "hash": f"{ filehash }",
                "date": f"{ filedate }"
            } }
            if bucket is None:
                srcdict['source'] = fileset
                # print( srcdict['source'] )
            else:
                if __dot__ in bucket:
                    script, options = bucket.split( __dot__ )
                    srcdict[ script ][ options ]["source"] = fileset
                else:
                    srcdict[ bucket ]['source'] = fileset
                    # print( srcdict[ bucket ]['source'] )

        except FileNotFoundError as ex:
            display_warning( f"{ message }\n{ ex }" )

    else:
        display_warning( f"{ message }" )

    return srcdict

## ----------------------------------------------
def load_project() -> dict:
    """
    Objective:  Configure Project Paths
    Parameters: None
    Returns:    project (dict)
    """

    gitrepo_dirname = os.path.basename( os.path.normpath(
        repo.working_tree_dir
    ))
    # print( f"\nload_script -> Project Git-Repo:\n{ gitrepo_dirname }" )

    module_parent = os.path.dirname(
        os.path.dirname( os.path.abspath( __file__ ) )
    )

    if repo.working_tree_dir == module_parent:
        # print( "Simple Project Structure!" )
        abspath = repo.working_tree_dir
    else:
        # print( "Complex Project Structure!" )
        abspath = module_parent

    # print( f"\nload_script -> Project Directory:\n{ abspath }" )
    os.chdir( abspath )

    prjpath = abspath.split( f"{ gitrepo_dirname }{ os.sep }" )
    if len( prjpath ) == 1:
        prjpath = __empty__
    else:
        prjpath = prjpath[-1]
    # print( f"\nload_script -> Project Path:\n{ prjpath }" )

    project = {
        "gitrepo": gitrepo_dirname,
        "abspath": abspath,
        "prjpath": prjpath,
        "configs": "conf",
    }
    # print( project )

    return project

## ----------------------------------------------
def load_script(
        srcfile: str=None,
        json_config: dict=None
    ) -> list:
    """
    Objective:  Correcting execution context
    Parameters:
        parent (str): Parent directory
        child  (str): Child directory (default: "..")
    Returns:   List [ input_parser, input_args, rouge_args, config ]
    """

    ## Loading Custom Configurations
    if json_config is not None:
        display_warning( "Missing Load-Script JSON Configuration!" )
        # config = json_config

    ## Aborting execution if srcfile is missing
    if srcfile is None:
        display_warning( "Load Script - Missing Script Configuration!" )
        return False

    project = load_project()
    # print( project )

    filename = os.path.join(
        project["abspath"],
        srcfile
    )
    # print( "filename:", filename )

    ## Loading Default/Custom Configurations
    load_assets(
        f"{ os.path.splitext( filename )[0] }.json",
        project
    )

    name = os.path.splitext( srcfile )[0]

    config["script"]["package"]["name"] = name
    config["script"]["package"]["script"] = srcfile

    config["script"]["package"]["abspath"] = project["abspath"]
    config["script"]["package"]["path"] = project["prjpath"]
    config["script"]["package"]["configs"] = project["configs"]

    ## Loading Script Buckets (configs)
    config["script"]["buckets"] = load_buckets()

    ## Script Export Configurations
    package = config["script"]["package"]
    filepath = os.path.join(
        package["path"], "exports", project["configs"]
    )

    config["script"]["exports"]["config"]["path"] = filepath
    ## Default Configuration Filename: package["name"]
    config["script"]["exports"]["config"]["name"] = "project"

    ## Git Repository Configuration
    configure_gitrepo()

    # ## Configure User-Input Parser
    _ = user_input()
    input_parser, input_args, rouge_args = _
    # print( vars( input_args ) )

    ## Script Arguments
    config["script"]["input"]["args"] = vars( input_args )

    ## Returns: Script Location
    return [ input_parser, input_args, rouge_args, config ]

## ------------------------------------------
def print_divisor(
        character = '-',
        length = 80
    ) -> str:
    """
    Objective:  Display Section Divisor (character * length)
    Parameters:
        string (str): Divisor character
        length (int): Length of divisor
    Returns:    True (bool)
    """

    return character * length

## ----------------------------------------------
def read_version(
        config_file: str=None
    ) -> str:
    """
    Objective:  Read Package Version (.package file)
    Parameters:
        configfile (str): Parent directory
    Returns:    version (str)
    Reference:  https://packaging.python.org/en/latest/guides/
                single-sourcing-package-version/
    """

    parent = os.path.abspath( os.path.dirname( os.path.dirname( __file__ ) ) )
    with codecs.open( os.path.join( parent, config_file ), 'r') as file_pointer:
        return file_pointer.read()

## ----------------------------------------------
def user_input(
        get_args: bool=True,
        json_config: dict=None
    ) -> core_classes.AppConfig | list:
    """
    Objective:  Configure User-Input Arguments
    Parameters:
        get_args (bool): Get User-Input Arguments (default: True)
        json_config (dict): User-Input JSON Configuration (default: None)
    Returns:    List -> [ input_parser, input_args, rouge_args ]
    Reference:  https://docs.python.org/3/library/argparse.html
    """

    input_parser, parser = user_parser(
        json_config = json_config
    )

    options = parser["options"]
    # print( options )

    for _, value in options.items():
        # print( f"key: { key } -> value: { value }" )

        ## Configure Parameter -> Param-Argument
        args, params = configure_parameter( value, parser )
        parse_args = str(
            f"input_parser.add_argument( { args }, { params } )"
        )

        # print( parse_args )
        eval( parse_args )

    ## Aggregating all User-Input parameters
    input_args, rouge_args = input_parser.parse_known_args()

    # print( "core-module -> user-input -> input-args:", input_args )
    # print( "core-module -> user-input -> rouge-args:", rouge_args )

    if get_args:

        # print( get_args )
        ## No-Arguments -> Displaying Help
        # if len( sys.argv ) == 1:
        #     display_help( parser )

        # ## --------------------------------------
        # if input_args.json:
        #     ## Display JSON Configuration (conf/config.json)
        #     export = config["script"]["exports"]
        #     filename = f'{ export["config"]["name"] }.{ export["config"]["type"] }'
        #     config_path = os.path.join(
        #         config["script"]["package"]["abspath"],
        #         filename
        #     )
        #     print( import_config(
        #         config_path,
        #         export["config"]["indent"]
        #     ) )

        ## --------------------------------------
        if input_args.version is True:
            package_version = ".".join( map( str, list(
                config["script"]["package"]["version"].values()
            ) ) )
            print( f"Version: { package_version }" )

        ## --------------------------------------
        if input_args.params:
            ## Display User-Input parameters
            print( input_args )

        return [ input_parser, input_args, rouge_args ]

    return [ input_parser ]

## ----------------------------------------------
def user_parser(
        json_config: dict=None
    ) -> argparse.ArgumentParser:
    """
    Objective:  Generate argparse.ArgumentParser
    Parameters:
        json_config (dict): User-Input JSON Configuration (default: None)
    Returns:    user_parser (argparse.ArgumentParser)
                parser (core_classes.AppConfig)
                <class 'argparse.Namespace'>
    """

    if json_config is None:
        # display_warning( "Missing User-Input JSON Configuration!" )
        parser = {
            "package": config["script"]["package"],
            "formatter": config["script"]["helper"]["formatter"],
            "options": config["script"]["options"]["params"]
        }
    else:
        parser = json_config
    # print( "user-parser:", json.dumps( parser, indent = 4 ) )

    ## Script Import Configurations
    default_params = json.loads( import_config(
        os.path.join(
            os.path.dirname(
                os.path.dirname( os.path.abspath( __file__ ) )
            ),
            "core",
            "core_options.json"
        )
    ) )
    # print( default_params )

    if isinstance( default_params, dict ):
        parser["options"] |= default_params
    # print( json.dumps( parser["options"], indent = 4 ) )

    program = os.path.join(
        parser["package"]["path"],
        parser["package"]["script"]
    )

    help_formatter = parser["formatter"]
    if help_formatter == "default":
        help_formatter = argparse.ArgumentDefaultsHelpFormatter

    description = parser["package"]["description"]
    if description is None:
        description = 'Processing User-Input parameters'

    user_argparser = argparse.ArgumentParser(
        prog = program,
        usage = None,
        description = description,
        parents = [],
        formatter_class = help_formatter,
        prefix_chars = '-',
        fromfile_prefix_chars = None,
        argument_default = None,
        conflict_handler = 'error',
        add_help = True,
        allow_abbrev = True,
        exit_on_error = False
    )
    # user_argparser = argparse.ArgumentParser( description = description )

    return [ user_argparser, parser ]

## ----------------------------------------------

# Semantic Versioning
# <type> refers to the kind of change made and is usually one of:

# feat: A new feature.
# fix: A bug fix.
# docs: Documentation changes.
# style: Changes that do not affect the meaning of the code (white-space,
#     formatting, missing semi-colons, etc).
# refactor: A code change that neither fixes a bug nor adds a feature.
# perf: A code change that improves performance.
# test: Changes to the test framework.
# build: Changes to the build process or tools.
# scope is an optional keyword that provides context for where the change was made.
# It can be anything relevant to your package or development workflow
# (e.g., it could be the module or function name affected by the change).
