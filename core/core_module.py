""" Core Module: Objects, Functions """

from typing import Any

import os
import sys

import re

import argparse
import ast
import codecs
import datetime
import hashlib
import inspect

import json
import yaml

import git

# from pprint import pprint

## Importing:
from core import core_parser
from core import core_toolset as toolset

## Global Variables:

config = {}
version = {}

__empty__ = ''
__space__ = ' '
__dot__ = '.'

repo = None
try:
    repo = git.Repo( __dot__, search_parent_directories = True )
except git.exc.InvalidGitRepositoryError:
    # print( git.exc.InvalidGitRepositoryError )
    pass

## ----------------------------------------------
def configure_features(
        parser: dict=None
    ) -> dict:
    """
    Objective:  Configure Script Features
    Parameters:
        parser (dict): Script Parser
    Returns:    None
    """

    toolset.trace_workflow( inspect.currentframe() )

    ## Script Import Configurations
    core_options = json.loads( import_config(
        os.path.join(
            os.path.dirname(
                os.path.dirname( os.path.abspath( __file__ ) )
            ),
            "core",
            "configs",
            "core_options.json"
        )
    ) )
    # print( core_options )

    if isinstance( core_options, dict ):
        ## Attempting to configure optional parameters
        try:
            optional = config["script"]["features"]["optional"]
        except KeyError:
            optional = False

        if optional is not False:
            for _, value in core_options.items():
                # print( f"key: { key } -> value: { value }", end = "\n\n" )
                optional.append(
                    value["name"]
                )

    if isinstance( core_options, dict ):
        parser["options"]["defaults"] = core_options
    # print( json.dumps( parser["options"]["defaults"], indent = 4 ) )

    if isinstance( parser["options"]["params"], dict ):
        ## Attempting to configure optional parameters
        try:
            examples = config["script"]["features"]["examples"]
        except KeyError:
            examples = False

        if examples is not False:
            for _, value in parser["options"]["params"].items():
                # print( f"key: { key } -> value: { value }", end = "\n\n" )
                examples.append(
                    value["name"]
                )

    return parser

## ----------------------------------------------
def configure_gitrepo() -> bool:
    """
    Objective:  Extract Git Repository Configuration
    Parameters: None
    Returns:    True (bool)
    """

    toolset.trace_workflow( inspect.currentframe() )

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
        toolset.display_warning(  "Unable to identify Git Repository" )

    return True

## ----------------------------------------------
def configure_parameter(
        value: dict=None
    ) -> list:
    """
    Objective:  Configure User-Input Parameter
    Parameters:
        value (dict): Parameter value
    Returns:    True (bool)
    """

    toolset.trace_workflow( inspect.currentframe() )

    params = {}
    for index in value:
        # print( f"key: { index } -> value: { value[ index ] }" )

        ## Resolving configuration issues (e.g.: action/const)
        if index == "action":
            if value[ index ] == "extend":
                matches = [
                    "action", "dest",
                    "help", "metavar", "nargs", "required"
                ]
            elif value[ index ] == "store":
                matches = [
                    "action", "default", "dest",
                    "help", "required"
                ]
            else:
                matches = [
                    "action", "const", "default", "dest",
                    "help", "metavar", "nargs", "required", "type"
                ]

        if "name" in index:
            # args = [ f"'{ index }'" for index in value["name"] ]
            # for arg in args:
            #     params.append( arg )
            pass
        elif any( param in index for param in matches ):
            params |= inspect_parameter( index, value[ index ] )
        else:
            pass

    return [ value["name"], params ]

## ----------------------------------------------
def display_help(
        argparser: argparse.ArgumentParser=None
    ) -> bool:
    """
    Objective:  Displaying Help
    Parameters:
        argparser (argparse.ArgumentParser): Argument Parser
    Returns:    sys.exit( False )
    """

    toolset.trace_workflow( inspect.currentframe() )

    print()
    argparser.print_help()
    print()

    sys.exit( False )

## ------------------------------------------
def export_config(
        content: str = None,
        dataset: object = Any
    ) -> bool:
    """
    Objective:  Export Configuration
    Parameters:
        content (str): JSON Configuration
        dataset   (object): JSON Indent & Filepath
    Returns:    True (bool)
    """

    toolset.trace_workflow( inspect.currentframe() )

    # print( content )
    # print( dataset.path )

    filepath = os.path.join(
        dataset.path,
        f"{ dataset.name }.{ dataset.type }"
    )
    # print( filepath )

    if not os.path.exists( dataset.path ):
        toolset.display_message(
            heading = None,
            message = f"Creating Path: { dataset.path }"
        )
        try:
            os.makedirs(
                dataset.path,
                exist_ok = True
            )
        except OSError as error:
            # if error.errno != errno.EEXIST:
            print( f"OS Error: { error }" )
            raise

    try:
        if os.path.exists( filepath ):
            with open(
                filepath,
                "w",
                encoding = "utf8"
            ) as file:
                if dataset.type == 'json':
                    content = json.dumps(
                        content,
                        indent = dataset.indent
                    )
                    file.write( content )
                if dataset.type == 'yaml':
                    yaml.dump(
                        content,
                        file,
                        default_flow_style = False
                    )
            exported = "exported Configuration: { filepath }"
            if os.path.isfile( filepath ):
                # print( f"Located { exported }" )
                pass
            else:
                print( f"Missing { exported }" )
    except OSError as error:
        print( f"OS Error: { error }" )
        raise

    return True

