import json
import numpy as np
import matplotlib.pyplot as plt

'''
def cmp(e):
    likeCount = int(e.get('likeCount') or 0)
    viewCount = int(e.get('viewCount') or 0)
    commentCount = int(e.get('commentCount') or 0)
    return commentCount


json_data = json.load(open('video_details_info.json'))
processed = [{
    'id': item['id'],
    'duration': item['duration'],
    'viewCount': item['statistics'].get('viewCount') or 0,
    'likeCount': item['statistics'].get('likeCount') or 0,
    'commentCount': item['statistics'].get('commentCount') or 0
} for item in json_data]

processed.sort(key=cmp, reverse=True)
open('video_info_commentCount.json', 'w').write(json.dumps(processed))

def intersect(arr1, arr2):
    return len([x for x in arr1 if x in arr2])

json_data_1 = json.load(open('video_info_likeCount.json'))
json_data_2 = json.load(open('video_info_viewCount.json'))
json_data_3 = json.load(open('video_info_commentCount.json'))

json_data_1 = [v['id'] for v in json_data_1]
json_data_2 = [v['id'] for v in json_data_2]
json_data_3 = [v['id'] for v in json_data_3]

open('likeCount_list', 'w').write('\n'.join(json_data_1))
open('viewCount_list', 'w').write('\n'.join(json_data_2))
open('commentCount_list', 'w').write('\n'.join(json_data_3))

likeCount = open('likeCount_list', 'r').readlines()
viewCount = open('viewCount_list', 'r').readlines()
commentCount = open('commentCount_list', 'r').readlines()

#8120 8126 7396
print(intersect(likeCount[0:10000], viewCount[0:10000]))
print(intersect(likeCount[0:10000], commentCount[0:10000]))
print(intersect(viewCount[0:10000], commentCount[0:10000]))

json_data = json.load(open('./dataset_list/video_info_likeCount.json'))[:10000]
time_sum = 0

time_list = []
view_list = []
like_list = []
comm_list = []

for item in json_data:
    time = item['duration']
    minute = 0
    second = 0
    if 'M' in time:
        minute = int(time.split('M')[0][2:])
        second = int(time.split('M')[1][:-1] or 0)
    else:
        second = int(time[2:-1])
    time_list.append(minute * 60 + second)
    view_list.append(int(item['viewCount']))
    like_list.append(int(item['likeCount']))
    comm_list.append(int(item['commentCount']))

stat_list = like_list

m1 = min(stat_list)
m2 = max(stat_list)

print(m1, m2)

plt.hist(stat_list, bins=np.linspace(m1, m2, 1000))
plt.xlabel('like counts')
plt.ylabel('number of videos')
plt.show()
'''

id_list = []
json_data = json.load(open('./dataset_list/video_info_likeCount.json'))[:15000]
for item in json_data:
    id_list.append(item['id'])

open('list', 'w').writelines('\n'.join(id_list))