import sys
import csv
import subprocess
from pydriller import Repository

def git_diff(diff_type, repo_path, parent_sha, commit_sha, file_path):
    try:
        cmd = ["git", "-C", repo_path, "diff", parent_sha, commit_sha, "--", file_path, "--ignore-all-space"]
        if diff_type == "histogram":
            cmd.insert(4, "--diff-algorithm=histogram")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

columns = [
    'old_file_path', 'new_file_path', 'commit_SHA',
    'parent_commit_SHA', 'commit_message',
    'diff_myers', 'diff_histogram'
]

rows = []
count = 0
last_n = 500

commits = []
for commit in Repository(sys.argv[1], only_no_merge=True, order='reverse').traverse_commits():
    if commit.in_main_branch:
        count += 1
        commits.append(commit)
        if count == last_n:
            break

# Reverse the order of commits to process them correctly
commits.reverse()

for i, commit in enumerate(commits):
    print(f'[{i+1}/{len(commits)}] Mining commit {sys.argv[1]} {commit.hash}')

    parent_sha = commit.parents[0] if commit.parents else ''

    for modified_file in commit.modified_files:
        old_file_path = modified_file.old_path
        new_file_path = modified_file.new_path

        # Skip if both old and new paths are missing
        if not old_file_path and not new_file_path:
            continue

        # If new_file_path is None (e.g., a deleted file), use old_file_path
        if new_file_path is None:
            new_file_path = old_file_path

        repo_path = sys.argv[1]
        diff_myers = git_diff("myers", repo_path, parent_sha, commit.hash, new_file_path)
        diff_hist = git_diff("histogram", repo_path, parent_sha, commit.hash, new_file_path)

        rows.append([
            old_file_path,
            new_file_path,
            commit.hash,
            parent_sha,
            commit.msg,
            diff_myers,
            diff_hist
        ])

# Ensure output directory exists
import os
output_dir = sys.argv[1] + '_results'
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, 'commits_info.csv'), 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(columns)
    writer.writerows(rows)
