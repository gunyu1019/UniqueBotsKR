from setuptools import setup

setup(
    name='UniqueBotsKR',
    version='1.2',
    packages=['UniqueBotsKR'],
    url='https://github.com/gunyu1019/UniqueBotsKR',
    license='MIT',
    author='gunyu1019',
    author_email='gunyu1019@yhs.kr',
    description='UniqueBots를 위한 비공식 파이썬 API 레퍼입니다.',
    python_requires='>=3.6',
    long_description=open('README.md', encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=open('requirements.txt', encoding='UTF-8').read(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
