from setuptools import setup

package_name = 'controle_system'

setup(

    name=package_name,
    version='0.0.1',
    packages=[],
    py_modules=['control_system'],
    install_requires=['setuptools'],
    zip_safe=True,
    author='ItoMasaki',
    author_email='is0449sh@ed.ritsumei.ac.jp',
    maintainer='ItoMasaki,MatsudaYamato',
    maintainer_email='is0449sh@ed.ritsumei.ac.jp','is0476hv@ed.ritsumei.ac.jp',
    keywords=['ROS2'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='control_system using ros2',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'control_system = control_system:main'
        ],
    },
)
