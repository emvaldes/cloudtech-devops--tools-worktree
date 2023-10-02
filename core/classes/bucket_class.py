""" Core Class: Bucket Class """

import os
import errno
import inspect
import hashlib
import datetime
import humanize

## Importing Core Classses:
from core.classes.json_class import JsonObject
from core.classes.core_class import CoreClass

## Importing Core Modules:
from core import core_toolset as toolset

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

        toolset.trace_workflow( inspect.currentframe() )

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

        toolset.trace_workflow( inspect.currentframe() )

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
                                    [{ "docs": buckets[ listing ] }],
                                    pkgpath
                                )
                ## Update Buckets Configuration
                self.update_buckets(
                    dictobj = buckets,
                    tracker = self.__empty__,
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

        toolset.trace_workflow( inspect.currentframe() )

        if bucket_conf is not None:

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
                            folder = self.__empty__
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
                            # for item in value:
                            #     if "create" in item:
                            #         if item["create"] is False:
                            #             create = item["create"]
                            #             dataset[3] = item["create"]
                            #             # toolset.print_json( dataset )
                            # if create:
                            #     ## Create Bucket Folders
                            #     self.load_buckets( *dataset )
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
                                if "create" in item:
                                    if item["create"] is False:
                                        create = item["create"]
                                        dataset[3] = item["create"]
                                        # toolset.print_json( dataset )
                                else:
                                    self.load_buckets( *dataset )
                        elif key == 'docs':
                            for item in value:
                                filename = f"{ item['name'] }.{ item['type'] }"
                                ## Customize bucket-docs dataset
                                dataset[2] = os.path.join(
                                    bucket_path,
                                    filename
                                )
                                if "create" in item:
                                    if item["create"] is False:
                                        create = item["create"]
                                        dataset[3] = item["create"]
                                        # toolset.print_json( dataset )
                                else:
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

        toolset.trace_workflow( inspect.currentframe() )

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
                            file.write( self.__empty__ )
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

        toolset.trace_workflow( inspect.currentframe() )

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
                    if os.path.isfile( filepath ):
                        natural_size = humanize.naturalsize(
                            os.stat( filepath ).st_size
                        )
                        dictobj["size"] = natural_size
                elif key == "hash":
                    if os.path.isfile( filepath ):
                        try:
                            with open(
                                filepath,
                                "rb"
                            ) as rbinary:
                                filehash = hashlib.md5(
                                    rbinary.read()
                                ).hexdigest()
                            dictobj["hash"] = filehash
                        except OSError as error:
                            print( f"OS error: { error.errno } occurred." )
                elif key == "date":
                    if os.path.isfile( filepath ):
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
