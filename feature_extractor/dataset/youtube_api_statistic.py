# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json
import numpy as np

import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
api_service_name = "youtube"
api_version = "v3"
STEP = 50


def request(id_list):
    api_key = "balabala"
    # api_key = "balabala"
    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=id_list
    )
    response = request.execute()['items']
    processed = []
    for item in response:
        processed.append({
            'id': item['id'],
            'publishedAt': item['snippet']['publishedAt'],
            'title': item['snippet']['title'],
            'description': item['snippet'].get('description'),
            'channelTitle': item['snippet'].get('channelTitle'),
            'tags': item['snippet'].get('tags'),
            'duration': item['contentDetails']['duration'],
            'statistics': item['statistics']
        })
    return processed


def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    video_list = open('video_list').readlines()
    video_list = [item.split('.')[0][:-4] for item in video_list]
    index_list = np.arange(0, len(video_list), STEP).tolist()
    file_count = 0

    for v in index_list:
        print('request: %d - %d lines' % (v, min(v + STEP, len(video_list))))
        id_list = ','.join(video_list[v: min(v + STEP, len(video_list))])
        json_file = open('output_%d.json' % (file_count), 'a')
        file_count = file_count + 1
        chunk = request(id_list)
        json_file.write(json.dumps(chunk, indent=4))


if __name__ == "__main__":
    main()
