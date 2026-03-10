import csv
import json

def convert_matrix_to_points(input_file, output_file):
    points = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))
        
        # 1. 提取第一行的 X 坐标 (从第二列开始)
        # 过滤掉空字符串，并转为浮点数
        x_coords = [float(x) for x in reader[0][1:] if x.strip()]
        
        # 2. 遍历剩下的每一行 (从第二行开始)
        for row in reader[1:]:
            y_val_str = row[0].strip()
            if not y_val_str:
                continue
            
            y_val = float(y_val_str) # 当前行的 Y 坐标
            
            # 3. 遍历这一行中的每一个 Z 值
            # row[1:] 对应的就是之前提取的 x_coords
            for i, z_val_str in enumerate(row[1:]):
                z_val_str = z_val_str.strip()
                
                # 如果 Z 值不为空，则记录该点
                if z_val_str:
                    try:
                        z_val = float(z_val_str)
                        x_val = x_coords[i]
                        # 保存为 [x, y, z] 格式
                        points.append([x_val, y_val, z_val])
                    except (ValueError, IndexError):
                        # 忽略无法转换为数字的异常情况
                        continue

    # 4. 将结果保存为 JSON，方便 JS 直接读取
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(points, f)
    
    print(f"转换完成！共提取 {len(points)} 个有效点。数据已保存至 {output_file}")

# 使用示例
# 请确保你的 Excel 文件已另存为 CSV 格式 (例如 data.csv)
convert_matrix_to_points('data.csv', 'points.json')