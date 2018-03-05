from distutils.core import setup

requirements = [
    'django==2.0.2',
    'bitshares==0.1.11',
    'graphenelib==0.5.9',
    'social-auth-app-django==2.1.0'
]

setup(
    name='utschool-faucet',
    version='1.0',
    url='https://github.com/u-transnet/utschool-faucet',
    license='MIT',
    author='Ilya Shmelev',
    author_email='ishmelev23@gmail.com',
    description='Faucet for UT-SCHOOL project',
    requires=requirements
)