import setuptools


setuptools.setup(name='site-checker-bot',
                 version=0.1,
                 description='Telegram Site Checker Bot',
                 long_description=open('README.md').read().strip(),
                 author='Jordy Ferreira',
                 author_email='jordyfgomes@gmail.com',
                 url='http://path-to-my-packagename',
                 packages=['sitecheckerbot'],
                 entry_points={
                    'console_scripts':[
                        'sitecheckerbot = sitecheckerbot.bot:main'
                        ]    
                 },
                 data_files=[
                    ('/etc/', ['sitecheckerbot.conf'])
                    ],
                 install_requires=['pillow','python-telegram-bot','requests','pony','pymysql','python-dotenv','selenium'],
                 license='MIT License',
                 zip_safe=True,
                 keywords='bot telegram site checker',
                 classifiers=['site', 'telegram'])
