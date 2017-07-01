import setuptools


setuptools.setup(name='site-changer-bot',
                 version=0.1,
                 description='Telegram Site Checker Bot',
                 long_description=open('README.md').read().strip(),
                 author='Jordy Ferreira',
                 author_email='jordyfgomes@gmail.com',
                 url='http://path-to-my-packagename',
                 # packages=['sitechangerbot']
                 py_modules=['sitechangerbot'],
                 entry_points={
                    'console_scripts':[
                        'sitechangerbot = sitechangerbot.bot:main'
                        ]    
                 },
                 install_requires=['python-telegram-bot','requests','pony','pymysql','python-dotenv','selenium'],
                 license='MIT License',
                 zip_safe=False,
                 keywords='boilerplate package',
                 classifiers=['Packages', 'Boilerplate'])
