from setuptools import setup, find_packages

setup(
    name='devaralan',
    version='1.0.0',
    author='kr1shna4garwal',
    author_email='your-email@example.com',  # Update with your email
    description='Advanced Root domain permutation generator and resolver',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Kr1shna4garwal/devaralan',
    license='Apache License 2.0',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'colorama',
        'dnspython',
        'fake_useragent',
        'tqdm',
        'typer'
        ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Topic :: Internet :: Name Service (DNS)',
    ],
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'devaralan=src.devaralan:main',
        ],
    },
    include_package_data=True,
)
