import os
import re
import frontmatter
from datetime import datetime

def convert_markdown_tags_to_yaml(folder_path):
    """
    将文件夹中的Markdown文件的标签表格转换为YAML头部格式
    
    参数:
    folder_path (str): 包含Markdown文件的文件夹路径
    """
    # 确保文件夹路径存在
    if not os.path.exists(folder_path):
        print(f"错误: 文件夹 '{folder_path}' 不存在")
        return
    
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.md'):
            file_path = os.path.join(folder_path, filename)
            try:
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # 转换标签表格为YAML
                new_content = process_markdown(content)
                
                # 如果内容有变化，则写回文件
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f"已处理: {filename}")
                else:
                    print(f"无需修改: {filename}")
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")

def process_markdown(content):
    """
    处理单个Markdown文件内容，将标签表格转换为YAML头部
    
    参数:
    content (str): Markdown文件内容
    
    返回:
    str: 处理后的Markdown内容
    """
    # 检查是否已有YAML头部
    if content.startswith('---\n'):
        # 如果已有YAML头部，直接返回原内容，跳过处理
        return content
    else:
        # 将内容按行分割
        lines = content.split('\n')
        
        # 提取标题（第一个以 # 开头的行）
        title = ""
        for line in lines:
            if line.strip().startswith('#'):
                title = line.strip().lstrip('#').strip()
                break
        
        if not title:
            # 如果没有找到标题，使用文件名
            title = os.path.splitext(os.path.basename(content[:100]))[0]
        
        # 查找第一个表格的开始和结束位置
        table_start = -1
        table_end = -1
        table_header_row = -1
        
        for i, line in enumerate(lines):
            # 查找表格开始（第一个以 | 开头的行）
            if table_start == -1 and line.strip().startswith('|'):
                table_start = i
            # 查找表格头部分隔行（包含 ----- 的行）
            elif table_start != -1 and table_header_row == -1 and '---' in line and line.strip().startswith('|'):
                table_header_row = i
            # 查找表格结束（找到一个不以 | 开头的行，且已经找到了表格开始和表格头）
            elif table_start != -1 and table_header_row != -1 and i > table_header_row and not line.strip().startswith('|'):
                table_end = i - 1
                break
        
        # 如果到达文件末尾仍在表格中
        if table_start != -1 and table_header_row != -1 and table_end == -1:
            table_end = len(lines) - 1
        
        # 如果没有找到完整的表格，返回原内容
        if table_start == -1 or table_header_row == -1 or table_end == -1:
            return content
        
        # 解析表格内容
        metadata = {'title': title}
        
        # 遍历表格行，提取字段和值
        for i in range(table_start, table_end + 1):
            if i == table_header_row:  # 跳过分隔行
                continue
                
            cells = [cell.strip() for cell in lines[i].split('|')]
            if len(cells) >= 3:  # 确保有足够的单元格（包括首尾的空单元格）
                field = cells[1].strip()
                value = cells[2].strip()
                
                if field == '标签' and value:
                    metadata['tags'] = [value] if not value.startswith('[') else eval(value)
                elif field == '作者' and value:
                    metadata['author'] = [value]
                elif field == '来源' and value:
                    metadata['source'] = value
                elif field == '创建时间' and value:
                    # 转换日期格式
                    try:
                        if '/' in value:
                            dt = datetime.strptime(value, '%Y/%m/%d %H:%M')
                        else:
                            dt = datetime.strptime(value, '%Y-%m-%d %H:%M')
                        metadata['created'] = dt.strftime('%Y-%m-%d')
                    except ValueError:
                        # 如果解析失败，保留原始格式
                        metadata['created'] = value
        
        # 移除表格
        new_content_lines = lines[:table_start] + lines[table_end+1:]
        new_content = '\n'.join(new_content_lines)
        
        # 添加YAML头部
        yaml_header = '---\n'
        for key, value in metadata.items():
            if isinstance(value, list):
                yaml_header += f"{key}:\n"
                for item in value:
                    yaml_header += f"  - \"{item}\"\n"
            else:
                yaml_header += f"{key}: \"{value}\"\n"
        yaml_header += '---\n\n'
        
        return yaml_header + new_content

if __name__ == "__main__":
    # 指定要处理的文件夹路径
    folder_path = input("请输入Markdown文件所在的文件夹路径: ")
    convert_markdown_tags_to_yaml(folder_path)
    print("处理完成!")