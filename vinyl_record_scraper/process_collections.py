import pandas as pd
import json
import os

def _flatten_record_dictionary(record_dict: dict) -> dict:
    """Flatten the 'basic_information' field of a release from a user's collection"""
    basic_info = record_dict['basic_information']
    release_url = basic_info['resource_url']
    release_title = basic_info['title']
    artist_names = [artist['name'] for artist in basic_info['artists']]
    artist_ids = [artist['id'] for artist in basic_info['artists']]
    release_year = basic_info['year']
    label_ids = [label['id'] for label in basic_info['labels'] if label['entity_type_name'] == 'Label']
    formats = [record_format['name'] for record_format in basic_info['formats']]
    genres = basic_info['genres']
    styles = basic_info['styles']
    output = {'release_url': release_url, 'title': release_title, 'artist_names': artist_names,
              'artist_ids': artist_ids, 'release_year': release_year, 'label_ids': label_ids,
              'release_formats': formats, 'genres': genres, 'styles': styles}
    return output


def _create_flat_collection_table(collection: dict) -> pd.DataFrame:
    """Flatten collection JSON and store it as a DataFrame"""
    flat_collection = []
    for item in collection:
        flat_item = {'id': item['id'], 'date_added': item['date_added'], 'rating': item['rating']}
        flat_item.update(_flatten_record_dictionary(item))
        flat_collection.append(flat_item)
    return pd.DataFrame(flat_collection)

def transform_raw_files_to_flat_table(path_to_raw_files_dir: str):
    dfs_to_append = []
    for file in os.listdir(path_to_raw_files_dir):
        if file.endswith(".json"):
            with open(os.path.join(path_to_raw_files_dir, file), 'r') as f:
                collection = json.load(f)
            df = _create_flat_collection_table(collection=collection)
            df['username'] = file.replace('.json', '')
            dfs_to_append.append(df)
    return pd.concat(objs=dfs_to_append, axis=0, ignore_index=True)


if __name__ == "__main__":
    df = transform_raw_files_to_flat_table(path_to_raw_files_dir='../data/collections/raw/')
    df.to_csv(path_or_buf='../data/collections/flat/collections.csv', index=False)