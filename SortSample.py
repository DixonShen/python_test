#coding:utf8

__author__ = 'DixonShen'

import time


"""
插入排序
稳定排序，适用于基本有序的情况，O（n^2）

"""

def insert_sort(list):
    count = len(list)
    for i in range(1,count):
        key = list[i]
        j = i-1
        while j >=0:
            if list[j]>key:
                list[j+1] = list[j]
                list[j] = key
            j -= 1
        print list

"""
插入排序
稳定排序，适用于基本有序的情况，O（n^2）

"""

l1 = [1541,157,441,41,58,1,52,4,512,455,12,45,454,41,24456,798,4,54,64687,3,4654]
insert_sort(l1)
