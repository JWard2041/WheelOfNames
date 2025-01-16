import os
import sys

def resource_path(relative_path):
    """Get the absolute path to a resource, works for PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        # If running as a PyInstaller executable
        return os.path.join(sys._MEIPASS, relative_path)
    # If running as a normal Python script
    return os.path.join(os.path.abspath("."), relative_path)