## ----------------------------------------------
def extend_config(
        project: dict=None
    ) -> bool:
    """
    Objective:  Extending Script Configuration
    Parameters:
        project (dict): Project Configuration
    Returns:    bool (True)
    """

    toolset.trace_workflow( inspect.currentframe() )

    config["script"]["info"]["repo"] = __empty__

    package = config["script"]["package"]

    package["path"] = project["prjpath"]
    package["script"] = project["srcfile"]
    package["configs"] = project["configs"]

    package["abspath"] = project["abspath"]

    ## Loading Script Buckets (configs)
    config["script"]["buckets"] = load_buckets()

    config["script"]["exports"] = {
        "config": {
            "path": os.path.join(
                package["path"], "tests", "configs"
            ),
            "name": "project",
            "type": "json",
            "indent": 4
        },
        "docs": {
            "path": os.path.join(
                package["path"], "tests", "configs"
            ),
            "name": "buckets",
            "type": "json",
            "indent": 4
        }
    }

    config["script"]["options"] = __empty__

    config["script"]["features"] = {
        "required": [],
        "optional": [],
        "examples": []
    }

    config["script"]["input"] = {
            "args": {}
        }

    config["script"]["helper"] = {
        "formatter": "default",
        "headers": {
            "interview": "Please, answer the following questions"
        }
    }

    return True

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

    toolset.trace_workflow( inspect.currentframe() )

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
        spaces (int): JSON Configuration Indentation (default: 4)
    Returns:    False (bool) | json_config (str)
    """

    toolset.trace_workflow( inspect.currentframe() )

    if srcfile is not None:
        if os.path.exists( srcfile ):

            try:
                with open(
                    srcfile,
                    "r",
                    encoding='utf-8',
                    errors='ignore'
                ) as file:
                    data = json.load(
                        file,
                        strict = False
                    )
            except FileNotFoundError as ex:
                print( f"Warning Error: { ex }" )
                return False

            if isinstance( data, dict ):
                # toolset.display_message(
                #     heading = None,
                #     message = f"Loaded JSON Configuration\n{ srcfile }"
                # )
                json_config = json.dumps(
                    data,
                    indent = spaces
                )
                # print( json_config )
                return json_config

        else:
            toolset.display_warning(
                f"JSON Configuration { srcfile } does not exist!"
            )

    return False

## ----------------------------------------------
def inspect_parameter(
        index: str=None,
        target: str=None
    ) -> bool | dict:
    """
    Objective:  Inspect Parameter/Argument Value
    Parameters:
        index (str): Parameter/Argument Name
        content (str): Parameter/Argument Value
    Returns:    param (dict)
    """

    toolset.trace_workflow( inspect.currentframe() )

    ## Inspecting for regex in parameter value
    match = re.search(
        r'^(\{){2}(\ ?)(.*)(\}){2}$',
        str( target ).replace( " ", __empty__ )
    )

    ## Processing Pattern-Replacement
    if match:
        # print( target )
        pathway = match.group( 3 )
        # print( pathway )
        content = search_config(
            trgconf = config,
            target = target,
            pathway = pathway
        )
        # print( "value:", content )
    else:
        content = target

    ## Warning: Inspecting for malformed parameter value
    warning = f"Malformed Parameter: { index } = { content }"

    ## Sanitizing Malicioius Content
    response = True
    try:
        ## _ = ast.dump( ast.parse( f'"{ index }": "{ content }"' ) )
        parsed = ast.literal_eval( f"'{ content }'" )
        if not isinstance( parsed, str ):
            response = False
    except ( ValueError, SyntaxError ):
        update_config( config, content, __empty__ )
        content = __empty__
        response = False

    if response is False:
        toolset.display_warning( warning )

    param = { index: content }
    # print( f"Parameter: [ { param } ]" )

    return param

## ----------------------------------------------
def list_config(
        json_config: dict=None
    ) -> bool:
    """
    Objective:  Listing Script Configuration
    Parameters:
        json_config (dict): Script Configuration (default: None)
    Returns:    sys.exit()
    """

    toolset.trace_workflow( inspect.currentframe() )

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

    toolset.trace_workflow( inspect.currentframe() )

    return True

## ----------------------------------------------
def load_assets(
        srcfile: str="project.json",
        project: dict=None
    ) -> dict:
    """
    Objective:  Loading Custom Configuration
    Parameters:
        srcfile (str): JSON Configuration File (resource)
        project (dict): Project Configuration
    Returns:    True (bool)
    """

    toolset.trace_workflow( inspect.currentframe() )

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
    # print( f"load_assets -> Configuration: { source }" )

    ## Loading Default Configurations
    load_config(
        srcdict = config,
        srcfile = source,
        project = project["prjpath"]
    )

    ## Extending Script Basic Configuration
    extend_config( project = project )

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
                    toolset.display_warning(  message )
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

    toolset.trace_workflow( inspect.currentframe() )

    srcpath = os.path.dirname(
        os.path.dirname( os.path.abspath( __file__ ) )
    )
    srcfile = os.path.join(
        srcpath,
        "core",
        "configs",
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
        srcdict (dict): Source Dictionary (default: None)
        srcfile (str): JSON Configuration File (resource)
        project (str): Project Configuration (default: None)
        bucket (str): Bucket Configuration (default: None)
    Returns:    srcdict (dict)
    """

    toolset.trace_workflow( inspect.currentframe() )

    ## Aborting execution if srcfile is missing
    if srcfile is None:
        toolset.display_warning(  "Load Config - Missing Script Configuration!" )
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
                        script, _ = bucket.split( __dot__ )
                        srcdict[ script ][ _ ] = json.load( file )
                    else:
                        srcdict[ bucket ] = json.load( file )
                        # print( srcdict[bucket] )
            ## Appending file details
            filesize = toolset.get_filestat( confile )

        except FileNotFoundError as ex:
            toolset.display_warning(  f"{ message }\n{ ex }" )

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
                    script, _ = bucket.split( __dot__ )
                    srcdict[ script ][ _ ]["source"] = fileset
                else:
                    srcdict[ bucket ]['source'] = fileset
                    # print( srcdict[ bucket ]['source'] )

        except FileNotFoundError as ex:
            toolset.display_warning(  f"{ message }\n{ ex }" )

    else:
        toolset.display_warning(  f"{ message }" )

    return srcdict

