# setup.py
""" setup.py is used by pip to install the package. """

import setuptools

setuptools.setup(
    name="Rehearsify",
    version="1.0.0",
    description="Programme to rehearse words",
    entry_points = {
        'console_scripts':[
            'Rehearsify=scripts.command_line:script_rehearsify',
            'FindDuplicates=scripts.command_line:script_find_duplicates',
            'Statistics=scripts.command_line:script_compute_statistics' ]},
    packages=setuptools.find_packages('')
)
