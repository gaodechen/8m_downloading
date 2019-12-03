# Dealing with YouTube-8M Music Video Dataset

After crawling and downloading the MV subset of [YouTube-8M dataset](https://research.google.com/youtube8m/) which contains more than 110k music videos, I decided to remove part of those videos considering of the high cost of time and disk space computing and storing audio/video features (so sad to see optical feature of one single video may cost about 100-200mb disk space).

To this end, statistic data of videos are taken into consideration. Obviously, the videos are usually better with more view counts or comments. We've got statistic data through [YouTube Data API](https://developers.google.com/youtube/v3/docs/), you could find the Python implementation for in `youtube_api_statistic.py`. To avoid OAuth process for users, your own API keys are requested here, just generate one with your Google API account and set it in `api_key` variable.

``` Python
# API_KEY set here
api_key = "balabala"
# Get credentials and create an API client
youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=api_key)

request = youtube.videos().list(
        # set part field on your need
    part="snippet,contentDetails,statistics",
    id=id_list
)
```

# Folders

IDs of videos crawled are listed in `./list_110k` folder, including files separated into chunks, too. We also provide crawling and downloading scripts in [v2m/youtube_8m_downloading](https://github.com/gaodechen/v2m/tree/master/youtube_8m_downloading) folder of this repository by which you could crawl and download any subset of YouTube-8M you want easily. JSON files containing statistic data are not uploaded here due to the file size limit.

We have picked the most popular 15,000 music videos by likeCount as our final dataset, those lists and chunks could be found in `./list_10k5` folder.