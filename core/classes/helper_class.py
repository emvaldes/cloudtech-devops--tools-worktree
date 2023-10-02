""" Core Class: Helper Class """

import inspect

## Importing Core Classses:
from core.classes.core_class import CoreClass

## Importing Core Modules:
from core import core_toolset as toolset

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

        toolset.trace_workflow( inspect.currentframe() )

        if json_object is not None:
            self.json = json_object
        else:
            super().missing_config(
                warning = "Script Helper"
            )

        ## Initialize CoreClass
        super().__init__( json_object )
