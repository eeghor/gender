from setuptools import setup

setup(name='gender',
      version='0.0.1',
      description='Get gender from name and email address',
      classifiers=[
        'Programming Language :: Python :: 3.6.4'
      ]
      url='https://github.com/i9k/gender',
      author='Igor Korostil',
      author_email='eeghor@gmail.com',
      license='MIT',
      install_requires=['json'],
      packages=['funniest'],
      include_package_data=True,
      zip_safe=False)