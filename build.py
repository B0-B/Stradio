#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Compiles the app to a system executable (OS dependent)
'''

from pathlib import Path
import shutil

from os import path, system, remove, rmdir

# paths
__root__ = Path(__file__).parent
iconPath = __root__.joinpath('radio.ico')
scriptPath = __root__.joinpath('main.py')
binPath = __root__.joinpath('bin/')
buildPath = __root__.joinpath('build/')

print(f'Check pyinstaller module ...')
system('pip install pyinstaller')
print(f'build {scriptPath} to {binPath}...')
pyinstallerString = f'pyinstaller -F -n stradio --noconsole --onefile --distpath="{binPath}" --add-data "{iconPath};." -i {iconPath} {scriptPath} '
system(pyinstallerString)
__root__.joinpath('stradio.spec').unlink()
shutil.rmtree(buildPath, ignore_errors=False, onerror=None)
print('Successfully created executable!')