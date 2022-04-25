#!/usr/bin/env python
#coding:utf-8


'''
   替换视频文件中的音频流
   author:marker.liu@foxmail.com
   initial date :2022-03-27
'''
__version__='2.0.0'
__author__='alex.liu(marker.liu@foxmail.com)'
__initdate__='2022-03-27'


import datetime
import os
import sys
import shutil
import time
import re
import json
import requests
import getopt
import ffmpeg
import ffmpy

def usage():
    print("insert bgm into the video file and substitute the backgroud music of the video,initial by author {},initdate {}  ".format(__author__,__initdate__))
    print("{} -h --help :help message for usage".format(sys.argv[0]))
    print("{} -v --version: print version info".format(sys.argv[0]))
    print("{} -N --nfile=videourl_list_file :search video list from douyin.com download stream file".format(sys.argv[0]))

def version():
    print("{}".format(__version__))

def GetNameDuration(segfilelist,idx):
    '''
      根据索引，返回文件名和视频时长
    '''
    adict=segfilelist[idx]
    metainfo=None
    vfilename=None

    for k,v in adict.items():
        vfilename=str(k)
        metainfo=eval(v)
    vduration=0
    if (metainfo is not None):
        vduration=int(float(metainfo['streams'][0]['duration']))
    return vfilename,vduration

def catcut(dstfilelist,duration):
    '''
      功能：
        将dstfilelist各个视频文件，合并1个文件，并剪切时长为duration
    '''
    tmpfilename=dstfilelist[0]
    '''
     如果是多个文件，则进行转换，合并成新文件
    '''
    if (len(dstfilelist)>1):
        '''
        1. 转换成ts文件
            ffmpeg -i input1.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate1.ts
        '''
    
        sumts='concat'
        cnt=0
        for xsrcfile in dstfilelist:
            ts_filepath,ts_filename_a=os.path.split(xsrcfile)
            ts_filename,file_ext = os.path.splitext(ts_filename_a)

            ts_filename='E:\\git\\BGM\\tmp\\'+ts_filename+'.ts'
            if (cnt==0):
                sumts=sumts+':'+ts_filename
            else:
                sumts=sumts+'|'+ts_filename
            cnt=cnt+1

            if (os.path.exists(ts_filename)):
                print("ts file is ok:{}".format(ts_filename))
            else:
                '''
                  转换
                '''
                ff = ffmpy.FFmpeg(
                                   inputs={xsrcfile: None},
                                   outputs={ts_filename: [
                                    '-c','copy'
                                    ,'-bsf:v','h264_mp4toannexb'
                                    ,'-f','mpegts'
                                    ,'-loglevel','error'
                    ]}
                )
                print("ffmpy run cmd:{}".format(ff.cmd))
                ff.run()
        '''        
            2. 合并
           ffmpeg -i "concat:1.ts|2.ts|...n.ts" -c copy -absf aac_adtstoasc out.mp4   
        '''
        # sumts=sumts+''
        print("sumts={}".format(sumts))
        tmpfilename='E:\\git\\BGM\\tmp\\'+str(time.strftime("%Y%m%d%H%M%S", time.localtime())) +'.mp4'
        ffb = ffmpy.FFmpeg(
                                   inputs={sumts: None},
                                   outputs={tmpfilename: [
                                    '-c','copy'
                                    ,'-absf','aac_adtstoasc'
                                    ,'-loglevel','error'
                    ]}
                )
        print("ffmpy run cmd:{}".format(ffb.cmd))
        ffb.run()       
    '''
      删减到目标长度
    '''
    time.sleep(10)
    ndst='E:\\git\\BGM\\tmp\\'+str(time.strftime("%Y%m%d%H%M%S", time.localtime())) +'.mp4'
    tstr='00'+':'+'{:0>2d}'.format(int(duration/60))+':'+'{:0>2d}'.format(int(duration%60))
    ffc = ffmpy.FFmpeg(
               inputs={tmpfilename: None},
               outputs={ndst: [
               '-ss', '00:00:00',
               '-t',  tstr
               #,'-loglevel','error'
             ]}
            )
    print("cmd:{}".format(ffc.cmd))
    ffc.run()
    return ndst