## ----------------------------------------------
def load_project() -> dict:
    """
    Objective:  Configure Project Paths
    Parameters: None
    Returns:    project (dict)
    """

    toolset.trace_workflow( inspect.currentframe() )

    if repo is None:
        # toolset.display_warning(  "Unable to identify Git Repository" )
        gitrepo_dirname = os.path.basename( os.path.normpath(
            os.getcwd()
        ))
    else:
        gitrepo_dirname = os.path.basename( os.path.normpath(
            repo.working_tree_dir
        ))
    # print( f"\nload_script -> Project Git-Repo: { gitrepo_dirname }" )

    module_parent = os.path.dirname(
        os.path.dirname( os.path.abspath( __file__ ) )
    )

    if repo is None:
        abspath = os.getcwd()
    else:
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
        srcfile (str): Script Configuration File (resource)
        json_config (dict): Script Configuration (default: None)
    Returns:   List [ input_parser, input_args, rouge_args, config ]
    """

    toolset.trace_workflow( inspect.currentframe() )

    ## Loading Custom Configurations
    if json_config is not None:
        toolset.display_warning(  "Missing Load-Script JSON Configuration!" )
        # config = json_config

    ## Aborting execution if srcfile is missing
    if srcfile is None:
        toolset.display_warning(  "Load Script - Missing Script Configuration!" )
        return False

    project = load_project()
    project["srcfile"] = srcfile
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

    ## Git Repository Configuration
    configure_gitrepo()

    ## Configure User-Input Parser
    parser = {
        "package": config["script"]["package"],
        "formatter": config["script"]["helper"]["formatter"],
        "options": config["script"]["options"]
    }

    _ = core_parser.user_input( input_config = parser )
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
        character (str): Divisor Character (default: '-')
        length (int): Divisor Length (default: 80)
    Returns:    True (bool)
    """

    toolset.trace_workflow( inspect.currentframe() )

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

    toolset.trace_workflow( inspect.currentframe() )

    parent = os.path.abspath(
        os.path.dirname( os.path.dirname( __file__ ) )
    )
    with codecs.open( os.path.join( parent, config_file ), 'r') as file_pointer:
        return file_pointer.read()

## ----------------------------------------------
def search_config(
        trgconf: dict=None,
        target: str=None,
        pathway: str=None
    ) -> str:
    """
    Objective:  Search Dict-Key Pathway
    Parameters:
        trgconf (dict): Target Configuration
        target (str): Search Content
        pathway (str): Pathway to target configuration
    Returns:    content (str)
    """

    content = __empty__
    pathset = pathway.split( __dot__ )
    # print( pathway, pathset )

    if trgconf is not None:
        content = None
        for item in pathset:
            for key, value in trgconf.items():
                if key == item:
                    content = value
                    trgconf = trgconf[ key ]
                    break

        ## Search & Replace: content -> target
        update_config( config, target, content )

    return content

## ----------------------------------------------
def update_config(
        trgconf: dict=None,
        target: str=None,
        replace: str=None,
    ):
    """
    Objective:  Update Configuration (Dict-Key)
    Parameters:
        trgconf (dict): Target Configuration
        target (str): Search Content
        replace (str): Replace Content
    Returns:    None
    """

    for key, value in trgconf.items():
        if value == target:
            trgconf[ key ] = replace
        elif isinstance( value, list ):
            for item in value:
                if isinstance( item, dict ):
                    update_config( item, target, replace )
        if isinstance( value, dict ):
            update_config( value, target, replace )

    return True
