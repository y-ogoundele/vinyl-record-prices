import json
import os

import pandas as pd


def create_flat_release_table(path_to_release_files: str, path_to_flat_table_file: str):
    """ Read release JSON files, flatten them and extract all relevant information, and store them as a flat table."""
    all_releases = []
    all_flattened_releases = []
    for file in os.listdir(path_to_release_files):
        if file.endswith(".json"):
            with open(os.path.join(path_to_release_files, file), 'r') as f:
                release = json.load(f)
                all_releases.append(release)
    for release in all_releases:
        all_flattened_releases.append(_extract_relevant_features(release=release))
    output_df = pd.DataFrame(all_flattened_releases)
    output_df.to_csv(path_or_buf=path_to_flat_table_file, index=False)


def _extract_relevant_features(release: dict) -> dict:
    keys_to_keep = [
        'id', 'status', 'resource_url', 'title', 'artists_sort', 'num_for_sale', 'date_added', 'lowest_price',
        'released', 'country', 'genres', 'styles', 'estimated_weight', 'blocked_from_sale'
    ]
    flat_release = {key: release.get(key) for key in keys_to_keep}
    flat_release.update(_flatten_release_dict(release))
    return flat_release


def _flatten_release_dict(release: dict) -> dict:
    """Flatten all nested fields within a release JSON file"""
    artist_ids = [artist['id'] for artist in release['artists']]
    labels = [label['id'] for label in release['labels'] if label['entity_type'] == "1"]
    distributed_by = [company['id'] for company in release['companies'] if company['entity_type'] == "9"]
    mastered_by = [company['id'] for company in release['companies'] if company['entity_type'] == "29"]
    formats = [release_format['name'] for release_format in release['formats']]
    vinyl_qty = [int(release_format['qty']) for release_format in release['formats'] if
                 release_format['name'] == 'Vinyl']
    cd_qty = [int(release_format['qty']) for release_format in release['formats'] if release_format['name'] == 'CD']
    haves = release['community']['have']
    wants = release['community']['want']
    rating_count = release['community']['rating']['count']
    rating_avg = release['community']['rating']['average']
    if release.get('videos') is not None:
        n_videos = len(release.get('videos'))
    else:
        n_videos = None
    if release.get('tracklist') is not None:
        n_tracks = len(release['tracklist'])
    else:
        n_tracks = None
    output = {
        'artist_ids': artist_ids, 'label_ids': labels, 'distributor_ids': distributed_by, 'mastered_ids': mastered_by,
        'format_names': formats, 'vinyl_qty': vinyl_qty, 'cd_qty': cd_qty, 'community_haves': haves,
        'community_wants': wants, 'community_rating_count': rating_count, 'community_rating_avg': rating_avg,
        'n_videos': n_videos, 'n_tracks': n_tracks
    }
    return output


if __name__ == "__main__":
    create_flat_release_table(path_to_release_files='../../data/releases/raw/',
                              path_to_flat_table_file='../../data/releases/flat/releases.csv')
