```console
Help on module bucket_class:

NAME
    bucket_class - Core Class: Bucket Class

CLASSES
    core.classes.core_class.CoreClass(builtins.object)
        BucketsClass

    class BucketsClass(core.classes.core_class.CoreClass)
     |  BucketsClass(json_object: dict = None) -> None
     |
     |  Objective:  Construct Bucket Class (dirs, files, docs)
     |  Parameters:
     |      CoreClass (object)
     |  Returns:    None
     |
     |  Method resolution order:
     |      BucketsClass
     |      core.classes.core_class.CoreClass
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __init__(self, json_object: dict = None) -> None
     |      Objective:  Initialize Script Buckets
     |      Parameters:
     |          json_object (dict) -> None
     |      Returns:    None
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
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object
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
    core/classes/bucket_class.py
```