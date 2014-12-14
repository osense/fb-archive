# -*- coding: utf-8 -*-

## This file is part of fb-archive.

## fb-archive is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.

## fb-archive is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with fb-archive.  If not, see <http://www.gnu.org/licenses/>.

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

options = {"bdist_msi": bdist_msi_options, "build_exe": {"include_msvcr": True, 'include_files': ['libEGL.dll']}
    }

setup(name='FB Archive',
      version='1.0',
      description='Program for managing Brno Filharmony archive',
      options=options,
      executables=executables
      )

