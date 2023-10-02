""" Core Class: ConfigClass """

import inspect

## Importing Core Classses:
from core.classes.helper_class import HelperClass
from core.classes.bucket_class import BucketsClass

## Importing Core Modules:
from core import core_toolset as toolset

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

        toolset.trace_workflow( inspect.currentframe() )

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
