import os
import subprocess
import shutil
import sys

SOURCE_PATH = ''
OUTPUT_PATH = ''
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

APPEND_PATH = ''

def deal_path():
    """
    对添加的命令行参数进行处理，区分处理功能、处理路径
    """
    print("开始拼接视频")

    if len(sys.argv) < 3:
        print('checkout parameters, useage : python \'this_file.py\' \'src_dir\' \'out_dir\' \'your_file\' \'deal_mode\'')
        return
    
    SOURCE_PATH = os.path.join(CURRENT_PATH, sys.argv[1])
    OUTPUT_PATH = os.path.join(CURRENT_PATH, sys.argv[2])
    DEAL_FILE   = os.path.join(CURRENT_PATH, sys.argv[3])
    DEAL_MODE   = sys.argv[4]

    if not os.path.exists(DEAL_FILE):
        print(' your input file not exist, pls check : ', DEAL_FILE)
        return

    if DEAL_MODE == 'a' or DEAL_MODE == 'p':
        deal_video(SOURCE_PATH, OUTPUT_PATH, DEAL_FILE, DEAL_MODE)
    elif DEAL_MODE == 'w':
        deal_watermark(SOURCE_PATH, OUTPUT_PATH, DEAL_FILE)
    else :
        print('your current mode : ', DEAL_MODE, ', pls check help infomation !')

def deal_video(src, out, video, mode):
    """
    对视频添加前缀或者后缀
    """

    if os.path.exists(src) and os.path.exists(out):
        print('deal path : ', src, ' and ', out)
    else :
        print('checkout input path exists !', src, ' and ', out)
        return

    files = os.listdir(src)
    
    out_name = 'tmp_cache.mp4'

    for file_name in files:
        # 源文件相对位置
        src_file = os.path.join(src, file_name)
        # 临时文件相对位置
        tmp_file = 'tmp_deal.mp4'
        # 拼接文件相对位置
        cut_file = sys.argv[3]
        # 最终文件相对位置
        def_file = os.path.join(out, file_name)

        # 文件重命名防止ffmpeg无法处理
        shutil.copyfile(src_file, tmp_file)

        # 打开filelist文件写入拼接视频
        file_list_path = os.path.join(CURRENT_PATH, 'filelist.txt')
        with open(file_list_path,'+wt') as file_list:
            print('写入视频列表文件',file_list_path, " ", src_file)
            # 后缀视频
            if mode == 'a':
                file_list.write('file \'' + tmp_file + '\'\n')

            file_list.write('file \'' + cut_file + '\'\n')
            # 前缀视频
            if mode == 'p':
                file_list.write('file \'' + tmp_file + '\'\n')

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
            shutil.move(out_name, def_file)

        else :
            print('当前任务执行出错\n', val)

        # shutil.copyfile(os.path.join(src, file_name), os.path.join(out, str(index)+'.mp4'))

def deal_watermark(src, out, pic):
    """
    对视频添加移动水印
    """
    print("开始处理水印")

    files = os.listdir(src)

    for file_name in files:

        # 源文件相对位置
        src_file = os.path.join(src, file_name)
        # 临时文件
        tmp_file = 'tmp_cache.mp4'
        # 最终文件
        def_file = os.path.join(out, file_name)
        # 文件重命名防止ffmpeg无法处理
        shutil.copyfile(src_file, tmp_file)

        # 对角线移动 单次
        # ffmpeg -i input.mp4 -i watermark.png -filter_complex "[0:v][1:v] overlay=W-w-(t/2)*W:H-h-(t/2)*H" -codec:a copy output.mp4
        # 上往下垂直移动 单次
        # ffmpeg -i input.mp4 -i watermark.png -filter_complex "[0:v][1:v] overlay=W-w-(t/2)*W:main_h/2-overlay_h/2" -codec:a copy output.mp4
        
        # 缩放图片到100像素宽，左上角往右下角，4秒出现一次
        filter = '[1:v]scale=100:-1[wm];[0:v][wm]overlay=x=\'if(gte(t,0), -w+(mod(t,4)/4)*(W+w), NAN)\':y=\'if(gte(t,0), -h+(mod(t,4)/4)*(H+h), NAN)\''
        command = 'ffmpeg -i ' + tmp_file + ' -i ' + pic + ' -filter_complex "' + filter + '" -codec:a copy output.mp4'
        print('运行指令:', command)
        ret, val = subprocess.getstatusoutput(command)

        if ret == 0:
            print('\tffmpeg 拼接成功，请检查文件', def_file)
            # 删除临时文件
            os.remove(tmp_file)
            # 重新改回名字
            shutil.move('output.mp4', def_file)

        else :
            print('当前任务执行出错\n', val)

if __name__ == '__main__':
    if sys.argv[1] == 'help':
        print('提前打包要处理视频为同一目录,使用方法如下\npython outvideo.py src out file mode\n'
              '\n命令行参数为: \n'
              '\tsrc-原视频文件夹目录\n'
              '\tout-输出目录\n'
              '\tfile-处理文件\n'
              '\tmode-处理模式:\n'
              '\t\ta-后缀视频\tp-前缀视频[p3处理文件要为mp4格式视频]\n'
              '\t\tw-添加移动水印[p3处理文件要为png格式图片]\n')
    else:
        deal_path()