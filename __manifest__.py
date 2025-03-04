# ip_visitor_tracking/__manifest__.py
{
    'name': 'ip_visitor_tracking',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Integración con API de ipgeolocation para geolocalización de visitantes',
    'description': """
    Módulo personalizado en Odoo 16 Community para obtener información sobre la 
    geolocalización de los visitantes de la web oficial. Utiliza la API de la plataforma gratuita 
    https://app.ipgeolocation.io para registrar la geolocalización del visitante a través de un 
    formulario.
    """,
    'author': 'Víctor Quirós',
    'depends': ['base', 'website'],
    'data': [
        'views/ip_visitor_tracking_views.xml',
        'security/ir.model.access.csv',
    ],
    'icon': '/ip_visitor_tracking/static/description/icon.png',
    'installable': True,
    'application': False,
}
