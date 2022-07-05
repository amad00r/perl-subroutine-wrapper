from setuptools import setup, find_packages

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''

setup(
    name='perlsub',
    version='0.0.1',
    author='amado0r (Amadeu Moya Sardà)',
    author_email='<amadeumosar@gmail.com>',
    license='MIT',
    description='A Python wrapper for Perl subroutines',
    long_description_content_type='text/markdown',
    long_description=readme(),
    packages=find_packages(),
    install_requires=['jinja2'],
    keywords=['python', 'perl', 'wrapper'],
    url='https://github.com/amad00r/perl-subroutine-wrapper',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ]
)