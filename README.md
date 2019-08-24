## Note

We need some subsets of YouTube 8m dataset, mainly MVs & ads. However, they're of such large scale, and it was so hard to download them.

I finally choose ECS of huaweicloud, and storage service mounted on ECS in Asia-Singapore district to make it faster downloading original videos.

## Categories

- videos_ids
    - 8m_0mdxd              8m Music video
        - mv_ids_($id).txt  (chunk)
        - 0mdxd.txt         (full)
    - 8m_011s0.txt          8m Advertising
    - 8m_018ng.txt          8m Television advertisement
    - ads_.txt              url of [advertisement dataset](http://people.cs.pitt.edu/~kovashka/ads/#video)


## Crawler for Original Videos

As 8m dataset doesn't contain original videos, I crawled video ids using downloadcategoryids.sh in [youtube-8m-videos-frames](https://github.com/gsssrao/youtube-8m-videos-frames), which took the whole day.

Then I split it into some chunks as it's too slow to download the whole id list in one process.

To make it a multiprocess downloader, I simply applied nohup command here. And thus we need to split id list into several chunks, here we provided a list of Music videos and chunks splited.

And then, just use ``multi_process_download.sh`` to generate several background processes of ``download_id_list.sh``. It's really an big improvment in speed that I don't need to worry about my ECS cost anymore ...

```
# Usage:
bash multi_process_download.sh
```

BTW, some unknown bugs happended when I use youtube-dl to download some videos, youtube-dl was soooooooo slow in the first two steps downloading web page, and I've fixed it by changing some arguments:

```
youtube-dl -f 'worstaudio,worstvideo' "https://www.youtube.com/watch?v=$line" -o ./videos/"%(id)s_%(format_id)s.%(ext)s"
```

In fact, it's not "worst" word working, it's the ```https``` word ... Isn't that too weird that ```http``` came much slower?

## Links

- [youtube-8m-videos-frames](https://github.com/gsssrao/youtube-8m-videos-frames)
- [youtube-dl](https://github.com/ytdl-org/youtube-dl)
