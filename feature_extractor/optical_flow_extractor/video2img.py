import os
import subprocess


def video2frames(file_path, img_folder):
    try:
        os.makedirs(img_folder)
    except OSError:
        pass
    cmd = 'ffmpeg -i ' + file_path + ' -y -f image2 -r 2 ' + img_folder + '/img_%06d.jpg'
    FNULL = open(os.devnull, 'w')
    subprocess.Popen(cmd, stdout=FNULL, stderr=subprocess.STDOUT)
