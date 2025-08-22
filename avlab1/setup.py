import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'avlab1'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*'))
    ],
    install_requires=['setuptools'],
    py_modules=['markers','labfunctions'],
    zip_safe=True,
    maintainer='alex',
    maintainer_email='jlopezm@utec.edu.pe',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'test_fkine = avlab1.test_fkine:main',
        	'command_gazebo = avlab1.command_gazebo:main',
        ],
    },
)
