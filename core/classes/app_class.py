""" Core Class: AppConfig """

import os
import inspect

## Import Core Classes:
from core.classes.config_class import ConfigClass
from core.modules.storage.sharepoint import SharePoint

## Import Core Modules:
from core import core_module
from core import core_toolset as toolset

## ----------------------------------------------
class AppConfig( ConfigClass ):
    """
    Objective:  Construct AppConfig Class
    Parameters: ConfigClass (core.classes.ConfigClass)
    Returns:    None
    """

    ## Class Variables:

    trg_path = None
    args = None
    storage = None

    ## ------------------------------------------
    def __init__(
            self,
            json_object: dict = None,
            trg_path: str = os.getcwd()
        ) -> None:
        """
        Objective:  Initialize Class variables
        Parameters:
            json_object (dict) -> None
            trg_path (str) -> os.getcwd()
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        if json_object is not None:
            if self.json is None:
                self.json = json_object
        else:
            super().missing_config(
                warning = "AppConfig"
            )

        ## Execution Original Path
        self.trg_path = trg_path

        super().__init__( json_object )

        self.args = self.script.input.args

        if self.args.enable is not None:

            module = "sharepoint"
            if module in self.args.enable:
                # if self.args.verbose:
                #     print( f"\nEnabling { module } module ..." )
                self.storage = SharePoint(
                    trg_path = self.trg_path,
                    args = self.args,
                    storage = self.json["storage"][ module ]
                )

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

        toolset.trace_workflow( inspect.currentframe() )

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

        ## Deprecated but valuable for future consideration
        # pkg_name = self.json["script"]["package"]["name"]
        # filename = f"{ pkg_name }-{ filename }"

        # print( "filename:", filename )
        # f"{ filename }.json"

        ## Purging abspath from JSON object
        del self.json["script"]["package"]["abspath"]
        # print( self.json )

        file_types = [ "json", "yaml" ]
        default_format = "json"

        file_format = self.args.format
        if file_format not in file_types:
            file_format = default_format

        ## Exporting Buckets Configurations
        if len( self.json["script"]["buckets"]["dirs"] ) > 0:
            buckets_json = self.json["script"]["buckets"]["dirs"][0]
            for file_type in file_types:
                if file_type in file_format:

                    dataset = self.script.exports.docs
                    dataset.path = os.path.join(
                        abspath,
                        dataset.path
                    )
                    dataset.type = file_type

                    if not os.path.isfile( dataset.path ):
                        ## Export Configuration (JSON, YAML)
                        core_module.export_config(
                            buckets_json,
                            dataset
                        )
            ## Removing buckets.docs from JSON object
            del self.json["script"]["buckets"]["dirs"][0]

        ## Purging Options-stats from JSON object
        if "source" in self.json["script"]["options"]:
            del self.json["script"]["options"]["source"]

        ## Exporting Project Configurations
        for file_type in file_types:
            if file_type in file_format:
                dataset = self.script.exports.config
                dataset.path = os.path.join(
                    abspath,
                    dataset.path
                )
                dataset.type = file_type

                if not os.path.isfile( dataset.path ):
                    ## Export Configuration (JSON, YAML)
                    core_module.export_config(
                        self.json,
                        dataset
                    )

        ## Enforcing Configs default-setting to JSON
        self.script.exports.config.type = default_format

        return True
