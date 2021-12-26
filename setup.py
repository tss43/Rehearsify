# setup.py
""" setup.py is used by pip to install the package. """

import setuptools

setuptools.setup(
    name="Rehearsify",
    version="1.0.0",
    description="Programme to rehearse words",
    entry_points = {
        'console_scripts': [
            'Translate=command_line:script_translate' ]},
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'}
)
