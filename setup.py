from setuptools import setup, find_packages

setup(
    name='anp_city_extract',
    version='1.0.0',
    url='https://github.com/robsonzagrejr/anp_city_extract',
    author='Robson Zagre Júnior',
    author_email='r.zagre.jr@gmail.com',
    description='Simple ANP info stract for UFSC Probabilidade e Estatistica class'
    packages=find_packages(),    
    install_requires=[
        Unidecode >=1.1.1,
        beautifulsoup4 >=4.9.3,
        html5lib >=1.1,
        lxml >=4.5.2,
        pandas >=1.0.1,
        requests >=2.23.0,
    ],
)
