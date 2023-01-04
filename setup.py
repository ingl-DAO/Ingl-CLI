from setuptools import setup, find_packages
from src.cli_state import CLI_VERSION
setup(
    name = 'ingl',
    version = CLI_VERSION,
    description = "A command line interface for interacting with Ingl-DAO Program Instructions",
    author = 'Ingl-Labs',
    author_email = 'admin@ingl.io',
    url = 'https://www.ingl.io',
    packages = find_packages(),
    install_requires = [
        'Click',
        'asyncclick',
        'solana',
        'borsh_construct',
        'base58',
        'rich',
        'ledgerblue',
        ],
    entry_points = '''
    [console_scripts]
    ingl=src.ingl_cli:entry
    '''
)