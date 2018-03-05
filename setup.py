from distutils.core import setup

requirements = [
    'django==2.0.2'
]

setup(
    name='utschool-faucet',
    version='1.0',
    url='https://github.com/u-transnet/utschool-faucet',
    license='MIT',
    author='superpchelka',
    author_email='ishmelev23@gmail.com',
    description='Faucet for UT-SCHOOL project',
    requires=requirements
)
