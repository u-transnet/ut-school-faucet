from distutils.core import setup

requirements = [
    'django==2.0.2',
    'bitshares==0.1.11',
    'graphenelib==0.5.9',
    'social-auth-app-django==2.1.0',
    'vk==2.0.2',
    'google-auth==1.4.1',
    'google-auth-httplib2==0.0.3',
    'google-api-python-client==1.6.5',
    'facebook-sdk==2.0.0',
    'django-heroku',
    'gunicorn'
]

if __name__ == '__setup__':
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