def NewCatCut(dstfilelist,duration):
    '''
      功能：
        将dstfilelist各个视频文件，合并1个文件，并剪切时长为duration
    '''
    tmpfilename=dstfilelist[0]
    '''
     如果是多个文件，则进行转换，合并成新文件
    '''
    if (len(dstfilelist)>1):
        '''
        1. 转换成ts文件
            ffmpeg -i input1.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate1.ts
        '''
    
        sumts='concat'
        cnt=0
        for xsrcfile in dstfilelist:
            ts_filepath,ts_filename_a=os.path.split(xsrcfile)
            ts_filename,file_ext = os.path.splitext(ts_filename_a)

            ts_filename='E:\\git\\BGM\\tmp\\'+ts_filename+'.m4a'
            if (cnt==0):
                sumts=sumts+':'+ts_filename
            else:
                sumts=sumts+'|'+ts_filename
            cnt=cnt+1

            if (os.path.exists(ts_filename)):
                print("ts file is ok:{}".format(ts_filename))
            else:
                '''
                  转换
                '''
                ff = ffmpy.FFmpeg(
                                   inputs={xsrcfile: None},
                                   outputs={ts_filename: [
                                     '-vn'
                                    ,'-acodec','copy'
                                    #,'-f','mp3'
                                    ,'-loglevel','error'
                    ]}
                )
                print("ffmpy run cmd:{}".format(ff.cmd))
                ff.run()
        '''        
            2. 合并
           ffmpeg -i "concat:1.ts|2.ts|...n.ts" -c copy -absf aac_adtstoasc out.mp4   
        '''
        # sumts=sumts+''
        print("sumts={}".format(sumts))
        tmpfilename='E:\\git\\BGM\\tmp\\'+str(time.strftime("%Y%m%d%H%M%S", time.localtime())) +'.mp4'
        ffb = ffmpy.FFmpeg(
                                   inputs={sumts: None},
                                   outputs={tmpfilename: [
                                    '-c','copy'
                                    #,'-absf','aac_adtstoasc'
                                    ,'-loglevel','error'
                    ]}
                )
        print("ffmpy run cmd:{}".format(ffb.cmd))
        ffb.run()       
    '''
      删减到目标长度
    '''
    time.sleep(10)
    ndst='E:\\git\\BGM\\tmp\\'+str(time.strftime("%Y%m%d%H%M%S", time.localtime())) +'.mp4'
    tstr='00'+':'+'{:0>2d}'.format(int(duration/60))+':'+'{:0>2d}'.format(int(duration%60))
    ffc = ffmpy.FFmpeg(
               inputs={tmpfilename: None},
               outputs={ndst: [
               '-ss', '00:00:00',
               '-t',  tstr
               #,'-loglevel','error'
             ]}
            )
    print("cmd:{}".format(ffc.cmd))
    ffc.run()
    return ndst

def selectbgmvideo(duration,segfilelist):
    '''
    
    '''
    ##segfile='E:\\git\\BGM\\bgm_seglist.txt'
    lastidxfile='E:\\git\\BGM\\lastidx.txt'

    retfile=None
    xfilelist=list()
    '''
      read lastidx
    '''
    lastidx=0

    if (os.path.exists(lastidxfile)):
        with open(lastidxfile,'r') as idxf:
             line=idxf.readline()

             if (line):
                 dline=line.strip('\r').strip('\n').strip(' ')
                 lastidx=int(dline)
                 lastidx=lastidx+1
                 lastidx=lastidx%len(segfilelist)
             else:
                 lastidx=0
    '''   
    ###
    adict=segfilelist[lastidx]
    metainfo=None
    vfilename=None

    for k,v in adict.items():
        vfilename=str(k)
        metainfo=v
    vduration=0
    if (metainfo is not None):
        vduration=int(float(metainfo['streams'][0]['duration']))
    '''
    vfilename=None
    vduration=0

    vfilename,vduration=GetNameDuration(segfilelist,lastidx)

    dstfilelist=list()
    
    if (vduration>=int(float(duration))):
        '''
          将背景音乐文件，剪辑成：长度为duration的mp4文件，临时文件并返回。
        '''
        print("合并")
        dstfilelist.append(vfilename)
    else:
        sumduration=vduration        
        dstfilelist.append(vfilename)
        idx=(lastidx+1)%len(segfilelist)

        while (sumduration<int(float(duration))):            
            vtmpname,vtmpduration=GetNameDuration(segfilelist,idx)
            sumduration=sumduration+vtmpduration
            dstfilelist.append(vtmpname)
            idx=(idx+1)%len(segfilelist)
        lastidx=idx
    '''
    
    '''
    with open(lastidxfile,'w') as idxm:
             idxm.write(str(lastidx)+'\r\n')

    '''
    合并，裁剪
    '''
    retfile=catcut(dstfilelist,duration)
    return retfile

def loadseglist(segfile='E:\\git\\BGM\\bgm_seglist.txt'):
     
    retfile=None
    retfilelist=list()

    with open(segfile,'r') as f:
        lines=f.readlines()
        for d in lines:
            dname='E:\\git\\BGM\\split\\'+str(d).strip('\r').strip('\n').strip(' ')
            if (os.path.exists(dname)):
                dinfo=ffmpeg.probe(dname)
                ditem=dict()
                ditem[dname]=str(dinfo)
                retfilelist.append(ditem)
    return retfilelist    

