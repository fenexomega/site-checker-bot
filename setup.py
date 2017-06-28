import setuptools


setuptools.setup(name='site-changer-bot',
                 version=0.1,
                 description='Python Package Boilerplate',
                 long_description=open('README.md').read().strip(),
                 author='Package Author',
                 author_email='you@youremail.com',
                 url='http://path-to-my-packagename',
                 # packages=['sitechangerbot']
                 py_modules=['sitechangerbot'],
                 entry_points={
                    'console_scripts':[
                        'sitechangerbot = sitechangerbot.bot:main'
                        ]    
                 },
                 install_requires=['python-telegram-bot','requests','pony','pymysql'],
                 license='MIT License',
                 zip_safe=False,
                 keywords='boilerplate package',
                 classifiers=['Packages', 'Boilerplate'])
