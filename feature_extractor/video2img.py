import os
import subprocess


def video2frames(file_path, img_folder, fps=15):
    os.makedirs(img_folder, exist_ok=True)
    cmd = 'ffmpeg -i ' + file_path + \
        ' -y -f image2 -r ' + str(fps) + ' ' + img_folder + '/img_%06d.jpg'
    FNULL = open(os.devnull, 'w')
    subprocess.Popen(cmd, stdout=FNULL, stderr=subprocess.STDOUT).wait()


def img2log(img_folder, log_path):
    img_list = os.listdir(img_folder)
    img_list = [img_folder + i for i in img_list]
    open(log_path, 'w').write('\n'.join(img_list))
