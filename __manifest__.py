{
	'name': 'Chatter Security',
	'description': """Implements better security for chatter to prevent users from sending internal communications to customers
					  """,
	'author': 'Matthew Watkins',
	'depends': ['mail', 'crm'],
	'data': [	
		'views/chatter_security_views.xml',
	],
}