"""
Flask-srv-dash
-------------

srv-dash Flask extension that sends your server logs
to your srv-dash server.
"""
from setuptools import setup

setup(
    name='Flask-srv-dash',
    version='1.0',
    url='https://github.com/bariyu/srv-dash-flask-ext/',
    license='MIT',
    author='Baran Kucukguzel',
    author_email='kucukguzelbaran@gmail.com',
    description='this extension automatically makes your flask app to log http req/resps to your srv-dash dashboard.',
    long_description=__doc__,
    py_modules=['flask_srv_dash'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'requests',
        'tzlocal'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
