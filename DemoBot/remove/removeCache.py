import os

def delete_pycache(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                dir_path = os.path.join(root, dir_name)
                print(f"Deleting {dir_path}")
                os.system(f"rmdir /s {dir_path}")

# Replace '.' with your project's root directory path
delete_pycache('.')