def bgmcat(segfilelist,srcfilename,savepath):
    probe=None;
    probe = ffmpeg.probe(srcfilename)

    '''
      1. video1:检测第1个视频中内容长度
      2. video2:检测第2个视频中内容长度
      3. 
    '''
    #print("type={}".format(type(probe)))
    #print("PROBE:{}".format(probe))
    s=probe['streams']
    duration=0
    for x in s:
        #print("x:{}".format(type(x)))
        print("index:{},duration:{},codec_type:{},codec_name:{}".format(
            x['index'],x['duration'],x['codec_type'],x['codec_name'])) 
        if (x['codec_type']=='video'):
           duration=int(float(x['duration']))
    print("file:{},duration:{}".format(srcfilename,duration))

    '''
      目标文件
    '''
    xsrc_path,xsrc_filename=os.path.split(srcfilename)
    zsrc_filename,z_ext=os.path.splitext(xsrc_filename)
    zidx=1
    zdstfilename='E:\\git\\douyin\\upload\\'+zsrc_filename+'-'+'{:0>3d}'.format(zidx)+'.mp4'
    while (os.path.exists(zdstfilename)):
        zidx=zidx+1
        zdstfilename='E:\\git\\douyin\\upload\\'+zsrc_filename+'-'+'{:0>3d}'.format(zidx)+'.mp4'
    '''
      复制一个背景音乐MP4      
    '''
    ##bgmvfile=selectbgmvideo()
    bgmvfile=selectbgmvideo(duration,segfilelist)

    tmpfile=time.strftime("%Y%m%d%H%M%S", time.localtime()) 
    dstfile='E:\\git\\BGM\\tmp\\'+tmpfile+'.mp4'
    '''
    合成
    '''
    ff = ffmpy.FFmpeg(
      inputs={srcfilename: None,bgmvfile:None},
      outputs={dstfile: [
        '-vcodec', 'copy',
        '-acodec', 'copy',
        '-map','0:v',
        '-map','1:a'
        ,'-loglevel','error'
     ]}
    )
    print("cmd:{}".format(ff.cmd))
    ff.run()
    time.sleep(20)

    if (os.path.exists(dstfile)):
        nprobe=ffmpeg.probe(dstfile)
        vdur=int(float(nprobe['streams'][0]['duration']))

        adur=int(float(nprobe['streams'][1]['duration']))

        mdur=min(vdur,adur)

        if (vdur!=adur):
            tstr='00'+':'+'{:0>2d}'.format(int(mdur/60))+':'+'{:0>2d}'.format(int(mdur%60));
            print("timelen:{}".format(tstr))
            ndst='E:\\git\\BGM\\tmp\\'+str(time.strftime("%Y%m%d%H%M%S", time.localtime())) +'.mp4'
            ff = ffmpy.FFmpeg(
               inputs={dstfile: None},
               outputs={ndst: [
               '-ss', '00:00:00',
               '-t',  tstr
               ,'-loglevel','error'
             ]}
            )
            print("cmd:{}".format(ff.cmd))
            ff.run()
            print("dstfile={}".format(ndst))

            shutil.move(ndst,zdstfilename)
            
            return 
        else:
            shutil.move(dstfile,zdstfilename)
            return 

def listbgmcat(sfilelist,listfilename,savepath):
    with open(listfilename,'r') as lfd:
         lines=lfd.readlines()
         for data in lines:
             nfilename=str(data).strip('\r').strip('\n').strip(' ')
             if (os.path.exists(nfilename)):
                bgmcat(sfilelist,nfilename,savepath)
             else:
                 print("error filename:{}".format(nfilename))

def ParseOpts():
    opts,args=getopt.getopt(sys.argv[1:],"-h-v-N:-L:",["help","version","nfile=","List="])
    savepath='e:\\git\\BGM\\split'
    segfile='E:\\git\\BGM\\bgm_seglist.txt'
    sfilelist=loadseglist(segfile)

    for optname,optvalue in opts:
        if (optname in ["-h","--help"]):
            usage()
            exit()
        if (optname in ["-v","--version"]):
            version()
            exit()

        if (optname in ["-N","--nfile"]):
            bgmcat(sfilelist,optvalue,savepath)
            exit()

        if (optname in ["-L","--List"]):
            listbgmcat(sfilelist,optvalue,savepath)
            exit()

        print("opts:{}".format(opts))
        usage()
    print("sysv.argv={}".format(sys.argv))
    usage()

if __name__ == '__main__':
    ParseOpts()
