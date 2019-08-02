from setuptools import setup

package_name = 'controle_system'

setup(

    name=package_name,
    version='0.0.1',
    packages=[],
    py_modules=[
        'controle_system',
        'rotation'
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='ItoMasaki',
    author_email='is0449sh@ed.ritsumei.ac.jp',
    maintainer='ItoMasaki',
    maintainer_email='is0449sh@ed.ritsumei.ac.jp',
    keywords=['ROS2'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='human detection using PoseNet and OpenCV',
    license='Apache License, Version 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'controle_system = controle_system:main',
            'rotation = rotation:main'
        ],
    },
)
