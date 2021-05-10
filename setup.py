from setuptools import setup, find_packages

setup(
    name='textalyzer',
    version='0.6.1',
    author='Ruben Peters',
    url='https://github.com/rubenpeters91/textalyzer',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'gunicorn',
        'spacy',
        'numpy',
        'wordcloud',
        'wikipedia'
    ],
    entry_points={
        'console_scripts': ['run_textalyzer=textalyzer.__init__:main']
    },
)
