import xml.etree.ElementTree as ET

# 加载SVG文件
input_svg_path = "/home/shenshuyu/GBX_dashboard/GBX_dashboard/src/assets/data/haibei_map.svg"
output_svg_path = "/home/shenshuyu/GBX_dashboard/GBX_dashboard/src/assets/data/haibei_map.svg"
# output_svg_path = "/mnt/c/Users/dobby/Desktop/gbx_box/gbx_vis/src/assets/hkust_gz_map.svg"

# 解析SVG文件
tree = ET.parse(input_svg_path)
root = tree.getroot()

# 命名空间 (SVG的默认命名空间)
ns = {'ns0': 'http://www.w3.org/2000/svg'}

# 递归函数，用于遍历所有层级的g标签并处理path元素
buildings = [
    "W1", "W2", "W3", "W4", "E1", "E2", "E3", "E4",
    "Library", "Lecture Halls", "Administration Building", "Activity Center",
    "Block 1A", "Block 1B", "Block 3", "Block 5A", "Block 5B", "Block 5C",
    "Block 2A", "Block 2B", "Block 4A", "Block 4B", "Block 6A", "Block 6B",
    "Block 6C", "Bleachers", "Stadium","Canteen",
    "10D", "10C", "10B", "10A",
    "9D", "9C", "9B", "9A",
    "NN-8", "NN-6", "NN-9", "NN-2", "NN-3", "NN-1", "NN-4-5",
    "Data Center","Energy Center","Fire Control Center",
    "Locker 3"

]

def process_group(group_element):
    # 查找当前group中的path元素
    for path in group_element.findall("ns0:path[@id]", ns):
        if path.get("id") in buildings:
            path.set("name", path.get("id"))

    # 查找嵌套的g标签并递归调用
    for nested_group in group_element.findall("ns0:g", ns):
        process_group(nested_group)

# 从根元素开始处理
process_group(root)

# 去掉命名空间前缀
for elem in root.iter():
    if '}' in elem.tag:
        elem.tag = elem.tag.split('}', 1)[1]  # 去掉命名空间

# 将修改后的内容保存到新文件
tree.write(output_svg_path)

print("处理完成，嵌套的所有g标签中的path元素已检查并添加name属性（如有id），并去掉了命名空间前缀。")
