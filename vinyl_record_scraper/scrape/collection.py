import json

from discogs.api_fetcher import DiscogsAPIFetcher


def scrape_record_collection(username: str, folder_id: int, file_name: str, sort_key="artist"):
    """
    Pipeline to retrieve a record collection of a given Discogs user
    :param username: Discogs username
    :param folder_id: A collection is arranged into folders.
    Every user has two permanent folders already: 0 is the "all" folder, 1 is the "uncategorized folder.
    :param file_name: Name of the JSON file where the data will be written to
    :param sort_key: The key on which we want to sort the results. Valid sort keys are:
    - label
    - artist
    - title
    - catno
    - format
    - rating
    - added
    - year
    """
    collection_request_params = {
        "username": username,
        "folder_id": folder_id,
        "sort": sort_key
    }
    fetcher = DiscogsAPIFetcher(path_to_credentials_file='config/credentials.yaml')
    collection = fetcher.retrieve_collection(endpoint_name="collection_releases",
                                             request_params=collection_request_params)
    with open(f'../data/{file_name}.json', 'w') as f:
        json.dump(collection, f)


if __name__ == "__main__":
    scrape_record_collection(username="le_yems", folder_id=0, file_name="collections/raw/le_yems")
