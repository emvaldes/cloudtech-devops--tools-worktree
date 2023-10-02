""" Core JsonObject Class """

from typing import Any

import inspect

## Import Core Modules:
from core import core_toolset as toolset

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

        toolset.trace_workflow( inspect.currentframe() )

        if data is None:
            data = {}
        else:
            data = dict( data )
        for key, val in data.items():
            setattr( self, key, self.set_value( val ) )

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

        toolset.trace_workflow( inspect.currentframe() )

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

        toolset.trace_workflow( inspect.currentframe() )

        # print( 'app - deletting attribute' )
        super().__delattr__( key )
        return super().__getattribute__( key )

    ## List Methods

    ## ------------------------------------------
    def keys_list( self ) -> list:
        """ Return list of keys """

        toolset.trace_workflow( inspect.currentframe() )

        # print( 'app - listing keys' )
        return list( self.__dict__.keys() )

    ## ------------------------------------------
    def values_list( self ) -> list:
        """ Return list of values """

        toolset.trace_workflow( inspect.currentframe() )

        # print( 'app - listing values' )
        return list( self.__dict__.values() )

    ## ------------------------------------------
    def items_list( self ) -> list:
        """ Return list of items """

        toolset.trace_workflow( inspect.currentframe() )

        # print( 'app - listing items' )
        return list( self.__dict__.items() )

    ## Dictionary Methods

    ## ------------------------------------------
    def set_key_dict( self, key: str, value: Any ) -> None:
        """ Set item in dictionary """

        toolset.trace_workflow( inspect.currentframe() )

        # print( 'app - setting dict-keys' )
        self.__dict__[ key ] = value
        return self.__dict__[ key ]

    ## ------------------------------------------
    def len_dict( self ) -> int:
        """ Return length of dictionary """

        toolset.trace_workflow( inspect.currentframe() )

        # print( 'app - sizing dict-keys' )
        return len( self.__dict__ )

    ## ------------------------------------------
    def iter_dict( self ) -> iter:
        """ Return iterator """

        toolset.trace_workflow( inspect.currentframe() )

        # print( 'app - iterating dict-keys' )
        return iter( self.__dict__ )
