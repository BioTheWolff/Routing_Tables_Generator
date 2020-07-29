import os
import sys
from subprocess import check_output, SubprocessError

DOCLINES = (__doc__ or '').split("\n")

if sys.version_info[:2] < (3, 6):
    raise RuntimeError("Python version >= 3.6 required.")


MAJOR = 1
MINOR = 0
MICRO = 0
IS_RELEASED = True
VERSION = '%d.%d.%d' % (MAJOR, MINOR, MICRO)


def git_version():
    try:
        rev = check_output(['git', 'rev-parse', 'HEAD'])
        return rev.strip().decode('ascii')
    except (SubprocessError, OSError):
        return "Unknown"


def get_version_info():
    full_version = VERSION
    if os.path.exists('.git'):
        git_revision = git_version()
    else:
        git_revision = "Unknown"

    if not IS_RELEASED:
        full_version += '.dev0+' + git_revision[:7]

    return full_version, git_revision


def write_version_py(filename='rth/version.py'):
    full_version, git_revision = get_version_info()

    content = "# Version file generated by setup.py \n\n" \
              f"short_version = '{VERSION}' \n" \
              f"version = '{VERSION}' \n" \
              f"full_version = '{full_version}' \n" \
              f"git_revision = '{git_revision}' \n" \
              f"release = {str(IS_RELEASED)} \n" \
              "\n\n" \
              f"if not release: \n" \
              f"    version = full_version \n"

    with open(filename, 'w') as f:
        f.write(content)


def return_desc():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description


def setup_package():
    from setuptools import setup
    write_version_py()
    md_desc = return_desc()

    setup(
        name='rth',
        version=get_version_info()[0],
        description='Generates routing tables using network description',
        long_description=md_desc,
        long_description_content_type="text/markdown",

        url='https://github.com/BioTheWolff/RTH',
        project_urls={
            'Source Code': 'https://github.com/BioTheWolff/RTH',
            'Bug Tracker': 'https://github.com/BioTheWolff/RTH/issues',
        },

        author='Fabien Z.',
        author_email='contact.biowolf@gmx.fr',
        maintainer='Fabien Z.',
        maintainer_email='contact.biowolf@gmx.fr',

        license='MIT',
        packages=[
            'rth',
            'rth.core',
            'rth.virtual_building'
        ],
        install_requires=[
            "nettools",
        ],

        classifiers=[
            'Development Status :: 5 - Production/Stable',

            'Intended Audience :: Developers',
            'Intended Audience :: System Administrators',

            'Topic :: Utilities',

            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],

        python_requires='>=3.6',
        zip_safe=False
    )


if __name__ == '__main__':
    setup_package()
