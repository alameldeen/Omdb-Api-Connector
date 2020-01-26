# -*- coding: utf-8 -*-
{
    'name': "OMDB API Connector",

    'summary': "OMDB API Connector",

    'author': "Waell Ahmed",

    'website': "",

    'category': 'Test',

    'version': '0.1',

    'depends': [
        'base',
        'purchase',
        'account',
    ],

    'data': [
        'data/data.xml',

        'security/groups.xml',
        'security/ir.model.access.csv',

        'views/omdb_type_view.xml',
        'views/omdb_api_key_view.xml',
        
        'wizards/omdb_search_view.xml',

        'menus.xml',
    ],

    'demo': [

    ],

    'external_dependencies': {
        'python': ['omdb'],
    },

    'installable': True,
    'auto_install': False,
    'application': True,
}
