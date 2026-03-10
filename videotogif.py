from moviepy import VideoFileClip

def extract_gif_segment(input_video, output_gif, start_time, end_time):
    # 1. 加载视频
    clip = VideoFileClip(input_video)
    
    # 2. 截取片段 (注意这里是 subclipped)
    sub_clip = clip.subclipped(start_time, end_time)
    
    # 3. 调整尺寸 (注意这里是 resized)
    optimized_clip = sub_clip.resized(width=800)
    
    # 4. 导出为 GIF
    print(f"开始导出...")
    optimized_clip.write_gif(output_gif, fps=12)
    
    # 记得关闭文件释放内存
    clip.close()
if __name__ == "__main__":
    # 根据你截图中的文件名进行设置
    input_file = "Array show.mp4" # 请确保文件名与文件夹中完全一致
    output_file = "docs/images/Array_show.gif"
    
    extract_gif_segment(input_file, output_file, 0, 20)