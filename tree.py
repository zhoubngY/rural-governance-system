import os
from pathlib import Path

def generate_tree(dir_path, prefix="", ignore_dirs=None):
    """递归生成目录树结构的文本行列表"""
    if ignore_dirs is None:
        ignore_dirs = {'.git', '__pycache__', '.idea', '.vscode', 'node_modules', '.DS_Store'}
    
    lines = []
    try:
        entries = list(Path(dir_path).iterdir())
        dirs = sorted([e for e in entries if e.is_dir() and e.name not in ignore_dirs], 
                      key=lambda e: e.name.lower())
        files = sorted([e for e in entries if e.is_file()], key=lambda e: e.name.lower())
        sorted_entries = dirs + files
        
        for idx, entry in enumerate(sorted_entries):
            is_last = (idx == len(sorted_entries) - 1)
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{entry.name}")
            
            if entry.is_dir():
                extension = "    " if is_last else "│   "
                lines.extend(generate_tree(entry, prefix + extension, ignore_dirs))
    except PermissionError:
        lines.append(f"{prefix}[权限不足]")
    except Exception as e:
        lines.append(f"{prefix}[错误: {e}]")
    
    return lines

def select_folder_interactive(prompt):
    """交互式选择文件夹"""
    print(f"\n{prompt}")
    while True:
        folder_path = input("请输入文件夹路径（直接回车使用当前目录）: ").strip()
        if not folder_path:
            folder_path = os.getcwd()
            print(f"使用当前目录: {folder_path}")
        
        path = Path(folder_path)
        if path.exists() and path.is_dir():
            return str(path.resolve())
        else:
            print(f"❌ 路径不存在或不是文件夹: {folder_path}")
            print("请重新输入")

def main():
    print("=" * 50)
    print("目录树生成工具（命令行版）")
    print("=" * 50)
    
    # 选择源文件夹
    source_dir = select_folder_interactive("请选择要生成目录树的源文件夹")
    print(f"✅ 已选择: {source_dir}")
    
    # 选择输出文件夹
    output_dir = select_folder_interactive("请选择目录树的保存位置")
    print(f"✅ 已选择: {output_dir}")
    
    # 生成目录树
    print("\n正在生成目录树...")
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    output_file = output_path / f"{source_path.name}_tree.txt"
    
    tree_lines = [source_path.name]
    tree_lines.extend(generate_tree(source_path))
    
    try:
        output_path.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(tree_lines))
        
        print("\n" + "=" * 50)
        print("✅ 目录树生成成功！")
        print(f"📁 源文件夹: {source_dir}")
        print(f"💾 保存位置: {output_file}")
        print(f"📊 总行数: {len(tree_lines)}")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ 保存失败: {e}")

if __name__ == "__main__":
    main()