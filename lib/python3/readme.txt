Instructions for deploying the Python bridge.

Windows:
Copy libfont3-2.1.2-py3.6.egg-info to the <Python path>\Lib\site-packages folder.
Copy libfont3backend.cp36-win_amd64.pyd (in the \windows folder) to the <Python path>\Lib\site-packages folder.
Create a folder called libfont3 under <Python path>\Lib\site-packages folder and copy __init__.py there.

OSX:
Deterimine the path to site-packages folder for your Python installation. For example:
/Library/Frameworks/Python.framework/Versions/<active version>/lib/python<version>/site-packages
Copy libfont3-2.1.2-py3.6.egg-info to that folder.
copy libfont3backend.cpython-36m-darwin.so (in the /osx folder) to that folder.
Create a folder called libfont3 under the above folder and copy __init__.py there.