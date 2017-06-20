"""
Landport
--------------

Python MMO game server framework, you can easy build a virtual room by websocket!
The player can easily chat with other player~
"""
import re
from setuptools import setup

setup(
    name='kengine',
    version='1.0.4',
    url='https://github.com/land-pack/kengine',
    license='MIT',
    author='Frank AK',
    author_email='804048353@qq.com',
    description='MMORPG Game Server Framework (Based on Websocket)',
    long_description=__doc__,
    packages=['kengine',],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'tornado',
        'ujson',
        'futures',
        'redis'
    ],
  
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
