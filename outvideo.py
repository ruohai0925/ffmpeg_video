import os
import subprocess
import shutil
import sys

SOURCE_PATH = ''
OUTPUT_PATH = ''
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

APPEND_PATH = ''

def deal_path():

    if len(sys.argv) < 3:
        print('checkout parameters, useage : python \'this_file.py\' \'src_dir\' \'out_dir\' \'append_video\'')
        return
    
    SOURCE_PATH = os.path.join(CURRENT_PATH, sys.argv[1])
    OUTPUT_PATH = os.path.join(CURRENT_PATH, sys.argv[2])
    APPEND_PATH = os.path.join(CURRENT_PATH, sys.argv[3])

    if not os.path.exists(APPEND_PATH):
        print('append video not exist, pls check : ', APPEND_PATH)
        return

    if os.path.exists(SOURCE_PATH) and os.path.exists(OUTPUT_PATH):
        print('deal path : ', SOURCE_PATH, ' and ', OUTPUT_PATH)
        deal_video(SOURCE_PATH, OUTPUT_PATH)
    else :
        print('checkout input path exists !', SOURCE_PATH, ' and ', OUTPUT_PATH)

def deal_video(src, out):
    # 获取目标文件夹视频文件
    files = os.listdir(src)
    
    out_name = 'nonono.mp4'

    for file_name in files:
        src_file = os.path.join(src, file_name)
        tmp_file = os.path.join(CURRENT_PATH, '1.mp4')
        out_file = os.path.join(CURRENT_PATH, out_name)
        def_file = os.path.join(out, file_name)

        # 文件重命名防止ffmpeg无法处理
        shutil.copyfile(src_file, tmp_file)

        # 打开filelist文件写入拼接视频
        file_list_path = os.path.join(CURRENT_PATH, 'filelist.txt')
        with open(file_list_path,'+wt') as file_list:
            print('写入视频列表文件',file_list_path, " ", src_file)
            file_list.write('file \'' + '1.mp4\'\n')
            file_list.write('file \'' + sys.argv[3] + '\'')
            file_list.close()

        # ffmpeg -f concat -i file_list_path -c copy a.mp4
        command = 'ffmpeg -f concat -i ' + file_list_path + ' -c copy ' + out_name

        print('运行指令:', command)
        ret, val = subprocess.getstatusoutput(command)

        if ret == 0:
            print('\tffmpeg 拼接成功，请检查文件', def_file)
            # 删除filelist.txt文件
            if os.path.exists(file_list_path):
                os.remove(file_list_path)
            os.remove(tmp_file)
            # 重新改回名字
            shutil.move(out_file, def_file)

        else :
            print('当前任务执行出错\n', val)

        # shutil.copyfile(os.path.join(src, file_name), os.path.join(out, str(index)+'.mp4'))


if __name__ == '__main__':
    if sys.argv[1] == 'help':
        print('提前打包要处理视频为同一目录,使用方法如下\npython outvideo.py p1 p2\n命令行参数为: p1.原视频文件夹目录, p2.输出目录')
    else:
        deal_path()