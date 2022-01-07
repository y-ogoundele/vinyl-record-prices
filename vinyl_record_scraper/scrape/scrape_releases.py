import json
import pickle

from discogs.api_fetcher import DiscogsAPIFetcher


def scrape_release(release_id: int, curr_abbr='EUR'):
    release_request_params = {
        "release_id": release_id,
        "curr_abbr": curr_abbr
    }
    fetcher = DiscogsAPIFetcher(
        path_to_credentials_file='../config/credentials.yaml'
    )
    releases = fetcher.retrieve_release(request_params=release_request_params)
    with open(f'../data/releases/raw/{release_id}.json', 'w') as f:
        json.dump(releases, f)


if __name__ == "__main__":
    with open('../../data/releases/unique_release_ids.pkl', 'rb') as f:
        release_ids = pickle.load(f)
    for release_id in release_ids:
        try:
            scrape_release(release_id=release_id)
        except ValueError:
            print(f'Scraping failed for release number {release_id}')
