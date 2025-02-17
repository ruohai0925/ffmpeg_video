# ffmpeg_video

## 1.intro

A small tool for adding an opening, a closing, and a watermark to videos.

## 2.Dependencies

- [ffmpeg]([FFmpeg](https://ffmpeg.org/))
- [python](https://www.python.org/) [recommend [conda](https://docs.anaconda.com/miniconda/)]

## 3.usage

You can use the following command line to obtain the usage method:

```base
python outvideo.py help
```

help message:

```txt
提前打包要处理视频为同一目录,使用方法如下
python outvideo.py src out file mode

命令行参数为:
        src-原视频文件夹目录
        out-输出目录
        file-处理文件
        mode-处理模式:
                a-后缀视频      [file处理文件要为mp4格式视频]
                p-前缀视频      [file处理文件要为mp4格式视频]
                w-添加移动水印  [file处理文件要为png格式图片]
```

### 3.1 example

- To add `end.mp4` to the end of the videos in the `src` directory and output the modified videos to the `out` directory

    ```bash
    python outvideo.py src out end.mp4 a
    ```

- To add `start.mp4` at the beginning of the videos in the `src` directory and output the combined videos to the `out` directory

    ```bash
    python outvideo.py src out start.mp4 p
    ```

- To add the `cat.png` image as a watermark to the videos in the `src` directory and output the processed videos to the `out` directory

    ```bash
    python outvideo.py src out cat.png w
    ```

    

    