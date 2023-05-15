import atexit
import shutil
import os

## used for cleanup
# detect_path = "./runs/detect"
# upload_path = "./pig-images"

# def cleanup_directory(path):
#     for filename in os.listdir(path):
#         file_path = os.path.join(path, filename)
#         try:
#             if os.path.isfile(file_path) or os.path.islink(file_path):
#                 os.unlink(file_path)
#             elif os.path.isdir(file_path):
#                 shutil.rmtree(file_path)
#         except Exception as e:
#             print(f"Failed to delete {file_path}. Reason: {e}")

# atexit.register(cleanup_directory(detect_path))
# atexit.register(cleanup_directory(upload_path))