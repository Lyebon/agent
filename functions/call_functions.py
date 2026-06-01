from functions.get_files_info import schema_get_files_info, schema_write_files, schema_get_file_content, schema_run_python_file, function_map
from google.genai import types

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_files,
        schema_get_file_content,
        schema_run_python_file
        ],
)

def call_function(
    function_call: types.FunctionCall, verbose: bool = False
) -> types.Content:
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    function_name = function_call.name or ""
    if function_name == "" or function_name is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"
    function_result = function_map[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
