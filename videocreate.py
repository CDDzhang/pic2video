import os
import cv2
import argparse
import numpy as np
from tqdm import tqdm


def fusion_video(picpath, output, savename, fps):
    fourcc = cv2.VideoWriter_fourcc(*'MPEG')  # e.g. XVID, DIVX, MJPG, X264, mp4v, I420
    path = picpath
    list = sorted(os.listdir(path))
    frame = cv2.imread(path + list[0])
    size = np.shape(frame)[:2]
    size0 = size[0]
    size1 = size[1]
    size = (size1, size0)

    videowriter = cv2.VideoWriter(output + '/' + savename, fourcc, fps, size)
    for i in tqdm(list):
        frame = cv2.imread(path + i)
        videowriter.write(frame)
        # cv2.imshow("frame",frame)
        # cv2.waitKey(20)
    pass
    videowriter.release()
    print('already finished!!')

# def groundtruth_show():


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--picpath', type=str, default='/home/zhangcheng/dataset/tracking/Bird2/img/')
    parser.add_argument('--output', type=str, default='/home/zhangcheng/dataset/tracking/video')
    parser.add_argument('--savename', type=str, default='Bird2.avi')
    parser.add_argument('--fps', type=int, default=24)
    opt = parser.parse_args()
    fusion_video(opt.picpath, opt.output, opt.savename, opt.fps)


