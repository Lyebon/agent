from functions.get_files_info import schema_get_files_info, schema_write_files, schema_get_files_content, schema_run_python_files
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_files,
        schema_get_files_content,
        schema_run_python_files
        ],
)
