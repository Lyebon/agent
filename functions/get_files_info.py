import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        joint = os.path.normpath(os.path.join(working_directory, directory))
        if valid_target_dir is False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        result = ""
        destination = os.listdir(joint)
        for dir in destination:
            derection = os.path.join(joint, dir)
            if os.path.isdir(derection):
                is_dir = True
            else:
                is_dir = False
            result += f"\n- {dir}: file_size={os.path.getsize(derection)} bytes, is_dir={is_dir}"
        return result
            
        
    except Exception as e:
        print(f"Error found: {e}")