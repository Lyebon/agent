import os
import subprocess
from config import MAX_CHARS
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

schema_write_files = types.FunctionDeclaration(
    name="write_files",
    description="Write or overwrite files in a specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content for write or overwrite the files"
            )
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments in a specified directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="The list of scripts that can we use"
            ),
        },
        required=["file_path"],
    ),
)

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
        return f"Error found: {e}"

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir is False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(target_dir):
            return read_file(target_dir, file_path)
        return f'Error: File not found or is not a regular file: "{file_path}"'
    except Exception as e:
            return f"Error: {e}"

def write_files(working_directory: str, file_path: str, content: str) -> str:
        try:
            working_dir_abs = os.path.abspath(working_directory)
            target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
            valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
            if valid_target_dir is False:
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            if os.path.isdir(target_dir):
                return f'Error: Cannot write to "{file_path}" as it is a directory'
            trace = os.path.dirname(target_dir)
            os.makedirs(trace, exist_ok=True)
            write_file(target_dir, content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        except Exception as e:
            return f"Error: {e}"

def read_file(target_dir, file_path):
    with open(target_dir, "r") as f:
        content = f.read(MAX_CHARS)
        if f.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    
def write_file(target_dir, content):
    with open(target_dir, "w") as f:
                f.write(content)

def run_python_file(
          working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if valid_target_dir is False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_dir]
        if args is not None:
            command.extend(args)
        final_message =""
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            final_message += f"\nProcess exited with code {result.returncode}"
        if result.stdout == None and result.stderr == None:
            final_message += f"\nNo output produced"
        else:
            final_message += f"\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        return final_message
        
    except Exception as e:
        return f"Error: executing Python file: {e}"