
# services/users/project/test/test_users.py
import json
import unittest

from project.tests.base import BaseTestCase
from project import db
from project.api.models import Losa


def add_cancha(canchan, tipo, preciod, precion):
    cancha = Losa(canchan=canchan, tipo=tipo, preciod=preciod, precion=precion)
    db.session.add(cancha)
    db.session.commit()
    return cancha

class TestUserService(BaseTestCase):
    """Prueba para el servicio users."""
    def test_canchas(self):
        """Asegurando que la ruta /ping se comporta correctamente."""
        response = self.client.get('/canchas/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])

    def test_add_canchas_invalid_json(self):
        """ Asegurando de que se arroje un error si el objeto JSON está vacío."""

        with self.client:
            response = self.client.post(
                '/canchas',
                data=json.dumps({}),
                content_type='application/json',
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_autos_invalid_json_keys(self):
        """Asegurando de que se produce un error si el objeto JSON no tiene los campos completos."""

        with self.client:
            response = self.client.post(
                '/canchas',
                data=json.dumps({
                    'canchan': 'Sintetico'
                }),
                content_type='application/json',

            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload.', data['message'])
        self.assertIn('fail', data['status'])

    def test_add_cancha_duplicate_placa(self):
        """Asegurando de que se haya producido un error si la placa ya existe."""

        with self.client:
            self.client.post(
                '/canchas',
                data=json.dumps({
                    'canchan': 'Sintetico',
                    'tipo': '7x7',
                    'preciod': '40',
                    'precion': '80'}),
                content_type='application/json',
            )
        response = self.client.post(
            '/canchas',
            data=json.dumps({
                'canchan': 'Sintetico',
                'tipo': '7x7',
                'preciod': '40',
                'precion': '80'
            }),
            content_type='application/json',
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Disculpe. Esta placa ya existe.', data['mensaje'])
        self.assertIn('fallo', data['estado'])

    def test_single_canchas(self):
        """ Asegurando de que el usuario individual se comporte correctamente."""
        cancha = add_cancha('Sintetico', '7x7', '40', '80')
        with self.client:
            response = self.client.get(f'/canchas/{cancha.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Sintetico', data['data']['canchan'])
            self.assertIn('7x7', data['data']['tipo'])
            self.assertIn('40', data['data']['preciod'])
            self.assertIn('80', data['data']['precion'])
            self.assertIn('satisfactorio', data['estado'])

    def test_single_cancha_no_id(self):
        """Asegúrese de que se arroje un error si no se proporciona una identificación."""

        with self.client:
            response = self.client.get('/canchas/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('La cancha no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

    def test_single_cancha_incorrect_id(self):
        """Asegurando de que se arroje un error si la identificación no existe."""

        with self.client:
            response = self.client.get('/canchas/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('La cancha no existe', data['mensaje'])
            self.assertIn('fallo', data['estado'])

if __name__ == '__main__':
    unittest.main()



