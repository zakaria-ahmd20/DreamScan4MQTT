import os
import glob

print("Cleaning up results and reports...")

base_dir = os.path.dirname(os.path.abspath(__file__))
results_folder = os.path.join(base_dir, '..', 'results')
reports_folder = os.path.join(base_dir, '..', 'reports')

# Remove all files in results folder
for file_path in glob.glob(os.path.join(results_folder, '*')):
    if os.path.isfile(file_path):
        os.remove(file_path)

# Remove all files in reports folder
for file_path in glob.glob(os.path.join(reports_folder, '*')):
    if os.path.isfile(file_path):
        os.remove(file_path)

print("Cleanup complete!")
