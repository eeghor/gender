from setuptools import setup
import os

setup(name='gender',
      version='0.0.16',
      description='Get gender from name and email address',
      long_description='gender from name or email',
      classifiers=[
      	'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Filters"
      ],
      url='https://github.com/eeghor/gender',
      author='Igor Korostil',
      author_email='eeghor@gmail.com',
      license='MIT',
      packages=['gender'],
      install_requires=['unidecode'],
      python_requires='>=3.6',
      package_data={'gender': ['data/*.json']},
      keywords='gender name email')