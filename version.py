#!/usr/bin/env python3
"""
Version management for IdleOutpostClaimer
"""

# Current version of the application
__version__ = "1.0.4"

def get_version():
    """
    Get the current version string
    
    Returns:
        str: Current version number
    """
    return __version__

def get_version_info():
    """
    Get detailed version information
    
    Returns:
        dict: Version information including major, minor, and patch numbers
    """
    parts = __version__.split('.')
    return {
        'major': int(parts[0]) if len(parts) > 0 else 0,
        'minor': int(parts[1]) if len(parts) > 1 else 0,
        'patch': int(parts[2]) if len(parts) > 2 else 0,
        'version_string': __version__
    }