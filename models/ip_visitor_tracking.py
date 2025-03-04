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
        """Obtener información de geolocalización basada en la IP proporcionada"""
        if not self.api_key:
            return {'warning': {'title': 'Error', 'message': 'Introduzca una clave API válida'}}
        
        # Usar la IP introducida por el usuario, no una fija
        ip = self.ip_address
        
        try:
            # Consultar la API
            url = f'https://api.ipgeolocation.io/ipgeo?apiKey={self.api_key}&ip={ip}'
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                
                # SOLO actualizar el registro actual, no crear uno nuevo
                self.write({
                    'country': data.get('country_name'),
                    'city': data.get('city'),
                    'longitude': float(data.get('longitude', 0.0)),
                    'latitude': float(data.get('latitude', 0.0)),
                    'isp': data.get('isp'),
                    'organization': data.get('organization'),
                    'visit_time': fields.Datetime.now()
                })
                
                # Retornar sin recargar para evitar crear un nuevo registro
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Éxito',
                        'message': f'Información de geolocalización obtenida para la IP {ip}',
                        'sticky': False,
                        'type': 'success',
                    }
                }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Error',
                        'message': f'Error al consultar la API: {response.status_code}',
                        'sticky': False,
                        'type': 'danger',
                    }
                }
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': f'Error de conexión: {str(e)}',
                    'sticky': False,
                    'type': 'danger',
                }
            }