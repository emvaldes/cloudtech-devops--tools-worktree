```console
Help on module mod_classes:

NAME
    mod_classes - Application Module: Worktree Classes

CLASSES
    core.classes.app_class.AppConfig(core.classes.config_class.ConfigClass)
        Worktree
    
    class Worktree(core.classes.app_class.AppConfig)
     |  Worktree(json_object: dict = None, trg_path: str = os.getcwd()) -> None
     |  
     |  Objective:  Construct Worktree Class
     |  Parameters:
     |      AppConfig (core.classes.AppConfig) -> None
     |  Returns:    None
     |  
     |  Method resolution order:
     |      Worktree
     |      core.classes.app_class.AppConfig
     |      core.classes.config_class.ConfigClass
     |      core.classes.helper_class.HelperClass
     |      core.classes.bucket_class.BucketsClass
     |      core.classes.core_class.CoreClass
     |      builtins.object
     |  
     |  Methods defined here:
     |  
     |  __init__(self, json_object: dict = None, trg_path: str = os.getcwd()) -> None
     |      Objective:  Initialize Class variables
     |      Parameters:
     |          json_object => JSON Object (dict)
     |      Returns:    None
     |  
     |  configure_environment(self) -> None
     |      Objective:  Configure Environment
     |      Parameters: None
     |      Returns:    None
     |  
     |  disable_branch(self, branch) -> bool
     |      Objective:  Disable (remove) Git Worktree Branch
     |      Parameters:
     |          branch (str): Git Branch
     |      Returns:    True/False (bool)
     |  
     |  display_worktree(self, abort=False, path=os.getcwd()) -> bool
     |      Objective:  Displaying Git Worktree
     |      Parameters:
     |          abort (bool): Abort execution
     |          path (str): Path to Git Repository
     |      Returns:    True/False (bool)
     |  
     |  enable_branch(self, target_branch, message, path=os.getcwd()) -> bool
     |      Objective:  Enable (add) Git Worktree Branch
     |      Parameters:
     |          target_branch (str): Git Branch
     |          message (str): Commit Message
     |          path (str): Path to Git Repository
     |      Returns:    True/False (bool)
     |  
     |  filter_branch(self, text, listing, pattern='/') -> str
     |      Objective:  Splits key/pair set and return its value
     |      Parameters:
     |          text (str): Text to be filtered (key/pair set)
     |          listing (list): List of patterns to be filtered/discarded
     |          pattern (str): Pattern to be used as split key/pair set
     |      Returns:    value (str): Extracted value or False
     |  
     |  import_branches(self) -> bool
     |      Objective:  Include All Branches into Git Worktree
     |      Parameters: None
     |      Returns:    True/False (bool)
     |  
     |  include_branch(self, branch: str = None) -> bool
     |      Objective:  Include Branch into Git Worktree
     |      Parameters:
     |          branch (str): Git Branch
     |      Returns:    True/False (bool)
     |  
     |  inspect_worktree(self, path) -> bool
     |      Objective:  Inspecting Git Worktree
     |      Parameters:
     |          path (str): Path to Git Repository
     |      Returns:    True/False (bool)
     |  
     |  manage_branches(self) -> bool
     |      Objective:  Managing Git Worktree branches
     |      Parameters: None
     |      Returns:    True/False (bool)
     |  
     |  prune_worktrees(self) -> bool
     |      Objective:  Pruning Git Worktree
     |      Parameters: None
     |      Returns:    True/False (bool)
     |      Warning:    Private method invoked by remove_worktrees()
     |  
     |  pull_branches(self) -> bool
     |      Objective:  Updating Git Repository branches
     |      Parameters: None
     |      Returns:    True/False (bool)
     |  
     |  remove_branch(self, target_branch: str = None) -> bool
     |      Objective:  Removing Git Worktree directory (branch)
     |      Parameters: worktrees (str): Path to Git Worktrees
     |      Returns:    True/False (bool)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes defined here:
     |  
     |  args = None
     |  
     |  discard = None
     |  
     |  ignore = None
     |  
     |  json_config = None
     |  
     |  repo = None
     |  
     |  revparse = {}
     |  
     |  worktrees = None
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from core.classes.app_class.AppConfig:
     |  
     |  export_project(self) -> bool
     |      Objective:  Export Project Configurations
     |      Parameters: None
     |      Returns:    bool (True)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from core.classes.app_class.AppConfig:
     |  
     |  storage = None
     |  
     |  trg_path = None
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from core.classes.bucket_class.BucketsClass:
     |  
     |  create_buckets(self, bucket_path: str = None, bucket_type: str = None, verbose: bool = False) -> bool | int
     |      Objective:  Create/Initialize (dirs, files, docs)
     |      Parameters:
     |          bucket_path  (str): Bucket path
     |          bucket_type  (str): Bucket type (dirs, files, docs)
     |          verbose     (bool): Verbose output
     |      Returns:    True (bool) | bucket_size (int)
     |  
     |  load_buckets(self, bucket_type: str = None, bucket_conf: dict = None, bucket_path: str = None, create: bool = False) -> bool
     |      Objective:  Construct Bucket (dirs, files, docs)
     |      Parameters:
     |          bucket_type  (str): Bucket type (dirs, files, docs)
     |          bucket_conf (dict): Bucket configuration
     |          bucket_path  (str): Bucket path
     |          create      (bool): Create bucket
     |      Returns:    True (bool)
     |  
     |  setup_buckets(self) -> bool
     |      Objective:  Setup Buckets (dirs, files, docs)
     |      Parameters: None
     |      Returns:    True (bool)
     |  
     |  update_buckets(self, dictobj: dict = None, tracker: str = None, abspath: str = None) -> bool
     |      Objective:  Update Buckets (dirs, files, docs)
     |      Parameters:
     |          dictobj (dict): Dictionary object
     |          tracker  (str): Tracking path
     |          abspath  (str): Absolute path
     |      Returns:    True (bool)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from core.classes.core_class.CoreClass:
     |  
     |  add_key_dict(self, key: str, value: Any) -> None
     |      Add item to dictionary
     |  
     |  get(self, key: str) -> Any
     |      Get attribute
     |  
     |  get_all_dict(self) -> dict
     |      Return dictionary of all attributes
     |  
     |  get_key_dict(self, key: str) -> Any
     |      Get item from dictionary
     |  
     |  get_record(self: Any, obj: object = typing.Any, index: str = None, packed: bool = False) -> list | core.classes.json_class.JsonObject
     |      Objective:  Returns record by key
     |      Parameters:
     |          obj    (object): Any Object
     |          index     (str): Index
     |          packed   (bool): Return dictionary
     |      Returns:    record (List or JsonObject)
     |  
     |  get_value(self: Any, obj: object = typing.Any, index: str = None) -> str | None
     |      Objective:  Getting Value by Key
     |      Parameters:
     |          obj   (object): Any Object
     |          index    (str): Index
     |      Returns:    value (str) | None
     |  
     |  has(self, key: str) -> bool
     |      Check if attribute exists
     |  
     |  missing_config(self, warning: str = None, status: str = 'JSON Configuration was not found!') -> None
     |      Objective:  Missing Configuration
     |      Parameters:
     |          warning (str): Warning message
     |          status  (str): Status message
     |      Returns:    sys.exit( warning )
     |  
     |  set(self, key: str, value: Any) -> None
     |      Set attribute
     |  
     |  set_value(self: Any, obj: list, index: str = None) -> str | None
     |      Objective:  Set Object Property
     |      Parameters:
     |          obj   (object): Any Object
     |          index    (str): Index
     |      Returns:    value (str) | None
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from core.classes.core_class.CoreClass:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Data and other attributes inherited from core.classes.core_class.CoreClass:
     |  
     |  __empty__ = ''
     |  
     |  __space__ = ' '
     |  
     |  buckets = None
     |  
     |  config = None
     |  
     |  input = None
     |  
     |  json = None
     |  
     |  output = None

FILE
    app/mod_classes.py
```