import sys
from csv import writer
from pydriller import Repository
from pathlib import Path

# Define column names for the CSV
columns = [
    'old_file_path', 'new_file_path', 'commit_SHA',
    'parent_commit_SHA', 'commit_message', 'diff_hist', 'old_file_MCC', 'new_file_MCC'
]

# Prepare variables for commit processing
commit_count = 0
max_commits = 500
commit_list = []

# Traverse commits and store relevant ones
for commit in Repository(sys.argv[1], only_no_merge=True, order='reverse', histogram_diff=True, skip_whitespaces=True).traverse_commits():
    if commit.in_main_branch:
        commit_list.append(commit)
        commit_count += 1
        if commit_count == max_commits:
            break

# Reverse commit list to maintain order
commit_list.reverse()

# Prepare a list to hold the change records
change_records = []
total_commits = len(commit_list)

# Process each commit
for index, commit in enumerate(commit_list, 1):
    print(f'Processing [{index}/{total_commits}] {commit.hash} in {sys.argv[1]}')
    
    # Process each modified file in the commit
    for modified_file in commit.modified_files:
        # Calculate method complexities
        initial_complexity = sum(method.complexity for method in modified_file.methods_before) if modified_file.methods_before else 0
        final_complexity = modified_file.complexity or 0

        # Create a record for the modified file and add it to the change_records list
        change_record = [
            modified_file.old_path,
            modified_file.new_path,
            commit.hash,
            next(iter(commit.parents), None),
            commit.msg,
            modified_file.diff or '',
            initial_complexity,
            final_complexity
        ]
        change_records.append(change_record)

# Define the output directory and create it if it doesn't exist
results_dir = Path(f"{sys.argv[1]}_results")
results_dir.mkdir(exist_ok=True)

# Define the output CSV file path and write the change records
output_path = results_dir / "commits_info.csv"
with open(output_path, 'a', newline='') as output_file:
    csv_writer = writer(output_file)
    if output_file.tell() == 0:  # Write headers only if file is empty
        csv_writer.writerow(columns)
    csv_writer.writerows(change_records)

