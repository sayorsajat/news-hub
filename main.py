import os

directory = "sources"

for file_name in os.listdir(directory):
    if file_name.startswith('_') or not file_name.endswith('.py'):
        continue
    module_name = file_name[:-3]
    module = __import__(f"{directory}.{module_name}", fromlist=[module_name])
    module.collectNews()
