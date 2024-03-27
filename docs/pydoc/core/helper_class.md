```console
Help on module helper_class:

NAME
    helper_class - Core Class: Helper Class

CLASSES
    core.classes.core_class.CoreClass(builtins.object)
        HelperClass

    class HelperClass(core.classes.core_class.CoreClass)
     |  HelperClass(json_object: dict = None) -> None
     |
     |  Objective:  Construct Helper Class
     |  Parameters:
     |      CoreClass (object)
     |  Returns:    None
     |
     |  Method resolution order:
     |      HelperClass
     |      core.classes.core_class.CoreClass
     |      builtins.object
     |
     |  Methods defined here:
     |
     |  __init__(self, json_object: dict = None) -> None
     |      Objective:  Initialize Script Helper
     |      Parameters:
     |          json_object (dict) -> None
     |      Returns:    None
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
    core/classes/helper_class.py
```