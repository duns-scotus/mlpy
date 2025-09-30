from mlpy.cli.repl import MLREPLSession

repl = MLREPLSession()
result = repl.execute_ml_line('import string')
print(f"Import result: success={result.success}, error={result.error}")
print(f"Transpiled Python:\n{result.transpiled_python}")

result = repl.execute_ml_line('string.upper("hello")')
print(f"\nExecution result: success={result.success}, error={result.error}")
print(f"Transpiled Python:\n{result.transpiled_python}")
