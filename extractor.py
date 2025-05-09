#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @File     : extractor.py
# @Auther   : Zhang.Yuchen
# @Time     : 2023-10-22
# @Descript : 从一段视频中提取指定的帧数, 并且交错合成这些帧, 并生成用于打印的 pdf 文件, 用于手摇动画机中的动画纸的制作

import os
import re
import argparse
import cv2
import math
import numpy
import img2pdf
from tqdm import tqdm

supported_video_ext = ('.avi', '.mp4')
supported_frame_ext = ('.jpg', '.png')
pdf_print_a4_px     = (3508, 2480)
pdf_print_dpi       = 300
mm_per_inch         = 25.4
bg_color            = 255

class FrameExtractor:
    def __init__(self, video_file, output_dir, frame_ext='.jpg'):
        """Extract frames from video file and save them under a given output directory.

        Args:
            video_file (str)   : input video filename
            output_dir (str)   : output directory where video frames will be extracted
            frame_ext  (str)   : extracted frame file format
        """
        # Check if given video file exists -- abort otherwise
        if os.path.exists(video_file):
            self.video_file = video_file
        else:
            raise FileExistsError("video file {} does not exist.".format(video_file))
        
        # Create output directory for storing extracted frames
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.output_frame_dir = os.path.join(output_dir, 'frames')
        if not os.path.exists(self.output_frame_dir):
            os.makedirs(self.output_frame_dir)
        
        # Get extracted frame file format
        self.frame_ext = frame_ext
        if frame_ext not in supported_frame_ext:
            raise ValueError("Not supported frame file format: {}".format(frame_ext))
        else:
            self.frame_ext = frame_ext
            
        # Capture given video stream
        self.video = cv2.VideoCapture(self.video_file)
        
        # Get video fps
        self.video_fps = self.video.get(cv2.CAP_PROP_FPS)
            
        # Get video size
        self.video_size = (int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                           int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH)))
        
        # Get video length in frames
        self.video_length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.video_second = self.video_length / self.video_fps

    def extract(self, args_frm):
        """Extract video frames with specified parameter

        Args:
            args_frm (int): set the number of extracted frames
        """
        # Sets the number of frames extracted
        if args_frm != -1:
            self.sample_frm = args_frm
        else:
            self.sample_frm = self.video_length
        
        # Set extract process bar
        ext_pbar = tqdm(total=self.video_length)
        ext_pbar.set_description('Extracting frames')

        frame_cnt = 0
        frame_cnt_f = 0
        file_cnt = 0
        success = True

        while success:
            # Get frame
            self.video.set(cv2.CAP_PROP_POS_FRAMES, frame_cnt - 1)
            success, frame = self.video.read()
            
            # Extract frame to file
            curr_frame_filename = os.path.join(self.output_frame_dir, 
                                               "{:08d}{}".format(file_cnt, self.frame_ext))
            cv2.imwrite(curr_frame_filename, frame)
            
            if file_cnt == self.sample_frm - 1:
                break
            
            # Get next frame
            frame_old = frame_cnt
            frame_cnt_f += self.video_length / self.sample_frm
            frame_cnt = math.ceil(frame_cnt_f)
            file_cnt += 1
            
            if frame_cnt_f + (self.video_length / self.sample_frm) > self.video_length - 1:
                frame_cnt = self.video_length - 1

            ext_pbar.update(frame_cnt - frame_old)
        ext_pbar.update()
        ext_pbar.close()

def check_frm_param(s):
    s_ = int(s)
    if (s_ <= 0) and (s_ != -1):
        raise argparse.ArgumentTypeError("Please give a positive number of extract frame number.")
    return s_

def main():
    # Set up a parser for command line arguments
    parser = argparse.ArgumentParser(description="Extract the frames in the video and generate preview "
                                     "video, splice the top half of the frame with the bottom half and "
                                     "generate a printed pdf file.")
    parser.add_argument('-v', '--video', metavar='vidio_file', type=str, required=True,
                        help='Set the video files to be processed')
    parser.add_argument('-o', '--output-root', metavar='output_dir', type=str, default='extracted_frames', 
                        help="Set the root directory for the output video (default: ./extracted_frames)")
    parser.add_argument('-f', '--frame', metavar='frame_count', type=check_frm_param, default=-1,
                        help="The total number of video frames extracted (default: extract all frames)")

    args = parser.parse_args()
    
    # Extract frames from a (single) given video file
    if args.video:
        # Setup video extractor for given video file
        video_basename = os.path.basename(args.video).split('.')[0]
        # Check video file extension
        video_ext = os.path.splitext(args.video)[-1]
        if video_ext not in supported_video_ext:
            raise ValueError("Not supported video file format: {}".format(video_ext))
        # Set extracted frames output directory
        output_dir = os.path.join(args.output_root, 'output_{}'.format(video_basename))
        # Set up video extractor for given video file
        extractor = FrameExtractor(video_file=args.video, output_dir=output_dir)
        # Extract frames
        extractor.extract(args.frame)

if __name__ == '__main__':
    main()
