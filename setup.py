from setuptools import setup, find_packages

setup(
    name='django-receipts',
    version='0.1.4',
    description='Django app for verifying web app receipts',
    long_description=open('README.rst').read(),
    author='Andy McKay',
    author_email='andym@mozilla.com',
    license='BSD',
    install_requires=['receipts'],
    py_modules=['django_receipts'],
    url='https://github.com/andymckay/django-receipts',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        ],
    )
