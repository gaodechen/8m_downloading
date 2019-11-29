from shutil import copyfile
import numpy as np
import csv

'''
f = open('./dataset/video_list')
l = f.readlines()

# audio_format = ['249', '250', '251', '140', '139']
# video_format = ['133', '242', '160', '278', '134', '394']

CHUNK_LINES = 10000
m = np.arange(0, len(l), CHUNK_LINES)
m = np.append(m, len(l))
print(m)

for i in range(0, len(m) - 1):
	f = open('video_' + str(i), 'a+')
	f.writelines(l[m[i]:m[i+1]])
'''

audio_list = [0, 1, 2, 3, 4, 5]
video_list = [0, 1, 2, 3, 4, 5]

src_folder = ''
dst_folder = ''

file_list = ['audio_' + str(i) for i in audio_list] + \
    ['video_' + str(i) for i in video_list]
print(file_list)

for file in file_list:
	lines = open('../dataset/' + file).readlines()
	lines = [item.replace('\n', '') for item in lines]
	[copyfile(src_folder + item, dst_folder + item) for item in lines]
