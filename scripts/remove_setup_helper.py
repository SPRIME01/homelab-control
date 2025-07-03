import os

file_to_delete = "C:/Users/sprim/Projects/Dev/AI-Native-Monorepo-Starter-Kit/.make_assets/setup_helper.sh"

if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"Successfully removed {file_to_delete}")
else:
    print(f"File not found: {file_to_delete}")
