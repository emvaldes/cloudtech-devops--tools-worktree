""" Core Module: Classes """

import os
import sys

import errno
# import locale

from typing import Any

import json
# from pprint import pprint

import hashlib
import datetime

import humanize

# locale.setlocale( locale.LC_ALL, 'us_US' )

## ----------------------------------------------
class JsonObject:
    """
    Objective: Convert JSON to Object
    Reference: https://stackoverflow.com/a/66054047
    """

    ## ------------------------------------------
    def __init__(
            self,
            data=None
        ) -> None:
        """
        Objective:  Initialize Object variables
        Parameters:
            data (dict): JSON data
        Returns:    None
        """

        if data is None:
            data = {}
        else:
            data = dict( data )
        for key, val in data.items():
            setattr( self, key, self.set_value( val ) )

    ## ------------------------------------------
    def export_config(
            self,
            json_data: str=None,
            dataset: object=Any
        ) -> bool:
        """
        Objective:  Export Configuration
        Parameters: 
            json_data   (dict): JSON data
            dataset   (object): JSON Indent & Filepath
        Returns:    True (bool)
        """

        json_object = json.dumps(
            json_data,
            indent = dataset.config.indent
        )
        # print( json_object )
        # print( dataset.config.path )

        filepath = dataset.config.path
        # print( filepath )
        try:
            with open(
                    filepath,
                    "w",
                    encoding = "utf8"
                ) as json_file:
                json_file.write( json_object )
                if os.path.exists( filepath ):
                    # print( "Located exported JSON Configuration" )
                    pass
                else:
                    print( "Missing exported JSON Configuration" )

        except OSError as error:
            print( f"OS Error: { error }" )
            raise

        return True

    ## ------------------------------------------
    def set_value(
            self,
            value: Any
        ) -> Any | list | tuple | dict:
        """
        Objective:  Configure Attributes
        Parameters:
            value attribute (object)
        Returns:    value attribute (object) | list | tuple | dict
        """

        if isinstance( value, list ):
            return [ self.set_value( x ) for x in value ]

        if isinstance( value, tuple ):
            return tuple( self.set_value( x ) for x in value )

        if isinstance( value, dict ):
            return JsonObject( value )

        return value

    ## Attribute Methods

    ## ------------------------------------------
    def delete( self, key: str ) -> None:
        """ Delete attribute """
        # print( 'app - deletting attribute' )
        super().__delattr__( key )
        return super().__getattribute__( key )

    ## List Methods

    ## ------------------------------------------
    def keys_list( self ) -> list:
        """ Return list of keys """
        # print( 'app - listing keys' )
        return list( self.__dict__.keys() )

    ## ------------------------------------------
    def values_list( self ) -> list:
        """ Return list of values """
        # print( 'app - listing values' )
        return list( self.__dict__.values() )

    ## ------------------------------------------
    def items_list( self ) -> list:
        """ Return list of items """
        # print( 'app - listing items' )
        return list( self.__dict__.items() )

    ## Dictionary Methods

    ## ------------------------------------------
    def set_key_dict( self, key: str, value: Any ) -> None:
        """ Set item in dictionary """
        # print( 'app - setting dict-keys' )
        self.__dict__[ key ] = value
        return self.__dict__[ key ]

    ## ------------------------------------------
    def len_dict( self ) -> int:
        """ Return length of dictionary """
        # print( 'app - sizing dict-keys' )
        return len( self.__dict__ )

    ## ------------------------------------------
    def iter_dict( self ) -> iter:
        """ Return iterator """
        # print( 'app - iterating dict-keys' )
        return iter( self.__dict__ )

