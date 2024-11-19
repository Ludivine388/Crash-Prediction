"""
The following code is a CONVERSION TOOL from ROSBAG files to MP4 files and FRAME FOLDER.
This code is specific to:
- rosbag message type : sensor_msgs/CompressedImage 
- msg.format = rgb8; jpeg compressed bgr8

Portions of this code are adapted from:
Maximilian Laiacker 2020
post@mlaiacker.de
with contributions from
Abel Gabor 2019,
Bey Hao Yun 2021
baquatelle@gmail.com,
beyhy94@gmail.com
a.j.blight@leeds.ac.uk

Repository:
https://github.com/mlaiacker/rosbag2video/blob/master/rosbag2video.py
"""

import rosbag
import sys, getopt
import subprocess
import os
from PIL import Image
import io

VIDEO_CONVERTER_TO_USE = "ffmpeg" # or "avconv"

def print_help():
    print('rosbag2video.py [--fps 25] [--rate 1] [-o outputfile] [-v] [-s] [-t topic] bagfile1 [bagfile2] ...')
    print()
    print('Converts image sequence(s) in ros bag file(s) to video file(s) with fixed frame rate using',VIDEO_CONVERTER_TO_USE)
    print(VIDEO_CONVERTER_TO_USE,'needs to be installed!')
    print()
    print('--fps   Sets FPS value that is passed to',VIDEO_CONVERTER_TO_USE)
    print('        Default is 25.')
    print('-h      Displays this help.')
    print('--ofile (-o) sets output file name.')
    print('--of  sets output folder name.')
    print('--rate  (-r) You may slow down or speed up the video.')
    print('        Default is 1.0, that keeps the original speed.')
    print('--topic (-t) Only the images from topic "topic" are used for the video output.')
    print('--prefix (-p) set a output file name prefix othervise \'bagfile1\' is used (if -o is not set).')


class RosVideoWriter():
    def __init__(self, fps=25.0, rate=1.0, topic="", output_filename ="", output_folder=""):
        self.opt_topic = topic
        self.opt_out_file = output_filename
        self.opt_out_folder = output_folder
        self.rate = rate
        self.fps = fps
        self.opt_prefix= None
        self.t_first={}
        self.t_file={}
        self.t_video={}
        self.p_avconv = {}

    def parseArgs(self, args):
        opts, opt_files = getopt.getopt(args,"hsvr:o:t:p:",["fps=","rate=","ofile=","topic=","prefix="])
        for opt, arg in opts:
            if opt == '-h':
                print_help()
                sys.exit(0)
            elif opt in ("--fps"):
                self.fps = float(arg)
            elif opt in ("-r", "--rate"):
                self.rate = float(arg)
            elif opt in ("-o", "--ofile"):
                self.opt_out_file = arg
            elif opt in ("--of"):
                self.opt_out_folder = arg
            elif opt in ("-t", "--topic"):
                self.opt_topic = arg
            elif opt in ("-p", "--prefix"):
                self.opt_prefix = arg
            else:
                print("opz:", opt,'arg:', arg)

        if (self.fps<=0):
            print("invalid fps", self.fps)
            self.fps = 1

        if (self.rate<=0):
            print("invalid rate", self.rate)
            self.rate = 1

        return opt_files


    # filter messages using type or only the topic we whant from the 'topic' argument
    def filter_image_msgs(self, topic, datatype, md5sum, msg_def, header):      # last 3 arguments needed for bag.connection_filter
        if(datatype=="sensor_msgs/CompressedImage"):
            if (self.opt_topic != "" and self.opt_topic == topic) or self.opt_topic == "":
                print("############# COMPRESSED IMAGE  ######################")
                print()
                print('topic:', topic,' with datatype:', str(datatype))
                print()
                return True;
    
        return False;


    def write_output_video(self, msg, topic, t):
        # no data in this topic
        if len(msg.data) == 0 :
            return
        
        # image folder directory
        if self.opt_out_folder=="":
                    out_folder = f'frame_folders/{self.opt_prefix}' + str('_folder')
        else:
            out_folder = self.opt_out_folder
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)

        # initiate data for this topic
        if not topic in self.t_first :
            self.t_first[topic] = t # timestamp of first image for this topic
            self.t_video[topic] = 0
            self.t_file[topic] = 0
        # if multiple streams of images will start at different times the resulting video files will not be in sync
        # current offset time we are in the bag file
        self.t_file[topic] = (t-self.t_first[topic]).to_sec()
        # fill video file up with images until we reache the current offset from the beginning of the bag file
        while self.t_video[topic] < self.t_file[topic]/self.rate :
            if not topic in self.p_avconv:
                # we have to start a new process for this topic
                if self.opt_out_file=="":
                    out_file = f'mp4_video/{self.opt_prefix}' + str(topic).replace("/", "_")+".mp4"
                else:
                    out_file = self.opt_out_file

                cmd = [VIDEO_CONVERTER_TO_USE, '-v', '1', '-stats', '-r',str(self.fps),'-c','mjpeg','-f','mjpeg','-i','-','-an',out_file]
                self.p_avconv[topic] = subprocess.Popen(cmd, stdin=subprocess.PIPE)
            
            # Save each frame as a PNG file
            try:
                # Convert raw frame data to image using PIL and save as PNG
                image = Image.open(io.BytesIO(msg.data))  # Assuming msg.data is in a format PIL can read, like raw RGB or JPEG
                frame_number = int(self.t_video[topic] * self.fps)
                image.save(f"{out_folder}/frame_{frame_number:06d}.png")
            except Exception as e:
                print(f"Failed to save frame as PNG: {e}")

            # send data to ffmpeg process pipe
            # save file 
            self.p_avconv[topic].stdin.write(msg.data)
            # next frame time
            self.t_video[topic] += 1.0/self.fps

    def addBag(self, filename):
        if not self.opt_prefix:
            # create the output in the same folder and name the output file same as the bag file minus '.bag'
            self.opt_prefix = bagfile[:-4]

        #Go through the bag file
        bag = rosbag.Bag(filename)

        # loop over all topics
        for topic, msg, t in bag.read_messages(connection_filter=self.filter_image_msgs):
            # print(msg.format)          
            # in my case msg.format = rgb8; jpeg compressed bgr8
            if msg.format.find("jpeg")!=-1 :
                self.write_output_video( msg, topic, t)

        if self.p_avconv == {}:
            print("No image topics found in bag:", filename)
        bag.close()


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Please specify ros bag file(s)!')
        print_help()
        sys.exit(1)
    else :
        videowriter = RosVideoWriter()
        try:
            opt_files = videowriter.parseArgs(sys.argv[1:])
        except getopt.GetoptError:
            print_help()
            sys.exit(2)


    # loop over all files
    for files in range(0,len(opt_files)):
        #First arg is the bag to look at
        bagfile = opt_files[files]
        videowriter.addBag(bagfile)
    print("finished")