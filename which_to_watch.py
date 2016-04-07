#coding=utf8

__author__ = 'DixonShen'

import os
import random

def get_file_list(dir,filelist):
    # newdir = dir
    if os.path.isfile(dir):
        filelist.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            #如果需要忽略某些文件夹，使用以下代码
            #if s == "xxx":
                #continue
            newdir = os.path.join(dir,s)
            get_file_list(newdir,filelist)
    return filelist

if __name__=='__main__':
    fdir = 'F:\\Videos'
    flist = get_file_list(fdir,[])

    length = len(flist)
    # for s in flist:
    #     parts = s.split('.')
    #     num = len(parts)
    #     print parts[num-1]

    index = random.randint(0,length-1)
    print "Let's watch ",flist[index].split('\\')[len(flist[index].split('\\'))-1],"!"

