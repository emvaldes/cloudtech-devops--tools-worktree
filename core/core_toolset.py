""" Core Module: Custom Toolset """

import os
import re

from datetime import datetime
import humanize

timestamp = f"{ datetime.now():%y%m%d }".strip()

## ----------------------------------------------
def bucket_sizetype(
        bucket: str=None
    ) -> int:
    """
    Objective:  Identify Size-Type
    Parameters: bucket
    Returns:    int (natural_size)
    Documentation:
        Reference:  https://stackoverflow.com/a/15485265
        Package:    https://pypi.org/project/humanize
    Requirements:
        python -m pip install --upgrade humanize
        import humanize
    """

    natural_size = humanize.naturalsize( bucket )
    # binary_size = humanize.naturalsize( bucket , binary=True)

    return natural_size

## ----------------------------------------------
def name_iterator (
        location: str=os.getcwd(),
        file_name: str="file",
        file_type: str='',
        datestamp: bool=True
    ) -> str:
    """
    Objective: Ensure unique file naming
    Parameters:
        location (str): File location (default: os.getcwd())
        file_name (str): File name prefix (default: file)
        file_type (str): File type suffix (default: empty string)
        datestamp (str): Include module date-stamp (pattern)
    Returns: string
    """

    if datestamp is True:
        regex = r'^\w+-(\d{6})-(\d{2})(\.\w+)?$'
        index = 2
        name = f"{ file_name.strip() }-{ timestamp }"
    else:
        regex = r'^\w+-(\d{2})(\.\w+)?$'
        index = 1
        name = file_name.strip()
    ## Parsing file type
    if len( file_type.strip() ) > 0:
        file_type = f".{ file_type.strip() }"
    else:
        pass
    ## Setup file object
    file = {
        "name": os.path.join(
            str( location ).strip(),
            name
        ),
        "type": file_type,
        "version": "00"
    }
    files = sorted( os.listdir( location ) )
    ## Filter files by regex
    files = [ file for file in files if re.match( regex, file ) ]
    for item in files:
        match = re.search( regex, item )
        if match:
            counter = int( match.group( index ) )
            file['version'] = str( counter + 1 ).zfill( 2 )
        else:
            pass
    sufix = f"{ file['version'] }{ file['type'] }"
    file['path'] = f"{ file['name'] }-{ sufix }"

    return file['path']

## ----------------------------------------------
def unit_test( value: False ) -> True | False:
    """
    Objective:  Unit Testing function
    Parameters: value (bool) -> False
    Returns:    value (bool)
    """

    return value
