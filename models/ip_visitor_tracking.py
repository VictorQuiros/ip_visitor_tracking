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

    @api.model
    def create_visitor_record(self, api_key, ip):
        url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            visitor_vals = {
                'ip_address': ip,
                'country': data.get('country_name'),
                'city': data.get('city'),
                'longitude': data.get('longitude'),
                'latitude': data.get('latitude'),
                'isp': data.get('isp'),
                'organization': data.get('organization'),
                'visit_time': fields.Datetime.now(),
            }
            self.create(visitor_vals)
        else:
            raise Exception('Error al obtener información de geolocalización')

