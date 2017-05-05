from setuptools import find_packages, setup


with open('README.rst', 'r') as f:
    setup(
        name='sqla-paranoid',
        version='0.1.0',
        description='Brings transparent soft delete to SQLAlchemy ORM',
        long_description=f.read(),
        author='jean-philippe serafin',
        author_email='serafinjp@gmail.com',
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_requires=[
          'sqlalchemy',
        ],
        test_suite="paranoid.tests",
        license='MIT',
    )
