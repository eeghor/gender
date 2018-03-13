from setuptools import setup

setup(name='gender',
      version='0.0.1',
      description='Get gender from name and email address',
      classifiers=[
      	'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6.4',
        'Intended Audience :: Science/Research'
      ],
      url='https://github.com/i9k/gender',
      author='Igor Korostil',
      author_email='eeghor@gmail.com',
      license='MIT',
      install_requires=['json', 'unidecode'],
      include_package_data=True,
      keywords='gender name email detection',
      zip_safe=False)