""" Core Class: SharePoint """

import os
import sys

# import re
import inspect

from typing import Any

import time
import json
import base64

import requests
import maskpass

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

## Import Core Modules:
from core import core_parser
from core import core_toolset as toolset

## ----------------------------------------------
class SharePoint:
    """
    Objective:  Construct SharePoint Class
    Parameters: ConfigClass (core.classes.ConfigClass)
    Returns:    None
    """

    ## Class Variables:

    __empty__ = ''
    __space__ = ' '
    __tab__ = '\t'

    trg_path = None
    args = None
    storage = None

    login = None

    locations = None
    credentials = None

    import_latest = "latest"
    import_everything = "all"

    importing = {
        "local": None,
        "remote": None,
        "action": None
    }

    exporting = {
        "local": None,
        "remote": None,
        "action": None,
        "archive": None
    }

    archive_folder = {}

    already = {
        "exported": [],
        "archived": []
    }

    access = {
        "fernet": None,
        "hash": None,
        "keyset": None,
        "phrase": None
    }

    graph = {
        "domain": None,
        "sites": None,
        "version": None
    }

    sharepoint = {
        "config": None,
        "filepath": None
    }

    profile = {
        "credentials": {
            "client_id": "",
            "tenant_id": "",
            "secret": {
                "secret_id": "",
                "secret_value": "",
                "secret_ttl": ""
            },
            "token": {
                "token_value": "",
                "token_ttl": ""
            },
            "site_id": "",
            "drive_id": ""
        },
        "locations": None
    }

    ## REST API Status Codes
    ## 1xx Status Codes [Informational]
    ## 2xx Status Codes [Success]
    ## 3xx Status Codes [Redirection]
    ## 4xx Status Codes (Client Error)
    ## 5xx Status Codes (Server Error)

    status_code = {
        "200": "Indicates that the request has succeeded.",
        "201": "The request's new resource has been created.",
        "202": "The request has been accepted for processing.",
        "409": "Unable to create or update an existing resource."
    }

    ## ------------------------------------------
    def __init__(
            self,
            trg_path: str = os.getcwd(),
            args: Any = None,
            storage: dict = None
        ) -> None:
        """
        Objective:  Initialize Class variables
        Parameters:
            trg_path (str): Target path (default: os.getcwd())
            args (Any): User-Input arguments (default: None)
            storage (dict): User-Input JSON Configuration (default: None)
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        if trg_path is None:
            trg_path = os.getcwd()
        self.trg_path = trg_path

        self.args = args
        self.storage = storage

        self.profile["locations"] = self.storage

        ## Configure Environment
        self.configure_environment()

        ## Provisioning SharePoint profile
        self.provision_profile()

        if self.access["keyset"] is None:
            self.request_passphrase()
        else:
            self.access["fernet"] = Fernet( self.access["keyset"] )

        if self.args.display is not None:
            if "config" in self.args.display:
                toolset.print_json( content = self.profile )

        ## Exporting SharePoint profile
        self.export_profile()

    ## ------------------------------------------
    def archive_item(
            self,
            target_item: dict = None
        ) -> None:
        """
        Objective:  Archive item to another location
        Parameters:
            target_item => Target item to archive (dict)
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        file_name, file_type = os.path.splitext(
            target_item["target"]
        )

        # ## Configure SharePoint Already-Archive
        # self.already["archived"] = self.list_files(
        #     self.exporting["archive"],
        #     None
        # )

        for exported in self.already["exported"]:
            if exported["target"] == target_item["target"]:
                target_item = exported
                listing = []
                for archived in self.already["archived"]:
                    # message = f"Found match: { archived['name'] }"
                    if archived["name"].startswith( file_name ):
                        # if self.args.debug:
                        #     toolset.display_warning(
                        #         message = message
                        #     )
                        listing.append( archived["name"] )
                if listing:
                    target_file = [ max( listing ) ]
                    archive_filename = toolset.name_iterator(
                        location = target_file,
                        file_name = file_name,
                        file_type = file_type,
                        indexing = True
                    )
                else:
                    archive_filename = "".join([
                        f"{ file_name }" + 
                        f"-{ toolset.datestamp }-000" +
                        f"{ file_type }"
                    ])
                if self.args.debug:
                    toolset.display_message(
                        heading = None,
                        message = f"\nArchive Filename: { archive_filename }"
                    )
                ## Copying Exported file into Archives folder
                if self.archive_folder["id"] is not None:
                    self.copy_item(
                        source_item = exported["id"],
                        target_folder = self.archive_folder["id"],
                        target_name = archive_filename
                    )

        return True

    ## ------------------------------------------
    def configure_environment( self ) -> None:
        """
        Objective:  Configure Environment
        Parameters: None
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        self.sharepoint["config"] = "sharepoint.json"
        ## Addressing duplicity in path configuration
        self.sharepoint["filepath"] = os.path.join(
            self.trg_path,
            self.sharepoint["config"]
        )

        ## Configure Microsoft Graph & Domain
        self.graph["domain"] = r"https://graph.microsoft.com"
        self.graph["version"] = rf"{ self.graph['domain'] }/v1.0"
        self.graph["sites"] = rf"{ self.graph['version'] }/sites"
        self.login = r"https://login.microsoftonline.com"

        # return None

    ## ------------------------------------------
    def configure_profile( self ) -> bool:
        """
        Objective:  Configure SharePoint profile
        Parameters: None
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     toolset.display_message(
        #         message = "Configure SharePoint Profile"
        #     )

        ## Warning: Execution sequence is critical
        if self.profile is not None:
            self.profile_secrets()
            self.profile_locations()
        # if self.args.debug:
        #     toolset.print_json( content = self.profile )

        return True

    ## ------------------------------------------
    def copy_item(
            self,
            source_item: str = None,
            target_folder: str = None,
            target_name: str = None
        ) -> None:
        """
        Objective:  Copy item to another location
        Parameters:
            source_item => Source item to copy (str)
            target_folder => Target folder to copy (str)
            target_name => Target name to copy (str)
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     toolset.display_message(
        #         message = "Copying SharePoint files"
        #     )

        file_url = (
            rf"{ self.graph['sites'] }/" + 
            rf"{ self.profile['credentials']['site_id'] }/drives/" + 
            rf"{ self.profile['credentials']['drive_id'] }/items/" + 
            rf"{ source_item }/copy"
        )
        # if self.args.debug:
        #     toolset.display_message(
        #         heading = None,
        #         message = f"File URL: { file_url }\n"
        #     )
        token_value = self.credentials["token"]["token_value"]
        # toolset.display_message(
        #     heading = None,
        #     message = f"Token Value: { token_value }\n"
        # )
        headers = {
            "Authorization": rf"Bearer { token_value }",
            "Content-Type": "application/json"
        }
        # toolset.display_message(
        #     heading = None,
        #     message = f"Headers: { headers }\n"
        # )
        json_data = {
            "parentReference": { "id": target_folder },
            "name": target_name
        }
        # toolset.display_message(
        #     heading = None,
        #     message = f"JSON Data: { json_data }"
        # )
        try:

            response = requests.post(
                file_url,
                headers = headers,
                json = json_data,
                timeout = 60
            )
            if response.status_code in [ 202, 409 ]:
                # status_code = f"{ response.status_code }"
                # description = self.status_code[ status_code ]
                # if self.args.debug:
                #     toolset.display_message(
                #         heading = None,
                #         message = f"{ status_code }: { description }"
                #     )
                pass
            else:
                sys.exit( response.status_code )

        except requests.exceptions.RequestException as error:
            toolset.display_warning( message = error )

        return True

    ## ------------------------------------------
    def create_folder(
            self,
            target_folder: str = None,
        ) -> None:
        """
        Objective:  Create SharePoint Folder
        Parameters:
            target_folder => Target folder to create (str)
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        folder_url = (
            rf"{ self.graph['sites'] }/" +
            rf"{ self.profile['credentials']['site_id'] }/drives/" +
            rf"{ self.profile['credentials']['drive_id'] }/root:/" +
            rf"{ target_folder }"
        )
        # if self.args.debug:
        #     toolset.display_message(
        #         heading = None,
        #         message = f"File URL: { folder_url }\n"
        #     )
        token_value = self.credentials["token"]["token_value"]
        # toolset.display_message(
        #     heading = None,
        #     message = f"Token Value: { token_value }\n"
        # )
        headers = {
            "Authorization": rf"Bearer { token_value }",
            "Content-Type": "application/json"
        }
        # toolset.display_message(
        #     heading = None,
        #     message = f"Headers: { headers }\n"
        # )
        json_data = {
            "folder": {},
            "@microsoft_graph_conflict_behavior" : "fail"
        }
        # toolset.display_message(
        #     heading = None,
        #     message = f"JSON Data: { json_data }"
        # )
        try:
            response = requests.patch(
                folder_url,
                headers = headers,
                json = json_data,
                timeout = 60
            )
            if response.status_code in [ 200, 201 ]:
                # description = self.status_code[ response.status_code ]
                # if self.args.debug:
                #     toolset.display_message(
                #         heading = None,
                #         message = f"{ response.status_code }: { description }"
                #     )
                self.archive_folder = response.json()
            else:
                toolset.display_message(
                    message = "Failed to create folder!"
                )
                toolset.print_json( content = response.json() )
                sys.exit( response.status_code )
        except requests.exceptions.RequestException as error:
            toolset.display_warning( error )

        return response.json()

    ## ------------------------------------------
    def credentials_driveid( self ) -> Any:
        """
        Objective:  Acquire Drive ID for SharePoint
        Parameters: None
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     toolset.display_message(
        #         message = "Retrieving SharePoint Drive-ID"
        #     )

        site_id = self.credentials["site_id"]
        try:
            token_value = self.credentials["token"]["token_value"]
            response = requests.get(
                rf"{ self.graph['sites'] }/{ site_id }/drives/",
                headers = {
                    "Authorization": rf"Bearer { token_value }"
                },
                timeout = 60
            )
            if response.status_code == 200:
                for library in response.json()["value"]:
                    resource = self.locations["library"]
                    if library["name"] == resource:
                        drive_id = library["id"]
                if drive_id is None:
                    toolset.display_warning(
                        message = "SharePoint Library was not found"
                    )
                    return False
                self.credentials["drive_id"] = drive_id
            else:
                toolset.print_json( content = response.json() )
                sys.exit( response.status_code )
        except requests.exceptions.RequestException as error:
            toolset.display_warning( message = error )
            drive_id = False

        return drive_id

    ## ------------------------------------------
    def credentials_siteid( self ) -> Any:
        """
        Objective:  Acquire Site ID for SharePoint
        Parameters: None
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     toolset.display_message(
        #         message = "Retrieving SharePoint Site-ID"
        #     )

        sitename = self.storage['site_name']
        try:
            token_value = self.credentials["token"]["token_value"]
            response = requests.get(
                rf"{ self.graph['sites'] }/root:/sites/{ sitename }/",
                headers = {
                    "Authorization": rf"Bearer { token_value }"
                },
                timeout = 60
            )
            if response.status_code == 200:
                site_id = response.json()["id"].split( "," )[1]
                self.credentials["site_id"] = site_id
            else:
                toolset.print_json( content = response.json() )
                sys.exit( response.status_code )
        except requests.exceptions.RequestException as error:
            toolset.display_warning( message = error )
            site_id = False

        return site_id

    ## ------------------------------------------
    def credentials_token( self ) -> Any:
        """
        Objective:  Generate Credentials Token
        Parameters: None
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     toolset.display_message(
        #         message = "Generating Credentials Token"
        #     )

        tenant_id = self.credentials["tenant_id"]
        data = {
            "grant_type": "client_credentials",
            "client_id": self.credentials["client_id"],
            "client_secret": self.credentials["secret"]["secret_value"],
            "resource": self.graph["domain"]
        }
        # toolset.print_json( content = data )
        try:
            response = requests.post(
                rf"{ self.login }/{ tenant_id }/oauth2/token",
                data = data,
                timeout = 60
            )
            if response.status_code == 200:
                token_value = response.json()["access_token"]
                self.credentials["token"]["token_value"] = token_value
            else:
                toolset.print_json( content = response.json() )
                sys.exit( response.status_code )
        except requests.exceptions.RequestException as error:
            toolset.display_warning( error )
            token_value = False

        return token_value

    ## ------------------------------------------
    def delete_item(
            self,
            target_item: str = None
        ) -> None:
        """
        Objective:  Delete item from SharePoint
        Parameters:
            target_item => Target item to delete (str)
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        delete_url = (
            rf"{ self.graph['sites'] }/" +
            rf"{ self.profile['credentials']['site_id']  }/drives/" +
            rf"{ self.profile['credentials']['drive_id']  }/items/root:/" +
            rf"{ target_item }"
        )
        # if self.args.debug:
        #     toolset.display_message(
        #         heading = None,
        #         message = f"\nDelete URL: { delete_url }\n"
        #     )
        token_value = self.credentials["token"]["token_value"]
        response = requests.delete(
            delete_url,
            headers = {
                "Authorization": rf"Bearer { token_value }",
                "Content-Type": "application/json"
            },
            timeout = 60
        )
        if response.status_code == 200:
            toolset.print_json( content = response.json() )
        else:
            toolset.print_json( content = response.json() )
            sys.exit( response.status_code )

        return True

    ## ------------------------------------------
    def download_files( self ) -> bool:
        """
        Objective:  Download SharePoint Files
        Parameters: None
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     toolset.display_message(
        #         message = "Download SharePoint Files"
        #     )

        downloads = []
        # source_files = self.locations["import"]["files"]
        source_files = self.select_files()
        if self.args.download is not None:
            if self.args.verbose:
                toolset.display_message(
                    heading = None,
                    message = "\nDownloading files:\n"
                )
                toolset.print_json( content = source_files )
        # for source_file in source_files:
        #     if self.args.debug:
        #         toolset.display_message(
        #             heading = None,
        #             message = source_file
        #         )
        #     # else:
        #     #     name = source_file["name"]
        #     #     target = source_file["target"]
        #     #     message = f"Downloading { name } as { target }"
        #     #     toolset.display_message(
        #     #         message = message
        #     #     )
        downloads.append(
            self.fetch_content(
                source_files
            )
        )
        # toolset.display_message(
        #     heading = None,
        #     message = downloads
        # )

        return downloads

    ## ------------------------------------------
    def export_profile( self ) -> bool:
        """
        Objective:  Export SharePoint profile
        Parameters: None
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     toolset.display_message(
        #         message = "Exporting SharePoint Profile"
        #     )

        update = False
        ## Updating Configuration file
        if os.path.exists( self.sharepoint["filepath"] ):
            with open(
                self.sharepoint["filepath"],
                mode = "r",
                encoding = "utf8"
            ) as file:
                profile = json.load(
                    fp = file,
                )
            ## Determine Update Status
            # if self.args.debug:
            #     update_profile = profile['locations']['update']
            #     toolset.display_message(
            #         heading = None,
            #         message = f"\nUpdate Profile: { update_profile }"
            #     )
            if profile["locations"]["update"] is True:
                ## Resetting Profile Locations
                self.locations = self.storage
                profile["locations"] = self.locations
            update = True
        ## Creating Configuration file
        if not os.path.exists( self.sharepoint["filepath"] ):
            ## Copying SharePoint profile
            json_config = json.dumps( self.profile )
            profile = json.loads( json_config )
            for items in profile["credentials"].items():
                index, section = items
                if isinstance( section, dict ):
                    for key, value in section.items():
                        # print( key, value )
                        response = self.access["fernet"].encrypt(
                            str( value ).encode( encoding = "utf8" )
                        ).decode( encoding = "utf8" )
                        section[ key ] = response
                else:
                    # print( index, section )
                    response = self.access["fernet"].encrypt(
                        str( section ).encode( encoding = "utf8" )
                    ).decode( encoding = "utf8" )
                    profile["credentials"][ index ] = response
            # toolset.print_json( content = profile["credentials"] )
            update = True
        ## Inspecting SharePoint remotes
        self.inspect_locations()
        # if self.args.debug:
        #     toolset.print_json( content = profile )
        if update:
            with open(
                self.sharepoint["filepath"],
                mode = "w",
                encoding = "utf8"
            ) as file:
                json.dump(
                    profile,
                    fp = file,
                    indent = 4
                )

        return True

    ## ------------------------------------------
    def fetch_content(
            self,
            source_files: dict = None
        ) -> Any:
        """
        Objective:  Downloading SharePoint File
        Parameters:
            source_files => Source files to download (dict)
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     toolset.display_message(
        #         message = "Downloading SharePoint Content"
        #     )

        token_value = self.credentials["token"]["token_value"]
        file_paths = []
        for file_name in source_files:
            download_url = (
                rf"{ self.graph['sites'] }/" +
                rf"{ self.credentials['site_id'] }/drives/" +
                rf"{ self.credentials['drive_id'] }/root:/" + 
                rf"{ self.importing['remote'] }/" +
                rf"{ file_name['name'] }:/content"
            )
            # if self.args.debug:
            #     toolset.display_message(
            #         heading = None,
            #         message = f"\nDownload URL: { download_url }"
            #     )
            try:
                response = requests.get(
                    download_url,
                    headers = {
                        "Authorization": rf"Bearer { token_value }"
                    },
                    timeout = 60
                )
                if response.status_code == 200:
                    # content = response.content.decode()
                    content = response.content
                    # if self.args.debug:
                    #     toolset.print_json( content = content )
                else:
                    toolset.print_json( content = response.json() )
                    sys.exit( response.status_code )
            except requests.exceptions.RequestException as error:
                toolset.display_warning( error )
            # if file_name["target"] is not None:
            #     target_file = file_name["target"]
            # else:
            #     target_file = file_name["name"]
            try:
                file_path = os.path.join(
                    self.importing["local"],
                    file_name["rename"]
                )
                with open(
                    file_path,
                    "wb"
                ) as temp_file:
                    # if self.args.debug:
                    #     print( content )
                    temp_file.write( content )
                file_paths.append( file_path )
            except IOError as e:
                toolset.print_json(
                    content = f"I/O error({ e.errno }): { e.strerror }"
                )
                # file_path = None

        return file_paths

    ## ------------------------------------------
    def inspect_locations( self ) -> bool:
        """
        Objective:  Inspect SharePoint Remote Locations
        Parameters: None
        Returns:    True (bool)
        """

        toolset.trace_workflow( inspect.currentframe() )

        ## Configure Import Action
        self.importing["action"] = self.locations["import"]["action"]
        ## Configure SharePoint Import-Local
        self.importing["local"] = os.path.join(
            self.trg_path,
            self.locations["import"]["local"].replace( ':', os.sep )
        )
        # if self.args.debug:
        #     toolset.display_message(
        #         heading = None,
        #         message = "\nImport Local Path", self.importing["local"]
        #     )
        ## Configure SharePoint Import-Remote
        self.importing["remote"] = "/".join( [
                self.locations["project"],
                self.locations['import']['remote']
            ] )
        # if self.args.debug:
        #     toolset.display_message(
        #         heading = None,
        #         message = "\nImport Remote Path", self.importing["remote"]
        #     )
        ## Configure SharePoint Export-Local
        self.exporting["local"] = os.path.join(
            self.trg_path,
            self.locations["export"]["local"].replace( ':', os.sep )
        )
        # if self.args.debug:
        #     toolset.display_message(
        #         heading = None,
        #         message = f"\nExport Local Path: { self.exporting['local'] }"
        #     )
        ## Configure SharePoint Export-Remote
        self.exporting["remote"] = "/".join( [
                self.locations["project"],
                self.locations['export']['remote']
            ] )
        # if self.args.debug:
        #     toolset.display_message(
        #         heading = None,
        #         message = f"\nExport Remote Path: { self.exporting['remote'] }"
        #     )
        ## Configure SharePoint Export-Action
        self.exporting["action"] = self.locations["export"]["action"]
        ## Configure SharePoint Export-Archive
        self.exporting["archive"] = "/".join( [
            self.exporting["remote"],
            self.locations["export"]["archive"]
        ] )
        # if self.args.debug:
        #     toolset.display_message(
        #         heading = None,
        #         f"\nArchive Remote Path: { self.exporting['archive'] }"
        #     )
        ## Configure SharePoint Already-Export
        self.already["exported"], listed_items = self.list_files(
            self.exporting["remote"],
            self.locations["export"]["files"]
        )
        if not any(
            self.locations['export']['archive'] == item["name"]
            for item in listed_items
        ):
            # toolset.display_message(
            #     heading = None,
            #     message = f"\nCreating { self.locations['export']['archive'] } folder"
            # )
            self.create_folder(
                self.exporting["archive"]
            )
        # if self.args.debug:
        #     toolset.display_message(
        #         heading = None,
        #         message = "\nAlready Exported Files\n"
        #     )
        #     toolset.print_json( content = self.already["exported"] )
        ## Configure SharePoint Already-Archive
        self.already["archived"], _ = self.list_files(
            self.exporting["archive"],
            None
        )
        # if self.args.debug:
        #     toolset.display_message(
        #         heading = None,
        #         message = "\nAlready Archived Files\n"
        #     )
        #     toolset.print_json( content = self.already["archived"] )
        ## Configure SharePoint Archive-Folder
        if any(
            self.locations['export']['archive'] == item["name"]
            for item in listed_items
        ):
            for item in listed_items:
                if item["name"] == self.locations['export']['archive']:
                    self.archive_folder = item
        # toolset.print_json( content = self.archive_folder )

        return True

    ## ------------------------------------------
    def list_files(
            self,
            remote_location: str = None,
            target_files: list = None
        ) -> list:
        """
        Objective:  Listing SharePoint Files (downloads)
        Parameters:
            remote_location => Remote location to list (str)
            target_files => Target files to list (list)
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     toolset.display_message(
        #         heading = None,
        #         message = "\nRetrieving SharePoint files"
        #     )

        drive_id = self.credentials["drive_id"]
        files_url = (
            rf"{ self.graph['version'] }/drives/" +
            rf"{ drive_id }/root:/" +
            rf"{ remote_location }:/children"
        )
        # if self.args.debug:
        #     toolset.display_message(
        #         heading = None,
        #         message = f"\nFiles URL: { files_url }"
        #     )
        files_list = []
        listed_files = []
        try:
            token_value = self.credentials["token"]["token_value"]
            response = requests.get(
                files_url,
                headers = {
                    "Authorization": rf"Bearer { token_value }"
                },
                timeout = 60
            )
            # if self.args.debug:
            #     toolset.print_json( content = response.json() )
            if response.status_code == 200:
                listed_files = response.json()["value"]
                for listed_file in listed_files:
                    if listed_file.get( "file" ):
                        item_type = "file"
                        # if self.args.debug:
                        #     toolset.print_json( content = listed_file )
                    else:
                        item_type = "folder"
                    file_attributes = {
                        "id": listed_file["id"],
                        "time": listed_file["lastModifiedDateTime"],
                        "name": listed_file["name"],
                        "size": listed_file["size"],
                        "target": None,
                        "type": item_type,
                        "parent": listed_file["parentReference"]
                    }
                    if target_files is not None:
                        if self.importing["action"] == self.import_latest:
                            for file in target_files:
                                if file["target"] in listed_file["name"]:
                                    file_attributes["name"] = listed_file["name"]
                                    file_attributes["target"] = file["target"]
                                    file_attributes["rename"] = file["name"]
                                    if file_attributes["type"] == "file":
                                        files_list.append( file_attributes )
                    # elif self.importing["action"] == self.import_everything:
                    else:
                        if file_attributes["type"] == "file":
                            files_list.append( file_attributes )
                # if self.args.debug:
                #     if files_list:
                #         ## Displaying Listed files
                #         for file in files_list:
                #             toolset.display_message(
                #                 heading = None,
                #                 message = f"\nFile: { remote_location }/{ file['target'] }"
                #             )
                #             toolset.print_json( content = file )
                #     else:
                #         toolset.display_warning(
                #             message = f"{ remote_location }: No files were found!"
                #         )
            else:
                toolset.print_json( content = response.json() )
                sys.exit( response.status_code )
        except requests.exceptions.RequestException as error:
            toolset.display_warning( message = error )
            sys.exit( error )

        return files_list, listed_files

    ## ------------------------------------------
    def locations_token( self ) -> float:
        """
        Objective:  Provision Token & Generates JSON content
        Parameters: None
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     toolset.display_message(
        #         message = "Generating/Updating Locations Token"
        #     )

        if self.credentials["token"]["token_ttl"] == self.__empty__:
            token_ttl = time.time()
        else:
            token_ttl = float( self.credentials["token"]["token_ttl"] )
            token_ttl -= time.time()
            if token_ttl <= 3000:
                self.credentials_token()

        return token_ttl

    ## ------------------------------------------
    def profile_locations( self ) -> bool:
        """
        Objective:  Configure SharePoint locations
        Parameters: None
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     toolset.display_message(
        #         message = "Configuring SharePoint Locations"
        #     )

        profile = {
            "console": {
                "default": self.locations["console"],
                "question": None,
                "response": self.graph["domain"]
            },
            "site_name": {
                "default": self.storage["site_name"],
                "question": "SharePoint Site: ",
                "response": None
            },
            "library": {
                "default": self.locations["library"],
                "question": "SharePoint Library: ",
                "response": None
            },
            "import_remote": {
                "default": self.importing["remote"],
                "question": "SharePoint Download: ",
                "response": None
            },
            "export_remote": {
                "default": self.exporting["remote"],
                "question": "SharePoint Upload: ",
                "response": None
            }
        }
        ## Processing default invalid/empty configs
        for sections in profile.items():
            index, section = sections
            if section["question"] is not None:
                if section["default"] is self.__empty__:
                    section["response"] = core_parser.process_userinput(
                        question = section["question"]
                    ).replace( self.__space__, self.__empty__ )
        ## Processing default custom configs
        defaults = [
            "console",
            "site_name",
            "library"
        ]
        for sections in profile.items():
            index, section = sections
            response = section["response"]
            if response is not None:
                if index in defaults:
                    self.locations[ index ] = response
                else:
                    if index == "import_remote":
                        self.locations["import"]["remote"] = "/".join( [
                            self.locations["project"],
                            response
                        ] )
                    if index == "remote_export":
                        self.locations["export"]["remote"] = "/".join( [
                            self.locations["project"],
                            response
                        ] )
        # if self.args.debug:
        #     toolset.print_json( content = self.profile["locations"] )

        return True

    ## ------------------------------------------
    def profile_secrets( self ) -> bool:
        """
        Objective:  Configure SharePoint Credentials
        Parameters: None
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     toolset.display_message(
        #         message = "Configuring SharePoint Credentials"
        #     )

        ## Extracting SharePoint site-name
        site_name = self.storage["site_name"]
        ## SharePoint Environment credentials
        try:
            defaults = os.environ.get(
                f"SharePoint_{ site_name }_Credentials",
                None
            ).strip().split()
        except AttributeError as _:
            defaults = None
        # toolset.display_message(
        #     heading = None,
        #     message = f"SharePoint Credentials: { defaults }"
        # )
        ## Processing environment credentials
        if defaults is not None:
            client_id, tenant_id, secret_id, secret_value = defaults
            ## Processing required configurations
            self.credentials["client_id"] = client_id
            self.credentials["tenant_id"] = tenant_id
            self.credentials["secret"]["secret_id"] = secret_id
            self.credentials["secret"]["secret_value"] = secret_value
        else:
            profile = {
                "client_id": {
                    "question": "Client ID: ",
                    "response": None
                },
                "tenant_id": {
                    "question": "\nTenant ID: ",
                    "response": None
                },
                "secret_id": {
                    "question": "\nSecret ID: ",
                    "response": None
                },
                "secret_value": {
                    "question": "Secret Value: ",
                    "response": None
                },
                "secret_ttl": {
                    "question": None,
                    "response": None
                },
                "token_ttl": {
                    "question": None,
                    "response": None
                },
                "token_value": {
                    "question": None,
                    "response": None
                },
                "site_id": {
                    "question": None,
                    "response": None
                },
                "drive_id": {
                    "question": None,
                    "response": None
                }
            }
            for sections in profile.items():
                index, section = sections
                question = section["question"]
                if question is not None:
                    response = core_parser.process_userinput(
                        question = section["question"]
                    ).replace( self.__space__, self.__empty__ )
                    if index in [ "secret_id", "secret_value" ]:
                        self.credentials["secret"][ index ] = response
                    else:
                        self.credentials[ index ] = response
        ## Processing custom configurations
        self.credentials["token"]["token_ttl"] = self.locations_token()
        self.credentials["token"]["token_value"] = self.credentials_token()
        self.credentials["site_id"] = self.credentials_siteid()
        self.credentials["drive_id"] = self.credentials_driveid()
        # if self.args.debug:
        #     toolset.print_json( content = self.credentials )

        return True

    ## ------------------------------------------
    def provision_profile( self ) -> bool:
        """
        Objective:  Provision SharePoint JSON config-file
        Parameters: None
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     filepath = self.sharepoint["filepath"]
        #     toolset.display_message(
        #         message = f"SharePoint Configuration: { filepath }"
        #     )

        if os.path.exists( self.sharepoint["filepath"] ):
            self.request_passphrase()
            with open(
                self.sharepoint["filepath"],
                mode = "rb"
            ) as file:
                configuration = file.read()
            self.profile = json.loads( configuration )
            credentials = self.profile["credentials"]
            passphrase = str( self.access["phrase"] )
            error_message = f"Invalid Passphrase: { passphrase }\n"
            for items in self.profile["credentials"].items():
                index, section = items
                if isinstance( section, dict ):
                    for key, value in section.items():
                        # print( key, value )
                        try:
                            response = self.access["fernet"].decrypt(
                                str( value )
                            ).decode( encoding = "utf8" )
                            section[ key ] = response
                        except InvalidToken as error:
                            toolset.display_warning(
                                message = f"InvalidToken: { key }"
                            )
                            sys.exit( f"{ error_message }{ error }" )
                else:
                    try:
                        # print( index, section )
                        response = self.access["fernet"].decrypt(
                            str( section )
                        ).decode( encoding = "utf8" )
                        self.profile["credentials"][ index ] = response
                    except InvalidToken as error:
                        toolset.display_warning(
                            message = f"InvalidToken: { section }"
                        )
                        sys.exit( f"{ error_message }{ error }" )

# raise UserSecretException( error_message ) from error
# except Exception as error:
#     raise ValueError( error ) from error

# h.verify(data[-32:])
# cryptography.exceptions.InvalidSignature: Signature did not match digest.
# During handling of the above exception, another exception occurred:

# raise InvalidToken
# cryptography.fernet.InvalidToken
# The above exception was the direct cause of the following exception:

            self.profile["credentials"] = credentials
            self.credentials = self.profile.get( "credentials", {} )
            self.locations = self.profile.get( "locations", {} )
            self.locations_token()
        else:
            self.access["keyset"] = None
            self.credentials = self.profile.get( "credentials", {} )
            self.locations = self.profile.get( "locations", {} )
            self.configure_profile()
        # if self.args.debug:
        #     toolset.print_json( content = self.profile )

        return True

    ## ------------------------------------------
    def publish_content(
            self,
            source_file: dict = None
        ) -> Any:
        """
        Objective:  Uploading file to SharePoint
        Parameters:
            source_file => Source file to upload (dict)
        Returns:    None
        """
        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     toolset.display_message(
        #         heading = None,
        #         message = "Uploading file to SharePoint"
        #     )
        #     toolset.display_message(
        #         heading = None,
        #         message = f"\nReport Path: { source_file['name'] }"
        #     )

        if source_file["target"] is not None:
            file_name = source_file["target"]

        if self.exporting["action"] == "archive":
            ## Archiving SharePoint item
            self.archive_item(
                target_item = source_file
            )

        upload_url = (
            rf"{ self.graph['sites'] }/" +
            rf"{ self.profile['credentials']['site_id'] }/drives/" +
            rf"{ self.profile['credentials']['drive_id'] }/items/root:/" +
            rf"{ self.exporting['remote'] }/{ file_name }:/content"
        )
        # if self.args.debug:
        #     toolset.display_message(
        #         heading = None,
        #         message = f"\nUpload URL: { upload_url }\n"
        #     )
        token_value = self.credentials["token"]["token_value"]
        file_path = os.path.join(
            self.exporting["local"],
            source_file["name"]
        )
        file_name = source_file["name"]
        with open(
            file_path,
            "rb"
        ) as file:
            try:
                file_size = str( os.path.getsize( file_path ) )
                response = requests.put(
                    upload_url,
                    headers = {
                        "Authorization": rf"Bearer { token_value }",
                        "Content-Type": "application/octet-stream",
                        "Content-Length": file_size
                    },
                    data = file,
                    timeout = 60
                )
                content = response.json()
                del content["@odata.context"]
                del content["@microsoft.graph.downloadUrl"]
                if response.status_code in [ 200, 201, 202 ]:
                    # uploaded = f"Uploaded [{ file_name }] to SharePoint"
                    # if self.args.debug:
                    #     toolset.display_message(
                    #         heading = None,
                    #         message = uploaded
                    #     )
                    #     # toolset.print_json(
                    #     #     content = content
                    #     # )
                    pass
                else:
                    toolset.print_json(
                        content = response.json()
                    )
                    sys.exit( response.status_code )
            except requests.exceptions.RequestException as error:
                toolset.print_json( content = error )

        return response.json()["webUrl"]

    ## ------------------------------------------
    def request_passphrase( self ) -> bool:
        """
        Objective:  Encryption Passphrase
        Parameters: None
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     toolset.display_message(
        #         message = "Requesting Encryption Passphrase"
        #     )

        ## Provided passphrase
        if self.args.password is not False:
            self.access["phrase"] = self.args.password.encode(
                encoding = "utf8"
            )
        ## Extracted passphrase
        elif self.args.password is False:
            ## Extracting SharePoint site-name
            site_name = self.storage["site_name"]
            ## SharePoint Environment passphrase
            try:
                passphrase = bytes(
                    os.environ.get(
                        f"SharePoint_{ site_name }_Passphrase",
                        None
                    ).strip(),
                    encoding = "utf8"
                )
            except AttributeError as _:
                passphrase = None
            self.access["phrase"] = passphrase
        ## Requesting passphrase
        if self.access["phrase"] is None:
            self.access["phrase"] = maskpass.askpass(
                prompt = "Enter Passphrase: ",
                mask = "*"
            ).encode( encoding = "utf8" )
            ## Processing passphrase
            response = self.access["phrase"]
            if response.strip() == 0:
                print(
                    "\033[A\033[J" * len( response ),
                    end = self.__empty__
                )
                self.request_passphrase()
        # toolset.display_message(
        #     heading = None,
        #     message = "access->phrase:", self.access["phrase"]
        # )
        self.access["hash"] = PBKDF2HMAC(
            algorithm = hashes.SHA256(),
            length = 32,
            salt = b"salt",
            iterations = 100000
        )
        # toolset.display_message(
        #     heading = None,
        #     message = "access->hash:", self.access["hash"]
        # )
        self.access["keyset"] = base64.urlsafe_b64encode(
            self.access["hash"].derive( self.access["phrase"] )
        )
        # toolset.display_message(
        #     heading = None,
        #     message = "access->keyset: { self.access["keyset"] }"
        # )
        self.access["fernet"] = Fernet( self.access["keyset"] )
        # toolset.display_message(
        #     heading = None,
        #     message = "access->fernet: { self.access["fernet"] }"
        # )

        return True

    ## ------------------------------------------
    def select_files( self ) -> list:
        """
        Objective:  Return most recent file
        Parameters: None
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        import_action = self.importing["action"]
        # if self.args.debug:
        #         toolset.display_message(
        #         heading = None,
        #         message = f"\nDownload/Import Action: { import_action }"
        #     )

        files, _ = self.list_files(
            self.importing["remote"],
            self.locations["import"]["files"]
        )
        # if self.args.debug:
        #         toolset.display_message(
        #         heading = None,
        #         message = "Available Files: { files }"
        #     )

        if import_action != "latest":
            toolset.display_message(
                message = "Listing all SharePoint files"
            )
            return files
        # # Processing latest filtering
        # if self.args.debug:
        #     for file in self.locations['import']['files']:
        #         tools.display_message(
        #             heading = None,
        #             message = f"\nListing Import File: { file['target'] }\n"
        #         )
        items = []
        newest = []
        latest = []
        selected = []
        for file_prefix in self.locations["import"]["files"]:
            items.append( file_prefix["target"] )
        # toolset.display_message(
        #     heading = None,
        #     message = f"Required Files: { items }"
        # )
        for item_prefix in items:
            # toolset.display_message(
            #     heading = None,
            #     message = f"Filtered File: { item_prefix }"
            # )
            for item in files:
                if item_prefix in item["name"]:
                    selected.append( item )
            for file in selected:
                latest.append( file["time"] )
                if file["time"] == max( latest ):
                    newest_file = file
            newest.append( newest_file )

        return newest

    ## ------------------------------------------
    def upload_files( self ) -> bool:
        """
        Objective:  Uploading Local Files
        Parameters: None
        Returns:    None
        """

        toolset.trace_workflow( inspect.currentframe() )

        # if self.args.debug:
        #     toolset.display_message(
        #         message = "Uploading Local Files"
        #     )

        uploads = []
        source_files = self.profile["locations"]["export"]["files"]
        # toolset.display_message(
        #     heading = None,
        #     message = source_files
        # )
        if self.args.upload is not None:
            if self.args.verbose:
                toolset.display_message(
                    heading = None,
                    message = "\nUploading files:\n"
                )
                toolset.print_json( content = source_files )
        for source_file in source_files:
            # if self.args.debug:
            #     toolset.display_message(
            #         heading = None,
            #         message = f"\nUpload File: { source_file }\n"
            #     )
            # else:
            #     name = source_file["name"]
            #     target = source_file["target"]
            #     message = f"Uploading { name } as { target }"
            #     toolset.display_message(
            #         message = message
            #     )
            response = self.publish_content(
                source_file
            )
            if response is not None:
                ## Updating SharePoint Exported
                self.already["exported"], _ = self.list_files(
                    self.exporting["remote"],
                    self.locations["export"]["files"]
                )
                uploads.append( response )
            # toolset.display_message(
            #     heading = None,
            #     message = f"\nUploaded File: { source_file }\n"
            # )
        # if self.args.debug:
        #     toolset.print_json( content = uploads )

        return uploads

# {
#     "error":{
#         "code":"InvalidAuthenticationToken",
#         "message":"Access token is empty.",
#         "innerError":{
#             "date":"2023-10-29T20:26:29",
#             "request-id":"0e56d200-078e-4476-9a9e-1223fd4151ba",
#             "client-request-id":"0e56d200-078e-4476-9a9e-1223fd4151ba"
#         }
#     }
# }