## ----------------------------------------------
class CoreClass:
    """
    Objective:  Construct Core Class
    Parameters: None
    Returns:    None
    """

    ## Empty string
    empty = ''

    ## Configuration items
    json = None
    config = None

    ## Script Interface
    input = None
    output = None

    ## Script Structure
    buckets = None

    __empty__ = ''
    __space__ = ' '

    ## ------------------------------------------
    def __init__(
            self,
            json_object: dict=None
        ) -> None:
        """
        Objective:  Initialize Class variables
        Parameters:
            json_object (dict) -> None
        Returns:    None
        """

        if json_object is not None:
            if self.json is None:
                self.json = json_object
        else:
            self.missing_config( "CoreClass" )

        if isinstance( self.config, type( None ) ):
            ## Initializing CoreClass
            self.config = JsonObject( self.json )

        if self.config is not None:
            ## Parsing items: script, project, dataset, ...
            indexes = self.config.items_list()

            ## Inspecting Key/Pair Values
            for key, value in indexes:

                ## Initializing: self.[key]
                if not self.has( key ):
                    self.add_key_dict( key, value )

        ## Records items
        self.records = {}

    ## ------------------------------------------
    def missing_config(
            self,
            warning: str=None,
            status: str="JSON Configuration was not found!"
        ) -> None:
        """
        Objective:  Missing Configuration
        Parameters:
            warning (str): Warning message
            status  (str): Status message
        Returns:    sys.exit( warning )
        """

        sys.exit( f"{ warning } { status }" )

    ## Custom Methods

    ## ------------------------------------------
    def get_record(
            self: Any,
            obj: object=Any,
            index: str=None,
            packed: bool=False
        ) -> list | JsonObject:
        """
        Objective:  Returns record by key
        Parameters:
            obj    (object): Any Object
            index     (str): Index
            packed   (bool): Return dictionary
        Returns:    record (List or JsonObject)
        """

        record = None
        ## Comprenhension list cycles through all items
        # record = [ item for item in obj if item.id == index ][0]
        if index is not None:
            if isinstance( obj, list ):
                for item in obj:
                    if isinstance( item, dict ):
                        for key, value in item.items():
                            if key == index:
                                record = { key: value }
                                break
                    if isinstance( item, JsonObject ):
                        key, value = list( item.__dict__.values() )
                        if key == index:
                            record = value
                            break
            if isinstance( obj, JsonObject ):
                if packed is False:
                    record = obj.get_key_dict( index )
                else:
                    record = obj.get_all_dict()

        return record

    ## ------------------------------------------
    def get_value(
            self: Any,
            obj: object=Any,
            index: str=None
        ) -> str | None:
        """
        Objective:  Getting Value by Key
        Parameters:
            obj   (object): Any Object
            index    (str): Index
        Returns:    value (str) | None
        """

        if index is not None:
            if isinstance( obj, dict ):
                value = obj[ index ]
            if isinstance( obj, list ):
                for item in obj:
                    if isinstance( item, dict ):
                        for key, value in item.items():
                            if key == index:
                                return value
                    if isinstance( item, JsonObject ):
                        key, value = list( item.__dict__.values() )
                        if key == index:
                            return value
            if isinstance( obj, JsonObject ):
                value = self.get_record( obj, index )
                return value

        return None

    ## ------------------------------------------
    def set_value(
            self: Any,
            obj: list,
            index: str=None
        ) -> str | None:
        """
        Objective:  Set Object Property
        Parameters:
            obj   (object): Any Object
            index    (str): Index
        Returns:    value (str) | None
        """

        if index is not None:
            for item in obj:
                key, value = list( item.__dict__.values() )
                # print( key, value )
                if key == index:
                    self.set( key, value )
                    break
                # print( key, value )
                return value

        return None

    ## Attribute Methods

    ## ------------------------------------------
    def get( self, key: str ) -> Any:
        """ Get attribute """
        # print( 'app - getting attribute' )
        return super().__getattribute__( key )

    ## ------------------------------------------
    def has( self, key: str ) -> bool:
        """ Check if attribute exists """
        return hasattr( self, key )

    ## ------------------------------------------
    def set( self, key: str, value: Any ) -> None:
        """ Set attribute """
        # print( 'app - setting attribute' )
        super().__setattr__( key, value )
        return super().__getattribute__( key )

    ## Dictionary Methods

    ## ------------------------------------------
    def add_key_dict( self, key: str, value: Any ) -> None:
        """ Add item to dictionary """
        # print( 'app - adding dict-keys' )
        self.__dict__[ key ] = value
        return self.__dict__[ key ]

    ## ------------------------------------------
    def get_key_dict( self, key: str ) -> Any:
        """ Get item from dictionary """
        # print( 'app - getting dict-keys' )
        return self.__dict__[ key ]

    ## ------------------------------------------
    def get_all_dict( self ) -> dict:
        """ Return dictionary of all attributes """
        # print( 'app - getting all-dict-keys' )
        return self.__dict__

