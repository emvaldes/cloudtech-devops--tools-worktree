```console
Help on module core_class:

NAME
    core_class - Core Module: Classes

CLASSES
    builtins.object
        CoreClass
    
    class CoreClass(builtins.object)
     |  CoreClass(json_object: dict = None) -> None
     |  
     |  Objective:  Construct Core Class
     |  Parameters: None
     |  Returns:    None
     |  
     |  Methods defined here:
     |  
     |  __init__(self, json_object: dict = None) -> None
     |      Objective:  Initialize Class variables
     |      Parameters:
     |          json_object (dict) -> None
     |      Returns:    None
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
    core/classes/core_class.py
```