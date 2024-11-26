# 目录下包含很多文件，按照每500个文件进行分割，放到不同目录下


import os
import shutil

def split_files(src_dir, dst_dir, num):
    files = os.listdir(src_dir)

    total_num = len(files)
    for i in range(0, total_num, num):

        # 创建新的目录
        dst_dir_name = dst_dir + '/' + 'part' + str(i//num+1)

        if not os.path.exists(dst_dir_name):
            os.makedirs(dst_dir_name)

        # 移动文件
        for file in files[i:i+num]:

            src_file_path = os.path.join(src_dir, file)

            # 移动文件
            shutil.move(src_file_path, dst_dir_name)


src_dir = '/mnt/tmp/apps/cmss-yangjiandong/data/the-stack-v2-full-java'
dst_dir = '/mnt/tmp/apps/cmss-yangjiandong/data/the-stack-v2-full-java'
num = 240
split_files(src_dir, dst_dir, num)

