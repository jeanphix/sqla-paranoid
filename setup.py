from setuptools import find_packages, setup


with open('README.rst', 'r') as f:
    setup(
        name='sqla-paranoid',
        version='0.1.1',
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
        tests_require=[
          'psycopg2',
        ],
        test_suite="paranoid.tests",
        license='MIT',
    )
