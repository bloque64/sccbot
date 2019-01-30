from setuptools import setup

setup(
    name='cli_sccbot',
    version='1.0',
    py_modules=['cli_sccbot'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        scc=cli_sccbot:cli
    '''
)
