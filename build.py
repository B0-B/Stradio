#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Compiles the app to a system executable (OS dependent)
'''

from pathlib import Path
from os import path, system, remove, rmdir

# paths
__root__ = Path(__file__).parent
iconPath = __root__.joinpath('radio.ico')
scriptPath = __root__.joinpath('main.py')
buildPath = __root__.joinpath('bin/')

print(f'Check pyinstaller module ...')
system('pip install pyinstaller')
print(f'build {scriptPath} to {buildPath}...')
pyinstallerString = f'pyinstaller -F -n stradio --noconsole --distpath="{buildPath}" -i {iconPath} {scriptPath}'
system(pyinstallerString)
__root__.joinpath('stradio.spec').unlink()
buildPath.rmdir()
print('Successfully created executable!')