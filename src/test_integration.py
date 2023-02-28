import unittest
import requests

HOST='https://open.spotify.com'

class TestEndpoints(unittest.TestCase):

    def test_endpoints(self):

        for endpoint in ('/user/rosycarina',
                         '/artist/06HL4z0CvFAxyc27GXpf02',
                         '/playlist/4f5ADsjBDpMmN8Ngf4rWZV'
                         ):
            with self.subTest(path=endpoint):

                url = HOST + endpoint
                response = requests.get(url)
                self.assertEqual(response.status_code, requests.codes.ok, msg=f'expected status code {requests.codes.ok}')

if __name__ == '__main__':
    unittest.main()