import os
import cv2


def video2frames(pathIn='',
                 pathOut='',
                 display_video_info=False,
                 extract_time_points=None,
                 initial_extract_time=0,
                 end_extract_time=None,
                 extract_time_interval=1,
                 output_prefix='frame',
                 jpg_quality=100,
                 isColor=True):

    cap = cv2.VideoCapture(pathIn)
    n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    dur = n_frames/fps

    if display_video_info:
        print("Number of frames: {}".format(n_frames))
        print("Frames per second (FPS): {}".format(fps))

    elif extract_time_points is not None:
        if max(extract_time_points) > dur:
            raise NameError(
                'the max time point is larger than the video duration....')
        try:
            os.mkdir(pathOut)
        except OSError:
            pass
        success = True
        count = 0
        while success and count < len(extract_time_points):
            cap.set(cv2.CAP_PROP_POS_MSEC, (1000*extract_time_points[count]))
            success, image = cap.read()
            if success:
                if not isColor:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(os.path.join(pathOut, "{}_{:06d}.jpg".format(output_prefix, count+1)),
                            image, [int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])
                count = count + 1

    else:
        if initial_extract_time > dur:
            raise NameError(
                'initial extract time is larger than the video duration....')
        if end_extract_time is not None:
            if end_extract_time > dur:
                raise NameError(
                    'end extract time is larger than the video duration....')
            if initial_extract_time > end_extract_time:
                raise NameError(
                    'end extract time is less than the initial extract time....')

        if extract_time_interval == -1:
            if initial_extract_time > 0:
                cap.set(cv2.CAP_PROP_POS_MSEC, (1000*initial_extract_time))
            try:
                os.mkdir(pathOut)
            except OSError:
                pass
            print('Converting a video into frames......')
            if end_extract_time is not None:
                N = (end_extract_time - initial_extract_time)*fps + 1
                success = True
                count = 0
                while success and count < N:
                    success, image = cap.read()
                    if success:
                        if not isColor:
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        cv2.imwrite(os.path.join(pathOut, "{}_{:06d}.jpg".format(output_prefix, count+1)), image, [
                                    int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                        count = count + 1
            else:
                success = True
                count = 0
                while success:
                    success, image = cap.read()
                    if success:
                        if not isColor:
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        cv2.imwrite(os.path.join(pathOut, "{}_{:06d}.jpg".format(output_prefix, count+1)), image, [
                                    int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                        count = count + 1

        elif extract_time_interval > 0 and extract_time_interval < 1/fps:
            raise NameError(
                'extract_time_interval is less than the frame time interval....')
        elif extract_time_interval > (n_frames/fps):
            raise NameError(
                'extract_time_interval is larger than the duration of the video....')

        else:
            try:
                os.mkdir(pathOut)
            except OSError:
                pass
            print('Converting a video into frames......')
            if end_extract_time is not None:
                N = (end_extract_time - initial_extract_time) / \
                    extract_time_interval + 1
                success = True
                count = 0
                while success and count < N:
                    cap.set(cv2.CAP_PROP_POS_MSEC, (1000 *
                                                    initial_extract_time+count*1000*extract_time_interval))
                    success, image = cap.read()
                    if success:
                        if not isColor:
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        cv2.imwrite(os.path.join(pathOut, "{}_{:06d}.jpg".format(output_prefix, count+1)), image, [
                                    int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                        count = count + 1
            else:
                success = True
                count = 0
                while success:
                    cap.set(cv2.CAP_PROP_POS_MSEC, (1000 *
                                                    initial_extract_time+count*1000*extract_time_interval))
                    success, image = cap.read()
                    if success:
                        if not isColor:
                            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        cv2.imwrite(os.path.join(pathOut, "{}_{:06d}.jpg".format(output_prefix, count+1)), image, [
                                    int(cv2.IMWRITE_JPEG_QUALITY), jpg_quality])     # save frame as JPEG file
                        count = count + 1