## ----------------------------------------------
class HelperClass( CoreClass ):
    """
    Objective:  Construct Helper Class
    Parameters:
        CoreClass (object)
    Returns:    None
    """

    ## ------------------------------------------
    def __init__(
            self,
            json_object: dict=None
        ) -> None:
        """
        Objective:  Initialize Script Helper
        Parameters:
            json_object (dict) -> None
        Returns:    None
        """

        if json_object is not None:
            self.json = json_object
        else:
            super().missing_config(
                warning = "Script Helper"
            )

        ## Initialize CoreClass
        super().__init__( json_object )

## ----------------------------------------------
class BucketsClass( CoreClass ):
    """
    Objective:  Construct Bucket Class (dirs, files, docs)
    Parameters:
        CoreClass (object)
    Returns:    None
    """

    ## ------------------------------------------
    def __init__(
            self,
            json_object: dict=None
        ) -> None:
        """
        Objective:  Initialize Script Buckets
        Parameters:
            json_object (dict) -> None
        Returns:    None
        """

        if json_object is not None:
            self.json = json_object
        else:
            super().missing_config(
                warning = "Script Buckets"
            )

        ## Initialize CoreClass
        super().__init__( json_object )

        ## Identify if project is available
        if self.has( 'project' ):
            ## Fetching self.project's keys
            keys = list( self.project.__dict__.keys() )
            ## Parsing: self.project( buckets, source, etc. )
            for key in keys:
                if key == 'buckets':
                    ## Inquiring if self.buckets is a JsonObject
                    if isinstance( self.buckets, JsonObject ):
                        ## Configure Script Helper Objects
                        self.setup_buckets()
                    else:
                        ## Initialize self.buckets JsonObject
                        self.add_key_dict(
                            key,
                            self.project.buckets
                        )
                    break

    ## ------------------------------------------
    def setup_buckets( self ) -> bool:
        """
        Objective:  Setup Buckets (dirs, files, docs)
        Parameters: None
        Returns:    True (bool)
        """

        if self.buckets is not None:

            package = self.script.package
            pkgpath = package.abspath

            ## Dictionary Objects:
            targets = [
                self.json["script"]["buckets"],
                self.json["project"]["buckets"]
            ]
            for buckets in targets:
                # buckets = self.json["project"]["buckets"]
                for listing in buckets:
                    # print( f"\nType: { listing } -> { type( listing ) }" )
                    if isinstance( buckets[listing], list ):
                        if listing in [ "dirs", "files" ]:
                            # print( f"List: { buckets[listing] }" )
                            # print( f"Type: { type( buckets[listing] ) }" )
                            ## Create Bucket Dirs
                            if listing == "dirs":
                                self.load_buckets(
                                    listing,
                                    buckets[listing],
                                    pkgpath
                                )
                            ## Create Bucket Files
                            if listing == "files":
                                self.load_buckets(
                                    listing,
                                    [{ "docs": buckets[listing] }],
                                    pkgpath
                                )
                ## Update Buckets Configuration
                self.update_buckets(
                    dictobj = buckets,
                    tracker = self.empty,
                    abspath = package.abspath
                )

        return True

    ## ------------------------------------------
    def load_buckets(
            self,
            bucket_type: str=None,
            bucket_conf: dict=None,
            bucket_path: str=None,
            create: bool=False
        ) -> bool:
        """
        Objective:  Construct Bucket (dirs, files, docs)
        Parameters:
            bucket_type  (str): Bucket type (dirs, files, docs)
            bucket_conf (dict): Bucket configuration
            bucket_path  (str): Bucket path
            create      (bool): Create bucket
        Returns:    True (bool)
        """

        if bucket_conf is not None:

            ## Execute if bucket_path is setup
            if create:

                self.create_buckets(
                    bucket_path,
                    bucket_type
                )

            ## Processing all list-based items
            if isinstance( bucket_conf, list ):
                ## e.g.: [{ 'id': 'pseudo', 'name': 'pseudo', ... }] (<class 'list'>)
                for records in bucket_conf:
                    ## e.g.: { 'id': 'pseudo', 'name': 'pseudo', ... } (<class 'dict'>)
                    for record in records.items():
                        ## e.g.: id (<class 'str'>) -> pseudo (<class 'str'>)
                        key, value = record
                        ## Identify if records[ "name" ] exists
                        if 'name' in records.keys():
                            folder = records[ "name" ]
                        else:
                            folder = self.empty
                        create = True
                        ## Predefine buckets dataset
                        dataset = [
                            key,
                            value,
                            os.path.join(
                                bucket_path,
                                folder
                            ),
                            create
                        ]
                        if key == 'dirs':
                            ## Create Bucket Folders
                            self.load_buckets( *dataset )
                        elif key == 'files':
                            for item in value:
                                filename = f"{ item['name'] }.{ item['type'] }"
                                ## Customize bucket-files dataset
                                dataset[2] = os.path.join(
                                    bucket_path,
                                    folder,
                                    filename
                                )
                                self.load_buckets( *dataset )
                        elif key == 'docs':
                            for item in value:
                                filename = f"{ item['name'] }.{ item['type'] }"
                                ## Customize bucket-docs dataset
                                dataset[2] = os.path.join(
                                    bucket_path,
                                    filename
                                )
                                self.load_buckets( *dataset )
                        else:
                            pass

        return True

    ## ------------------------------------------
    def create_buckets(
            self,
            bucket_path: str=None,
            bucket_type: str=None,
            verbose: bool=False
        ) -> bool | int:
        """
        Objective:  Create/Initialize (dirs, files, docs)
        Parameters:
            bucket_path  (str): Bucket path
            bucket_type  (str): Bucket type (dirs, files, docs)
            verbose     (bool): Verbose output
        Returns:    True (bool) | bucket_size (int)
        """

        bucket_size = 0
        exception = None
        status = False
        try:
            if bucket_type == 'dirs':
                if not os.path.isdir( bucket_path ):
                    if verbose:
                        print( f"Create Folder: { bucket_path }" )
                    try:
                        os.makedirs(
                            bucket_path,
                            exist_ok=False
                        )
                        status = True
                    except OSError as error:
                        exception = error
                        status = False
                        raise
                else:
                    if verbose:
                        print( f"Folder already exists: { bucket_path }" )
                    status = False
                for ele in os.scandir( bucket_path ):
                    bucket_size += os.stat( ele ).st_size
            if bucket_type in [ 'files', 'docs' ]:
                if not os.path.isfile( bucket_path ):
                    if verbose:
                        print( f"Create File: { bucket_path }" )
                    try:
                        with open(
                                bucket_path,
                                "w",
                                encoding = "utf8"
                            ) as file:
                            file.write( "" )
                        status = True
                    except OSError as error:
                        exception = error
                        status = False
                        raise
                else:
                    if verbose:
                        print( f"File already exists: { bucket_path }" )
                    status = False
                bucket_size = os.stat( bucket_path ).st_size
        except OSError as error:
            exception = error
            raise
        if exception is not None:
            if exception.errno != errno.EEXIST:
                if verbose:
                    print( f"OS error: { exception.errno } occurred." )
            status = False

        return [ bucket_size, status ]

    ## ------------------------------------------
    def update_buckets(
            self,
            dictobj: dict=None,
            tracker: str=None,
            abspath: str=None
        ) -> bool:
        """
        Objective:  Update Buckets (dirs, files, docs)
        Parameters:
            dictobj (dict): Dictionary object
            tracker  (str): Tracking path
            abspath  (str): Absolute path
        Returns:    True (bool)
        """

        if isinstance( dictobj, dict ):

            create = None
            # print( f"{ dictobj }" )

            if "type" in dictobj.keys():
                create = 'files'
            else:
                create = 'dirs'

            for key, value in dictobj.items():

                if key == "name":
                    tracker += f"/{ value }"
                    if create == 'files':
                        tracker += f".{ dictobj['type'] }"
                    # print( f"{ tracker }" )
                elif key == "size":
                    filepath = f"{ abspath }{ tracker }"
                    natural_size = humanize.naturalsize(
                        os.stat( filepath ).st_size
                    )
                    dictobj["size"] = natural_size
                elif key == "hash":
                    with open(
                        filepath,
                        "rb"
                    ) as rbinary:
                        filehash = hashlib.md5(
                            rbinary.read()
                        ).hexdigest()
                    dictobj["hash"] = filehash
                elif key == "date":
                    filedate = datetime.datetime.fromtimestamp(
                        os.path.getmtime( filepath )
                    )
                    dictobj["date"] = str( filedate )
                elif key in [ "id", "type" ]:
                    pass
                elif key in ["dirs", "files", "docs" ]:
                    pass
                else:
                    pass

                if isinstance( value, dict ):
                    self.update_buckets( value, tracker, abspath )

                elif isinstance( value, list ):
                    for item in value:
                        self.update_buckets( item, tracker, abspath )
                else:
                    pass

        return True

