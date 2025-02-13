import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# Define the project name and path to the CSV file
csv_path = f'/home/set-iitgn-vm/Desktop/Lab3/docker-stacks_results/commits_info_with_matches.csv'

# Check if the file exists
if not os.path.exists(csv_path):
    print(f"Error: The file {csv_path} does not exist.")
    exit()

# Load the CSV file
df = pd.read_csv(csv_path)

# Identify code and non-code artifacts based on file extensions
def classify_artifact(file_path):
    code_extensions = ['.py', '.java', '.cpp', '.c', '.js', '.cs', '.html', '.css']
    if any(file_path.endswith(ext) for ext in code_extensions):
        return "code"
    return "non-code"

# Add a column to classify artifacts
df['artifact_type'] = df['new_file_path'].apply(classify_artifact)

# Calculate statistics
stats = {
    "matches_code": len(df[(df['artifact_type'] == 'code') & (df['matches'] == 'Yes')]),
    "no_matches_code": len(df[(df['artifact_type'] == 'code') & (df['matches'] == 'No')]),
    "matches_non_code": len(df[(df['artifact_type'] == 'non-code') & (df['matches'] == 'Yes')]),
    "no_matches_non_code": len(df[(df['artifact_type'] == 'non-code') & (df['matches'] == 'No')]),
}

# Print the statistics
print("====================================================================")
print("Final Dataset Statistics:")
print(f"Matches for code artifacts: {stats['matches_code']}")
print(f"No matches for code artifacts: {stats['no_matches_code']}")
print(f"Matches for non-code artifacts: {stats['matches_non_code']}")
print(f"No matches for non-code artifacts: {stats['no_matches_non_code']}")
print("====================================================================")

# Generate bar plots
labels = ['Matches (Code)', 'No Matches (Code)', 'Matches (Non-Code)', 'No Matches (Non-Code)']
values = [stats['matches_code'], stats['no_matches_code'], stats['matches_non_code'], stats['no_matches_non_code']]

plt.figure(figsize=(10, 6))
plt.bar(labels, values, color=['green', 'red', 'blue', 'orange'])
plt.title(f'Statistics for Project: docker-stacks')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the plot
output_plot_path = f'/home/set-iitgn-vm/Desktop/Lab3/docker-stacks_results/artifact_statistics.png'
plt.savefig(output_plot_path)
print(f"Plot saved to docker-stacks_results dir")
