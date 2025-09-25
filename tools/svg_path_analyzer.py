#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG路径分析器 - 提取Vector 1路径中的所有转折点坐标
"""

import re
import math

def parse_svg_path_complete(path_data):
    """
    完整解析SVG路径数据，提取所有转折点的坐标
    
    Args:
        path_data (str): SVG路径数据字符串
    
    Returns:
        list: 包含所有转折点坐标的列表，每个元素为(x, y)元组
    """
    # 移除路径数据中的换行符和多余空格
    path_data = path_data.strip()
    
    # 当前坐标
    current_x = 0
    current_y = 0
    
    # 存储所有转折点
    design_points = []
    
    # 正则表达式匹配所有SVG路径命令
    # 匹配所有可能的命令: M, m, L, l, H, h, V, v, C, c, S, s, Q, q, T, t, A, a, Z, z
    pattern = r'([MmLlHhVvCcSsQqTtAaZz])\s*([^MmLlHhVvCcSsQqTtAaZz]*)'
    
    # 查找所有命令
    matches = re.findall(pattern, path_data)
    
    for command, coordinates in matches:
        # 分割坐标字符串
        coord_parts = re.findall(r'[-+]?\d*\.?\d+', coordinates)
        
        if command == 'M':  # 绝对移动
            for i in range(0, len(coord_parts), 2):
                if i + 1 < len(coord_parts):
                    current_x = float(coord_parts[i])
                    current_y = float(coord_parts[i + 1])
                    design_points.append((current_x, current_y))
        
        elif command == 'm':  # 相对移动
            for i in range(0, len(coord_parts), 2):
                if i + 1 < len(coord_parts):
                    dx = float(coord_parts[i])
                    dy = float(coord_parts[i + 1])
                    current_x += dx
                    current_y += dy
                    design_points.append((current_x, current_y))
        
        elif command == 'L':  # 绝对直线
            for i in range(0, len(coord_parts), 2):
                if i + 1 < len(coord_parts):
                    current_x = float(coord_parts[i])
                    current_y = float(coord_parts[i + 1])
                    design_points.append((current_x, current_y))
        
        elif command == 'l':  # 相对直线
            for i in range(0, len(coord_parts), 2):
                if i + 1 < len(coord_parts):
                    dx = float(coord_parts[i])
                    dy = float(coord_parts[i + 1])
                    current_x += dx
                    current_y += dy
                    design_points.append((current_x, current_y))
        
        elif command == 'H':  # 绝对水平线
            for x in coord_parts:
                current_x = float(x)
                design_points.append((current_x, current_y))
        
        elif command == 'h':  # 相对水平线
            for dx in coord_parts:
                current_x += float(dx)
                design_points.append((current_x, current_y))
        
        elif command == 'V':  # 绝对垂直线
            for y in coord_parts:
                current_y = float(y)
                design_points.append((current_x, current_y))
        
        elif command == 'v':  # 相对垂直线
            for dy in coord_parts:
                current_y += float(dy)
                design_points.append((current_x, current_y))
        
        elif command == 'C':  # 绝对三次贝塞尔曲线
            for i in range(0, len(coord_parts), 6):
                if i + 5 < len(coord_parts):
                    # 控制点1
                    cp1x = float(coord_parts[i])
                    cp1y = float(coord_parts[i + 1])
                    # 控制点2
                    cp2x = float(coord_parts[i + 2])
                    cp2y = float(coord_parts[i + 3])
                    # 终点
                    current_x = float(coord_parts[i + 4])
                    current_y = float(coord_parts[i + 5])
                    design_points.append((cp1x, cp1y))
                    design_points.append((cp2x, cp2y))
                    design_points.append((current_x, current_y))
        
        elif command == 'c':  # 相对三次贝塞尔曲线
            for i in range(0, len(coord_parts), 6):
                if i + 5 < len(coord_parts):
                    # 控制点1
                    cp1x = current_x + float(coord_parts[i])
                    cp1y = current_y + float(coord_parts[i + 1])
                    # 控制点2
                    cp2x = current_x + float(coord_parts[i + 2])
                    cp2y = current_y + float(coord_parts[i + 3])
                    # 终点
                    current_x += float(coord_parts[i + 4])
                    current_y += float(coord_parts[i + 5])
                    design_points.append((cp1x, cp1y))
                    design_points.append((cp2x, cp2y))
                    design_points.append((current_x, current_y))
        
        elif command == 'S':  # 绝对平滑三次贝塞尔曲线
            for i in range(0, len(coord_parts), 4):
                if i + 3 < len(coord_parts):
                    # 控制点2
                    cp2x = float(coord_parts[i])
                    cp2y = float(coord_parts[i + 1])
                    # 终点
                    current_x = float(coord_parts[i + 2])
                    current_y = float(coord_parts[i + 3])
                    design_points.append((cp2x, cp2y))
                    design_points.append((current_x, current_y))
        
        elif command == 's':  # 相对平滑三次贝塞尔曲线
            for i in range(0, len(coord_parts), 4):
                if i + 3 < len(coord_parts):
                    # 控制点2
                    cp2x = current_x + float(coord_parts[i])
                    cp2y = current_y + float(coord_parts[i + 1])
                    # 终点
                    current_x += float(coord_parts[i + 2])
                    current_y += float(coord_parts[i + 3])
                    design_points.append((cp2x, cp2y))
                    design_points.append((current_x, current_y))
        
        elif command == 'Q':  # 绝对二次贝塞尔曲线
            for i in range(0, len(coord_parts), 4):
                if i + 3 < len(coord_parts):
                    # 控制点
                    cpx = float(coord_parts[i])
                    cpy = float(coord_parts[i + 1])
                    # 终点
                    current_x = float(coord_parts[i + 2])
                    current_y = float(coord_parts[i + 3])
                    design_points.append((cpx, cpy))
                    design_points.append((current_x, current_y))
        
        elif command == 'q':  # 相对二次贝塞尔曲线
            for i in range(0, len(coord_parts), 4):
                if i + 3 < len(coord_parts):
                    # 控制点
                    cpx = current_x + float(coord_parts[i])
                    cpy = current_y + float(coord_parts[i + 1])
                    # 终点
                    current_x += float(coord_parts[i + 2])
                    current_y += float(coord_parts[i + 3])
                    design_points.append((cpx, cpy))
                    design_points.append((current_x, current_y))
        
        elif command == 'T':  # 绝对平滑二次贝塞尔曲线
            for i in range(0, len(coord_parts), 2):
                if i + 1 < len(coord_parts):
                    current_x = float(coord_parts[i])
                    current_y = float(coord_parts[i + 1])
                    design_points.append((current_x, current_y))
        
        elif command == 't':  # 相对平滑二次贝塞尔曲线
            for i in range(0, len(coord_parts), 2):
                if i + 1 < len(coord_parts):
                    current_x += float(coord_parts[i])
                    current_y += float(coord_parts[i + 1])
                    design_points.append((current_x, current_y))
        
        elif command == 'A':  # 绝对椭圆弧
            for i in range(0, len(coord_parts), 7):
                if i + 6 < len(coord_parts):
                    # 椭圆弧参数: rx ry x-axis-rotation large-arc-flag sweep-flag x y
                    current_x = float(coord_parts[i + 5])
                    current_y = float(coord_parts[i + 6])
                    design_points.append((current_x, current_y))
        
        elif command == 'a':  # 相对椭圆弧
            for i in range(0, len(coord_parts), 7):
                if i + 6 < len(coord_parts):
                    # 椭圆弧参数: rx ry x-axis-rotation large-arc-flag sweep-flag x y
                    current_x += float(coord_parts[i + 5])
                    current_y += float(coord_parts[i + 6])
                    design_points.append((current_x, current_y))
        
        elif command in ['Z', 'z']:  # 闭合路径
            # 闭合路径不添加新点，但可以在这里处理
            pass
    
    return design_points

def analyze_vector_path():
    """
    分析Vector 1路径并输出所有转折点坐标
    """
    # Vector 1的路径数据
    vector_path = "m222 645.5-10.5-15L202 612l-8-18.5-11.5-20.5-6-19-7.5-17.5-4-18.5 4-15.5 13.5-15 24.5-12 32-15 19.5-11 10.5-12v-20l-4-19.5-6.5-18.5L249 367s-4.592-5.205-8.5-7c-6.388-2.935-18 0-18 0h-18l-21 1h-43"
    vector_path = "M153 178.5V189.5L157.5 203V211.5V221V231V240V251V260L162.5 276.5L168 285.5"
    vector_path = "m97.5 591 22.5-20 14.5-16 13-15 8.5-17 6.5-21.5 6.5-19 10.5-12L203 457l34-14 21.5-12 8.5-12.5V397l-8.5-19-6.5-21.5-15-12.5h-17l-17 23.5s-4.763 19.979-13 29.5c-6.594 7.622-21 15-21 15s-7.346 5.999-13 6.5c-11.828 1.048-21.5-21.5-21.5-21.5s-11.726-16.966-14.5-29.5c-2.532-11.439 0-30 0-30"
    
    print("=== Vector 1 路径分析 ===")
    print(f"原始路径数据: {vector_path}")
    print()
    
    # 解析路径
    design_points = parse_svg_path_complete(vector_path)
    
    print(f"发现 {len(design_points)} 个转折点:")
    print("-" * 60)
    print("序号    X坐标      Y坐标      说明")
    print("-" * 60)
    
    for i, (x, y) in enumerate(design_points, 1):
        point_type = "转折点"
        if i == 1:
            point_type = "起始点"
        elif i == len(design_points):
            point_type = "结束点"
        
        print(f"{i:2d}   {x:8.2f}   {y:8.2f}   {point_type}")
    
    print("-" * 60)
    
    # 计算路径的边界框
    if design_points:
        min_x = min(point[0] for point in design_points)
        max_x = max(point[0] for point in design_points)
        min_y = min(point[1] for point in design_points)
        max_y = max(point[1] for point in design_points)
        
        print(f"路径边界框:")
        print(f"  最小X: {min_x:.2f}")
        print(f"  最大X: {max_x:.2f}")
        print(f"  最小Y: {min_y:.2f}")
        print(f"  最大Y: {max_y:.2f}")
        print(f"  宽度: {max_x - min_x:.2f}")
        print(f"  高度: {max_y - min_y:.2f}")
    
    return design_points

def export_coordinates_to_file(points, filename="vector1_all_points.txt"):
    """
    将坐标导出到文件
    
    Args:
        points (list): 设计点坐标列表
        filename (str): 输出文件名
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Vector 1 所有转折点坐标\n")
        f.write("# 格式: 点序号 X坐标 Y坐标 说明\n")
        f.write("# 坐标系统: SVG坐标系，原点在左上角\n")
        f.write("-" * 60 + "\n")
        
        for i, (x, y) in enumerate(points, 1):
            point_type = "转折点"
            if i == 1:
                point_type = "起始点"
            elif i == len(points):
                point_type = "结束点"
            
            f.write(f"{i:2d} {x:8.2f} {y:8.2f} {point_type}\n")
    
    print(f"\n坐标已导出到文件: {filename}")

def main():
    """主函数"""
    print("SVG Vector 1 完整路径分析器")
    print("=" * 60)
    
    # 分析路径
    design_points = analyze_vector_path()
    
    # 导出坐标到文件
    export_coordinates_to_file(design_points)
    
    print("\n分析完成！")

if __name__ == "__main__":
    main()