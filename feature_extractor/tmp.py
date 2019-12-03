import csv

infolder = './dataset/list_10k5/'

def run(infile):
    list = open(infolder + infile).readlines()
    list = [i.replace('\n', '') for i in list]
    list_ = [i.split('.')[0][:-4] for i in list]
    csv_file = csv.writer(open(infolder + infile + '.csv', 'w', newline=''))
    csv_file.writerows(zip(['video_path'], ['feature_path']))
    csv_file.writerows(zip(list, list_))

[run('video_' + str(i)) for i in range(0, 15)]
