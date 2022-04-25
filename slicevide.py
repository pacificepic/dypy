#!/usr/bin/env python
#coding:utf-8


'''
   音频/视频-拆分为59秒
   author:marker.liu@foxmail.com
   initial date :2021-12-01
'''
__version__='1.0.1'
__author__='alex.liu(marker.liu@foxmail.com)'
__initdate__='2022-03-21'


import datetime
import os
import sys
import time
import re
import json
import requests
import getopt
import ffmpeg
from ffmpy import FFmpeg

def usage():
    print("split video into 59 seconds parts,initial by author {},initdate {}  ".format(__author__,__initdate__))
    print("{} -h --help :help message for usage".format(sys.argv[0]))
    print("{} -v --version: print version info".format(sys.argv[0]))
    print("{} -N --nfile=videourl_list_file :search video list from douyin.com download stream file".format(sys.argv[0]))

def version():
    print("{}".format(__version__))

def splitvideo(srcfilename,savepath):
    probe=None;
    probe = ffmpeg.probe(srcfilename)

    #print("type={}".format(type(probe)))
    #print("PROBE:{}".format(probe))
    s=probe['streams']
    duration=0
    for x in s:
        #print("x:{}".format(type(x)))
        print("index:{},duration:{},codec_type:{},codec_name:{}".format(
            x['index'],x['duration'],x['codec_type'],x['codec_name'])) 
        if (x['codec_type']=='video'):
           duration=x['duration']
    timelen=58
    slicesep=20
    xdu_re=re.compile(r'[0-9]{0,20}')
    int_duration=xdu_re.findall(duration)
    #print("int_duration:{},type:{}".format(int_duration,type(int_duration)))
    cnt=int(int(int_duration[0])/int(slicesep))

    mlist=os.path.split(srcfilename)
    rlist=str(mlist[1]).split('.')
    rfilename=rlist[0]

    print("cnt={}".format(cnt))
    idx=0
    for idx in range(0,cnt):
        xlen=idx*20
        mlen=int(xlen/60)
        slen=int(xlen % 60)

        start_time='{:0>2d}:{:0>2d}:{:0>2d}'.format(0,mlen,slen)

        timelen='00:00:58'
        out_filename=savepath+'/'+rfilename+'_out_'+'{:04d}.mp4'.format(idx)
        (ffmpeg
                .input(srcfilename, ss=start_time, t=timelen)
                .output(out_filename)
                .overwrite_output()
                .run()
        )

def ParseOpts():
    opts,args=getopt.getopt(sys.argv[1:],"-h-v-N:",["help","version","nfile="])
    savepath='e:\\git\\BGM\\split'
    for optname,optvalue in opts:
        if (optname in ["-h","--help"]):
            usage()
            exit()
        if (optname in ["-v","--version"]):
            version()
            exit()

        if (optname in ["-N","--nfile"]):
            splitvideo(optvalue,savepath)
            exit()

        print("opts:{}".format(opts))
        usage()
    print("sysv.argv={}".format(sys.argv))
    usage()

if __name__ == '__main__':
    ParseOpts()
