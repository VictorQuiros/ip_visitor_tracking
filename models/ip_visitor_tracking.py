# ip_visitor_tracking.py
import requests
from odoo import models, fields, api

class IPVisitorTracking(models.Model):
    _name = 'ip.visitor.tracking'
    _description = 'Geolocalización de visitantes web'

    ip_address = fields.Char(string='Dirección IP', required=True)
    country = fields.Char(string='País')
    city = fields.Char(string='Ciudad')
    longitude = fields.Float(string='Longitud')
    latitude = fields.Float(string='Latitud')
    isp = fields.Char(string='Proveedor de Servicios')
    organization = fields.Char(string='Organización')
    visit_time = fields.Datetime(string='Hora de la Visita', default=fields.Datetime.now)
    api_key = fields.Char(string='Clave API')

    def action_register_visitor(self):
        if not self.api_key:
            return {'warning': {'title': 'Error', 'message': 'Introduzca una clave API válida'}}
        
        # Usar una IP de prueba
        ip = '8.8.8.8'  # Google DNS como IP de prueba
        
        try:
            # Consultar la API y crear el registro
            url = f'https://api.ipgeolocation.io/ipgeo?apiKey={self.api_key}&ip={ip}'
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                self.create({
                    'ip_address': ip,
                    'country': data.get('country_name'),
                    'city': data.get('city'),
                    'longitude': float(data.get('longitude', 0.0)),
                    'latitude': float(data.get('latitude', 0.0)),
                    'isp': data.get('isp'),
                    'organization': data.get('organization'),
                    'visit_time': fields.Datetime.now(),
                    'api_key': self.api_key
                })
                return {'type': 'ir.actions.client', 'tag': 'reload'}
            else:
                return {'warning': {'title': 'Error', 'message': 'Error al consultar la API'}}
        except Exception:
            return {'warning': {'title': 'Error', 'message': 'Error de conexión'}}