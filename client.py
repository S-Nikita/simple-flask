from requests import Session

class TestApi:
    def __init__(self, api_url):
        self.api_url = api_url
        self.session = Session()

    def _call(self, http_method, api_method, json_obj=None):
        url = f'{self.api_url}/{api_method}/'
        
        response = self.session.request(http_method, url, json=json_obj).json()

        print(response)

        


    def create_ad(self, title, description, author):
        json_obj = {
            'title': title,
            'description': description,
            'author': author
        }

        http_method = 'POST'
        api_method = 'create_ad'

        self._call(http_method, api_method, json_obj)

    def delete_ad(self, id):
        json_obj = {
            'id': id,
        }

        http_method = 'DELETE'
        api_method = 'delete_ad'

        self._call(http_method, api_method, json_obj)

    def get_ads(self):
        http_method = 'GET'
        api_method = 'ads'

        self._call(http_method, api_method)

create_new_ad = TestApi('http://127.0.0.1:5000')
# create_new_ad.create_ad('Title3', 'description3', 'author3')
create_new_ad.delete_ad(3)
# create_new_ad.get_ads()