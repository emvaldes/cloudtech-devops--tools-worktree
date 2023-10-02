```console
Help on module sharepoint:

NAME
    sharepoint - Core Class: SharePoint

CLASSES
    builtins.object
        SharePoint
    
    class SharePoint(builtins.object)
     |  SharePoint(trg_path: str = os.getcwd(), args: Any = None, storage: dict = None) -> None
     |  
     |  Objective:  Construct SharePoint Class
     |  Parameters: ConfigClass (core.classes.ConfigClass)
     |  Returns:    None
     |  
     |  Methods defined here:
     |  
     |  __init__(self, trg_path: str = os.getcwd(), args: Any = None, storage: dict = None) -> None
     |      Objective:  Initialize Class variables
     |      Parameters:
     |          trg_path (str): Target path (default: os.getcwd())
     |          args (Any): User-Input arguments (default: None)
     |          storage (dict): User-Input JSON Configuration (default: None)
     |      Returns:    None
     |  
     |  archive_item(self, target_item: dict = None) -> None
     |      Objective:  Archive item to another location
     |      Parameters:
     |          target_item => Target item to archive (dict)
     |      Returns:    None
     |  
     |  configure_environment(self) -> None
     |      Objective:  Configure Environment
     |      Parameters: None
     |      Returns:    None
     |  
     |  configure_profile(self) -> bool
     |      Objective:  Configure SharePoint profile
     |      Parameters: None
     |      Returns:    None
     |  
     |  copy_item(self, source_item: str = None, target_folder: str = None, target_name: str = None) -> None
     |      Objective:  Copy item to another location
     |      Parameters:
     |          source_item => Source item to copy (str)
     |          target_folder => Target folder to copy (str)
     |          target_name => Target name to copy (str)
     |      Returns:    None
     |  
     |  create_folder(self, target_folder: str = None) -> None
     |      Objective:  Create SharePoint Folder
     |      Parameters:
     |          target_folder => Target folder to create (str)
     |      Returns:    None
     |  
     |  credentials_driveid(self) -> Any
     |      Objective:  Acquire Drive ID for SharePoint
     |      Parameters: None
     |      Returns:    None
     |  
     |  credentials_siteid(self) -> Any
     |      Objective:  Acquire Site ID for SharePoint
     |      Parameters: None
     |      Returns:    None
     |  
     |  credentials_token(self) -> Any
     |      Objective:  Generate Credentials Token
     |      Parameters: None
     |      Returns:    None
     |  
     |  delete_item(self, target_item: str = None) -> None
     |      Objective:  Delete item from SharePoint
     |      Parameters:
     |          target_item => Target item to delete (str)
     |      Returns:    None
     |  
     |  download_files(self) -> bool
     |      Objective:  Download SharePoint Files
     |      Parameters: None
     |      Returns:    None
     |  
     |  export_profile(self) -> bool
     |      Objective:  Export SharePoint profile
     |      Parameters: None
     |      Returns:    None
     |  
     |  fetch_content(self, source_files: dict = None) -> Any
     |      Objective:  Downloading SharePoint File
     |      Parameters:
     |          source_files => Source files to download (dict)
     |      Returns:    None
     |  
     |  inspect_locations(self) -> bool
     |      Objective:  Inspect SharePoint Remote Locations
     |      Parameters: None
     |      Returns:    True (bool)
     |  
     |  list_files(self, remote_location: str = None, target_files: list = None) -> list
     |      Objective:  Listing SharePoint Files (downloads)
     |      Parameters:
     |          remote_location => Remote location to list (str)
     |          target_files => Target files to list (list)
     |      Returns:    None
     |  
     |  locations_token(self) -> float
     |      Objective:  Provision Token & Generates JSON content
     |      Parameters: None
     |      Returns:    None
     |  
     |  profile_locations(self) -> bool
     |      Objective:  Configure SharePoint locations
     |      Parameters: None
     |      Returns:    None
     |  
     |  profile_secrets(self) -> bool
     |      Objective:  Configure SharePoint Credentials
     |      Parameters: None
     |      Returns:    None
     |  
     |  provision_profile(self) -> bool
     |      Objective:  Provision SharePoint JSON config-file
     |      Parameters: None
     |      Returns:    None
     |  
     |  publish_content(self, source_file: dict = None) -> Any
     |      Objective:  Uploading file to SharePoint
     |      Parameters:
     |          source_file => Source file to upload (dict)
     |      Returns:    None
     |  
     |  request_passphrase(self) -> bool
     |      Objective:  Encryption Passphrase
     |      Parameters: None
     |      Returns:    None
     |  
     |  select_files(self) -> list
     |      Objective:  Return most recent file
     |      Parameters: None
     |      Returns:    None
     |  
     |  upload_files(self) -> bool
     |      Objective:  Uploading Local Files
     |      Parameters: None
     |      Returns:    None
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  __empty__ = ''
     |  
     |  __space__ = ' '
     |  
     |  __tab__ = '\t'
     |  
     |  access = {'fernet': None, 'hash': None, 'keyset': None, 'phrase': None...
     |  
     |  already = {'archived': [], 'exported': []}
     |  
     |  archive_folder = {}
     |  
     |  args = None
     |  
     |  credentials = None
     |  
     |  exporting = {'action': None, 'archive': None, 'local': None, 'remote':...
     |  
     |  graph = {'domain': None, 'sites': None, 'version': None}
     |  
     |  import_everything = 'all'
     |  
     |  import_latest = 'latest'
     |  
     |  importing = {'action': None, 'local': None, 'remote': None}
     |  
     |  locations = None
     |  
     |  login = None
     |  
     |  profile = {'credentials': {'client_id': '', 'drive_id': '', 'secret': ...
     |  
     |  sharepoint = {'config': None, 'filepath': None}
     |  
     |  status_code = {'200': 'Indicates that the request has succeeded.', '20...
     |  
     |  storage = None
     |  
     |  trg_path = None

FILE
    core/modules/storage/sharepoint.py
```