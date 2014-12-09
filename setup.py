# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('fb-archive.py', base=base, icon='icons/fb-icon.ico')#, shortcutName='FB Archiv', shortcutDir='DesktopFolder')
    ]

# Change some default MSI options and specify the use of the above defined tables
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "FB Archiv",     # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]fb-archive.exe",   # Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     ),

    ("ProgramMenuhortcut",        # Shortcut
     "ProgramMenuFolder",          # Directory_
     "FB Archiv",     # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]fb-archive.exe",   # Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     ),

    ]
msi_data = {"Shortcut": shortcut_table}
bdist_msi_options = {'data': msi_data}

options = {"bdist_msi": bdist_msi_options,
    }

setup(name='FB Archive',
      version='1.0',
      description='Program for managing Brno Filharmony archive',
      options=options,
      executables=executables
      )

