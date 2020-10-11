from setuptools import setup, find_packages

setup(
    name='anp_city_extract',
    version='1.0.0',
    url='https://github.com/robsonzagrejr/anp_city_extract',
    author='Robson Zagre Júnior',
    author_email='r.zagre.jr@gmail.com',
    description='Simple ANP info stract for UFSC Probabilidade e Estatistica class'
    packages=['anp_city_extract'],
    install_requires=[
        'unidecode',
        'pandas',
        'requests',
        'lxml',
        'beautifulsoup4'
    ]
)
