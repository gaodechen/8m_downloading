import csv

def run(infile):
    list = open('./dataset/original/' + infile).readlines()
    list = [i.replace('\n', '') for i in list]
    list_ = [i.split('.')[0][:-4] for i in list]
    csv_file = csv.writer(open(infile + '.csv', 'w', newline=''))
    csv_file.writerows(zip(['audio_path'], ['feature_path']))
    csv_file.writerows(zip(list, list_))

run('audio_0')
