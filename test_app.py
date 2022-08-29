import unittest
from app import app as stripe_app
import time

class TestStripeApp(unittest.TestCase):
    def setUp(self):
        self.app = stripe_app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Stripe Press Shop', response.data)
        self.assertNotIn(b'Hello World', response.data)

    def test_checkout(self):
        for valid_item_id in range(1, 4):
            response = self.app.get('/checkout?item={}'.format(str(valid_item_id)))
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Checkout', response.data)
            self.assertNotIn(b'Stripe Press Shop', response.data)
        
        error_response_item4 = self.app.get('/checkout?item=4') 
        self.assertIn(b'Error', error_response_item4.data)

        error_response_item0 = self.app.get('/checkout?item=0') 
        self.assertIn(b'Error', error_response_item0.data)

    def test_create_payment_intent(self):
        for valid_item_id in range(1, 4):
            response = self.app.post('/create-payment-intent', json={"item":valid_item_id})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'clientSecret', response.data)
            self.assertNotIn(b'The item with the given id does not exist', response.data)

        error_response_item4 = self.app.post('/create-payment-intent', json={"item":4})
        self.assertIn(b'The item with the given id does not exist', error_response_item4.data)


        error_response_item0 = self.app.post('/create-payment-intent', json={"item":0})
        self.assertIn(b'The item with the given id does not exist', error_response_item0.data)

    def test_get_item(self):
        for valid_item_id in range(1, 4):
            response = self.app.get('/items/{}'.format(valid_item_id))
            assert b'item' in response.data
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'item', response.data)
            self.assertIn(b'amount', response.data)
            self.assertIn(b'title', response.data)
            self.assertIn(b'img', response.data)
            self.assertNotIn(b'error', response.data)
        
        error_response_item4 = self.app.get('/items/4') 
        self.assertIn(b'The item with the given id does not exist', error_response_item4.data)

        error_response_item0 = self.app.get('/items/0') 
        self.assertIn(b'The item with the given id does not exist', error_response_item0.data)

    def test_success(self):
        response = self.app.get('/success')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'payment-success', response.data)            