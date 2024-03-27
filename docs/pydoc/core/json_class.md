```console
Help on module json_class:

NAME
    json_class - Core JsonObject Class

CLASSES
    builtins.object
        JsonObject

    class JsonObject(builtins.object)
     |  JsonObject(data=None) -> None
     |
     |  Objective: Convert JSON to Object
     |  Reference: https://stackoverflow.com/a/66054047
     |
     |  Methods defined here:
     |
     |  __init__(self, data=None) -> None
     |      Objective:  Initialize Object variables
     |      Parameters:
     |          data (dict): JSON data
     |      Returns:    None
     |
     |  delete(self, key: str) -> None
     |      Delete attribute
     |
     |  items_list(self) -> list
     |      Return list of items
     |
     |  iter_dict(self) -> <built-in function iter>
     |      Return iterator
     |
     |  keys_list(self) -> list
     |      Return list of keys
     |
     |  len_dict(self) -> int
     |      Return length of dictionary
     |
     |  set_key_dict(self, key: str, value: Any) -> None
     |      Set item in dictionary
     |
     |  set_value(self, value: Any) -> typing.Any | list | tuple | dict
     |      Objective:  Configure Attributes
     |      Parameters:
     |          value attribute (object)
     |      Returns:    value attribute (object) | list | tuple | dict
     |
     |  values_list(self) -> list
     |      Return list of values
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object

FILE
    core/classes/json_class.py
```