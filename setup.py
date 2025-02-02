from distutils.core import setup
import py2exe

setup(
    windows=[
        {
            "script": "crawler.py",
             "icon_resources": [(1, "icon.ico")] #if you want to use icon
        }
    ],
    options={
        "py2exe": {
            "bundle_files": 1,
            "compressed": True,
            "includes":["selenium","selenium.webdriver", "selenium.webdriver.support.ui","selenium.webdriver.common.by","selenium.webdriver.support", "selenium.webdriver.support.expected_conditions","webdriver_manager","webdriver_manager.chrome"],
            # "dll_excludes": ["w9xpopen.exe", 'msvcr71.dll','MSVCP71.dll', 'msvcp90.dll', 'msvcr90.dll', 'msvcr100.dll', 'msvcp100.dll'],
        }
    },
     zipfile=None,

    )