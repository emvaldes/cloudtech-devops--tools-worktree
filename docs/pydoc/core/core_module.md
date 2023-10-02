```console
Help on module core_module:

NAME
    core_module - Core Module: Objects, Functions

FUNCTIONS
    configure_features(parser: dict = None) -> dict
        Objective:  Configure Script Features
        Parameters:
            parser (dict): Script Parser
        Returns:    None
    
    configure_gitrepo() -> bool
        Objective:  Extract Git Repository Configuration
        Parameters: None
        Returns:    True (bool)
    
    configure_parameter(value: dict = None) -> list
        Objective:  Configure User-Input Parameter
        Parameters:
            value (dict): Parameter value
        Returns:    True (bool)
    
    display_help(argparser: argparse.ArgumentParser = None) -> bool
        Objective:  Displaying Help
        Parameters:
            argparser (argparse.ArgumentParser): Argument Parser
        Returns:    sys.exit( False )
    
    export_config(content: str = None, dataset: object = typing.Any) -> bool
        Objective:  Export Configuration
        Parameters:
            content (str): JSON Configuration
            dataset   (object): JSON Indent & Filepath
        Returns:    True (bool)
    
    extend_config(project: dict = None) -> bool
        Objective:  Extending Script Configuration
        Parameters:
            project (dict): Project Configuration
        Returns:    bool (True)
    
    get_version(config_file: str = None) -> str
        Objective:  Get Package Version (.package file)
        Parameters:
            configfile (str): Parent directory
        Returns:    version (str)
    
    import_config(srcfile: str = None, spaces: int = 4) -> bool
        Objective:  Import Configuration
        Parameters:
            srcfile (str): JSON Configuration File (resource)
            spaces (int): JSON Configuration Indentation (default: 4)
        Returns:    False (bool) | json_config (str)
    
    inspect_parameter(index: str = None, target: str = None) -> bool | dict
        Objective:  Inspect Parameter/Argument Value
        Parameters:
            index (str): Parameter/Argument Name
            content (str): Parameter/Argument Value
        Returns:    param (dict)
    
    list_config(json_config: dict = None) -> bool
        Objective:  Listing Script Configuration
        Parameters:
            json_config (dict): Script Configuration (default: None)
        Returns:    sys.exit()
    
    list_helper() -> bool
        Objective:  Displaying Custom Help
        Parameters: None
        Returns:    bool (True)
    
    load_assets(srcfile: str = 'project.json', project: dict = None) -> dict
        Objective:  Loading Custom Configuration
        Parameters:
            srcfile (str): JSON Configuration File (resource)
            project (dict): Project Configuration
        Returns:    True (bool)
    
    load_buckets() -> dict
        Objective:  Loading Custom Configuration
        Parameters: None
        Returns:    True (bool)
    
    load_config(srcdict: dict = None, srcfile: str = None, project: str = None, bucket: str = None) -> dict
        Objective:  Loading Script Configuration
        Parameters:
            srcdict (dict): Source Dictionary (default: None)
            srcfile (str): JSON Configuration File (resource)
            project (str): Project Configuration (default: None)
            bucket (str): Bucket Configuration (default: None)
        Returns:    srcdict (dict)
    
    load_project() -> dict
        Objective:  Configure Project Paths
        Parameters: None
        Returns:    project (dict)
    
    load_script(srcfile: str = None, json_config: dict = None) -> list
        Objective:  Correcting execution context
        Parameters:
            srcfile (str): Script Configuration File (resource)
            json_config (dict): Script Configuration (default: None)
        Returns:   List [ input_parser, input_args, rouge_args, config ]
    
    print_divisor(character='-', length=80) -> str
        Objective:  Display Section Divisor (character * length)
        Parameters:
            character (str): Divisor Character (default: '-')
            length (int): Divisor Length (default: 80)
        Returns:    True (bool)
    
    read_version(config_file: str = None) -> str
        Objective:  Read Package Version (.package file)
        Parameters:
            configfile (str): Parent directory
        Returns:    version (str)
        Reference:  https://packaging.python.org/en/latest/guides/
                    single-sourcing-package-version/
    
    search_config(trgconf: dict = None, target: str = None, pathway: str = None) -> str
        Objective:  Search Dict-Key Pathway
        Parameters:
            trgconf (dict): Target Configuration
            target (str): Search Content
            pathway (str): Pathway to target configuration
        Returns:    content (str)
    
    update_config(trgconf: dict = None, target: str = None, replace: str = None)
        Objective:  Update Configuration (Dict-Key)
        Parameters:
            trgconf (dict): Target Configuration
            target (str): Search Content
            replace (str): Replace Content
        Returns:    None

DATA
    __dot__ = '.'
    __empty__ = ''
    __space__ = ' '
    config = {}
    repo = <git.repo.base.Repo '.repos/devops/framework/wo...
    version = {}

FILE
    core/core_module.py
```