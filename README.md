## Note

We need some subsets of YouTube 8m dataset, mainly MVs & ads. However, they're of such large scale, and it was so hard to download them.

I finally choose ECS of huaweicloud, and storage service mounted on ECS in Asia-Singapore district to make it faster downloading original videos.

And here's how I did it.

## Crawler

As 8m dataset doesn't contain original videos, I crawled video ids using downloadcategoryids.sh in [youtube-8m-videos-frames](https://github.com/gsssrao/youtube-8m-videos-frames), which took the whole day.

Then I split it into some chunks as it's too slow to download the whole id list in one process.

To make it a multiprocess downloader, I simply applied nohup command here. You could use ``multi_process_download.sh`` here to generate several background processes of ``download_id_list.sh``.

```
# Usage (you might need to change some arugments):
bash multi_process_download.sh
```

## Links

- [youtube-8m-videos-frames](https://github.com/gsssrao/youtube-8m-videos-frames)
- [youtube-dl](https://github.com/ytdl-org/youtube-dl)