## ----------------------------------------------
class ConfigClass(
        HelperClass,
        BucketsClass
    ):
    """
    Objective:  Construct Multiple-Inheritance
    Parameters:
        HelperClass (object)
        BucketsClass (object)
    Returns:    None
    """

    ## ------------------------------------------
    def __init__(
            self,
            json_object: dict=None
        ) -> None:
        """
        Objective:  Initialize Class variables
        Parameters:
            json_object (dict) -> None
        Returns:    None
        """

        if json_object is not None:
            self.json = json_object
        else:
            super().missing_config(
                warning = "Script Filters"
            )

        if json_object["script"]:
            ## Initializing HelperClass Object
            HelperClass.__init__( self, json_object )

        if json_object["project"]["buckets"]:
            ## Initializing BucketsClass Object
            BucketsClass.__init__( self, json_object )

class AppConfig( ConfigClass ):
    """
    Objective:  Construct AppConfig Class
    Parameters: ConfigClass (core_classes.ConfigClass)
    Returns:    None
    """

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

        ## Export Configuration
        self.export_project()

    ## ------------------------------------------
    def export_project(
            self
        ) -> bool:
        """
        Objective:  Export Project Configurations
        Parameters: None
        Returns:    bool (True)
        """

        ## Extracting Package (abspath, configs)
        options = list(
            self.json["script"]["package"].values()
        )
        # print( "options:", options )

        filename, abspath = [
            options[ index ] for index in ( 3, 6 )
        ]
        # print( "picked:", abspath, filename )

        filename = os.path.splitext(
            os.path.basename( filename )
        )[0]
        # print( "filename:", filename )

        # f"{ filename }.json"
        config_path = os.path.join(
            abspath,
            "exports",
            "config",
            "project.json"
        )
        self.script.exports.config.path = config_path

        ## Purging abspath from JSON object
        del self.json["script"]["package"]["abspath"]
        # print( self.json )

        ## Export Configuration
        self.config.export_config(
            self.json,
            self.script.exports
        )

        return True
