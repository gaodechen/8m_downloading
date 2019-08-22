# Usage: you could run this separately as a single process,
# or run multi_process tool first to get multiprocess and download chunks faster

txt=".txt"

chunk=$1
echo "downloading chunk from file $chunk ..."

mkdir -p videos

while read line
do
    # change the quality of videos here
    # as merging process of ffmpeg is so slow, that i just download audio & video saparately
    youtube-dl -f 'worstaudio,worstvideo' "https://www.youtube.com/watch?v=$line" -o ./videos/"%(id)s_%(format_id)s.%(ext)s"
done < category-ids/$chunk

echo "$chunk has finished"
