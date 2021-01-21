from __future__ import print_function
from setuptools import setup, find_packages, Command

import os
import io
import re
import glob
import shutil

from os import listdir
from os.path import isfile, join

AMOD = 'amod_'  # Prefix for analytics package


def find_spec_folder():
    """Return name of folder that contains 'specification.py'"""
    return [f for f in listdir('.') if isfile(join(f, 'specification.py'))][0]


def import_spec():
    """Import SPEC from specification.py and return SPEC and package name"""
    spec_folder = find_spec_folder()
    spec_path = spec_folder + '.specification'
    spec_module = __import__(spec_path, fromlist=["SPEC"])
    return spec_module.SPEC, spec_folder


def long_description():
    """Return readme file as long description for package"""
    here = os.path.abspath(os.path.dirname(__file__))
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        return f.read()


class InitCommand(Command):
    """Rename folder with specification.

    Either current folder name is used with prefix AMOD or a different name
    can be set: python setup.py init --name package_name
    """
    user_options = [('name=', None, "Name of package")]

    def normalize(self, name):
        """Remove spaces, dashes and underscores"""
        if not name:
            _, name = os.path.split(os.getcwd())
        return re.sub(r'[\s\-_]', '', name.lower())

    def adjust_file(self, filename, pkg_name):
        """Replace package/repo names in files"""
        _, repo_name = os.path.split(os.getcwd())
        text = open(filename, 'r').read()
        text = text.replace('analytics-module-template', repo_name)
        text = text.replace(AMOD + 'template', pkg_name)
        with open(filename, 'w') as f:
            f.write(text)

    def initialize_options(self):
        self.name = None

    def finalize_options(self):
        pass

    def run(self):
        """Rename folders and configurations to new package name"""
        new_pkg_name = AMOD + self.normalize(self.name)
        print('new package name:', new_pkg_name)
        os.rename(find_spec_folder(), new_pkg_name)
        self.adjust_file('Dockerfile', new_pkg_name)
        self.adjust_file('.travis.yml', new_pkg_name)
        self.adjust_file(os.path.join(new_pkg_name, 'module.py'), new_pkg_name)


class CleanCommand(Command):
    """Delete all distribution files"""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Delete distribution files"""
        for folder in ['build', 'dist']:
            if os.path.exists(folder):
                print('deleting:', folder)
                shutil.rmtree(folder)
        for egg_file in glob.glob('*egg-info'):
            print('deleting:', egg_file)
            shutil.rmtree(egg_file)


SPEC, PACKAGENAME = import_spec()
PKGSPEC = SPEC['module']

setup(
    name=PACKAGENAME,
    version=PKGSPEC['version'],
    author=PKGSPEC['author'],
    author_email=PKGSPEC['author_email'],
    description=PKGSPEC['description'],
    long_description=long_description(),
    keywords=str("analytics module " + PKGSPEC['name']),
    url=PKGSPEC['url'],
    packages=find_packages(),
    package_data={PACKAGENAME: ['resources/**', 'testdata/**']},
    include_package_data=True,
    install_requires=PKGSPEC['dependencies'] + ["amodule>=1.2.0"],
    zip_safe=False,
    cmdclass={
        'init': InitCommand,
        'clean': CleanCommand,
    },
    license='Apache 2.0',
    platforms=['any'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
