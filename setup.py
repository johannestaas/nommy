import os
from setuptools import setup

# nommy
# A python byte and bit parser inspired by Rust's nom.


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="nommy",
    version="0.3.3",
    description="A python byte and bit parser inspired by Rust's nom.",
    author="Johan Nestaas",
    author_email="johannestaas@gmail.com",
    license="GPLv3",
    keywords="bytes struct nom",
    url="https://github.com/johannestaas/nommy",
    packages=['nommy'],
    package_dir={'nommy': 'nommy'},
    long_description=read('README.rst'),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[],
    # entry_points={
    #     'console_scripts': [
    #         'nommy=nommy:main',
    #     ],
    # },
    # If you get errors running setup.py install:
    # zip_safe=False,
    #
    # For including non-python files:
    # package_data={
    #     'nommy': ['templates/*.html'],
    # },
    # include_package_data=True,
)
