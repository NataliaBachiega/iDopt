from rest_framework.test import APITestCase


class TestSanity(APITestCase):
    '''
    Um teste bem simples apenas para verificar se os testes estão rodando.
    '''

    def test_sanity(self):
        # Verifica se 1=1, o que é verdade sempre. Isso é só um teste bobo.
        self.assertEqual(1, 1)