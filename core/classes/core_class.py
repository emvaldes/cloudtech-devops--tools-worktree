""" Core Module: Classes """

import sys
import inspect

from typing import Any

## Importing Core Classes:
from core.classes.json_class import JsonObject

## Importing Core Modules:
from core import core_toolset as toolset

# locale.setlocale( locale.LC_ALL, 'us_US' )

## Global Variables:

## ----------------------------------------------
class CoreClass:
    """
    Objective:  Construct Core Class
    Parameters: None
    Returns:    None
    """

    ## Configuration items
    json = None
    config = None

    ## Script Interface
    input = None
    output = None

    ## Script Structure
    buckets = None

    ## Empty string
    __empty__ = ''

    ## Space string
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

        toolset.trace_workflow( inspect.currentframe() )

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

        toolset.trace_workflow( inspect.currentframe() )

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

        toolset.trace_workflow( inspect.currentframe() )

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

        toolset.trace_workflow( inspect.currentframe() )

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

        toolset.trace_workflow( inspect.currentframe() )

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

        toolset.trace_workflow( inspect.currentframe() )

        # print( 'app - getting attribute' )
        return super().__getattribute__( key )

    ## ------------------------------------------
    def has( self, key: str ) -> bool:
        """ Check if attribute exists """

        toolset.trace_workflow( inspect.currentframe() )

        return hasattr( self, key )

    ## ------------------------------------------
    def set( self, key: str, value: Any ) -> None:
        """ Set attribute """

        toolset.trace_workflow( inspect.currentframe() )

        # print( 'app - setting attribute' )
        super().__setattr__( key, value )
        return super().__getattribute__( key )

    ## Dictionary Methods

    ## ------------------------------------------
    def add_key_dict( self, key: str, value: Any ) -> None:
        """ Add item to dictionary """

        toolset.trace_workflow( inspect.currentframe() )

        # print( 'app - adding dict-keys' )
        self.__dict__[ key ] = value
        return self.__dict__[ key ]

    ## ------------------------------------------
    def get_key_dict( self, key: str ) -> Any:
        """ Get item from dictionary """

        toolset.trace_workflow( inspect.currentframe() )

        # print( 'app - getting dict-keys' )
        return self.__dict__[ key ]

    ## ------------------------------------------
    def get_all_dict( self ) -> dict:
        """ Return dictionary of all attributes """

        toolset.trace_workflow( inspect.currentframe() )

        # print( 'app - getting all-dict-keys' )
        return self.__dict__
