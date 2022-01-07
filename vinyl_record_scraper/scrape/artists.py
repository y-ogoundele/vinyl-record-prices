import json
import pickle

from discogs.api_fetcher import DiscogsAPIFetcher


def scrape_artist_releases(artist_id: int, sort_key='year', sort_order='desc'):
    artist_releases_request_params = {
        "artist_id": artist_id,
        "sort": sort_key,
        "sort_order": sort_order
    }
    fetcher = DiscogsAPIFetcher(path_to_credentials_file='../config/credentials.yaml')
    releases = fetcher.retrieve_collection(endpoint_name="artist_releases",
                                           request_params=artist_releases_request_params)
    with open(f'../data/artists/raw/{artist_id}.json', 'w') as f:
        json.dump(releases, f)


if __name__ == "__main__":
    with open('../../data/artists/unique_artist_ids.pkl', 'rb') as f:
        artist_ids = pickle.load(f)
    for artist_id in artist_ids:
        scrape_artist_releases(artist_id=artist_id)
