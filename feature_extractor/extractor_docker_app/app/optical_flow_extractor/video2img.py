import os
import subprocess

'''
def video2frames(infile='',
                 outfile='',
                 display_info=False,
                 time_gap=0.5,
                 prefix='frame',
                 quality=100):

    cap = cv2.VideoCapture(infile)
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if display_info:
        print("Number of frames: {}".format(n_frames))
        print("Frames per second (FPS): {}".format(fps))

    if time_gap == -1:
        try:
            os.mkdirs(outfile)
        except OSError:
            return
        success = True
        count = 0
        while success:
            success, image = cap.read()
            if success:
                cv2.imwrite(os.path.join(outfile, "{}_{:06d}.jpg".format(prefix, count+1)), image, [
                            int(cv2.IMWRITE_JPEG_QUALITY), quality])     # save frame as JPEG file
                count = count + 1
    else:
        try:
            os.mkdir(outfile)
        except OSError:
            return
        success = True
        count = 0
        while success:
            cap.set(cv2.CAP_PROP_POS_MSEC, (count*1000*time_gap))
            success, image = cap.read()
            if success:
                cv2.imwrite(os.path.join(outfile, "{}_{:06d}.jpg".format(prefix, count+1)), image, [
                            int(cv2.IMWRITE_JPEG_QUALITY), quality])     # save frame as JPEG file
                count = count + 1
'''


def video2frames(file_path, img_folder):
    try:
        os.makedirs(img_folder)
    except OSError:
        pass
    cmd = 'ffmpeg -i ' + file_path + ' -y -f image2 -r 2 ' + img_folder + '/img_%06d.jpg'
    FNULL = open(os.devnull, 'w')
    subprocess.Popen(cmd, stdout=FNULL, stderr=subprocess.STDOUT)

