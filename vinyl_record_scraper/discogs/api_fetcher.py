import yaml
import requests
import json
import time

from discogs.api_config import base_url, discogs_endpoints

def retrieve_discogs_credentials(path_to_credentials_file: str) -> dict:
    with open(path_to_credentials_file, "r") as creds:
        try:
            file_values = yaml.safe_load(creds)
            credentials = file_values['discogs-api']
        except yaml.YAMLError as exc:
            raise(exc)
        return credentials

class DiscogsAPIFetcher:
    """
    Class to perform requests to the discogs HTTPS endpoint
    """
    def __init__(self, path_to_credentials_file):
        self.credentials = retrieve_discogs_credentials(path_to_credentials_file=path_to_credentials_file)
        self.base_url = base_url
        self.endpoints = discogs_endpoints

    def _implement_rate_limiting(self, response_headers: dict):
        if int(response_headers['X-Discogs-Ratelimit-Remaining']) <= 10:
            time.sleep(60)
        pass

    def _make_request(self, endpoint_name: str, request_params: dict):
        request_url = self.base_url + self.endpoints[endpoint_name].format(**request_params)
        request_params.update(self.credentials)
        response = requests.get(url=request_url, params=request_params)
        self._implement_rate_limiting(response_headers=response.headers)
        return response

    def retrieve_collection(self, endpoint_name: str, request_params: dict):
        accumulated_items = []
        page_number = 1
        all_items_pulled = False
        while not all_items_pulled:
            request_params['page'] = page_number
            response = self._make_request(endpoint_name=endpoint_name, request_params=request_params)
            if response.ok:
                response_json = json.loads(response.text)
            else:
                raise ValueError('API request failed with: %s'%response.text)
            accumulated_items.extend(response_json['releases'])
            if response_json['pagination']['pages'] == page_number:
                all_items_pulled = True
            else:
                page_number += 1
        return accumulated_items
