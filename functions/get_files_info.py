import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        dir_content = os.listdir(working_dir_abs)
        result = ""
        for dir in dir_content:
            if result == "":
                result += f"- {dir}: file_size={os.path.getsize(dir)} bytes, is_dir={os.path.isdir(dir)}"
            else:
                result += f"\n- {dir}: file_size={os.path.getsize(dir)} bytes, is_dir={os.path.isdir(dir)}"
        return result
        
    except Exception as e:
        print(f"Error found: {e}")