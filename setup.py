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
        'click==8.1.3',
        'asyncclick==8.1.3.4',
        'solana==0.29.0',
        'borsh-construct==0.1.0',
        'base58==2.1.1',
        'rich==13.1.0',
        'ledgerblue==0.1.43',
        ],
    entry_points = '''
    [console_scripts]
    ingl=src.ingl_cli:entry
    '''
)