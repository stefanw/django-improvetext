from distutils.core import setup

setup(
    name='django-improvetext',
    version='0.1.0',
    description='django-improvetext lets users suggest improvements for text fields\
of arbitrary model objects which can be viewed and applied in admin',
    author='Stefan Wehrmeyer',
    author_email='Stefan Wehrmeyer <mail@stefanwehrmeyer.com>',
    url='http://github.com/stefanw/django-improvetext',
    packages = ["improvetext", "lazyinclude.templatetags"],
    package_data={'improvetext': ['templates/improvetext/*.html', 'templates/admin/improvetext/*.html']},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)