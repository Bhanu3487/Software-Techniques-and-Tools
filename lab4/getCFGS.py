import sys
import os
from collections import Counter
from pydriller import Repository
from datetime import datetime
import matplotlib.pyplot as plt
from pycfg.pycfg import PyCFG, CFGNode
from typing import List, Dict, Tuple


def create_control_flow_graph(source_code: str, output_path: str) -> bool:
    """Generate the Control Flow Graph (CFG) from the source code."""
    try:
        cfg = PyCFG()
        arcs = []
        cfg.gen_cfg(source_code.strip())
        graph = CFGNode.to_graph(arcs)
        graph.draw(f"{output_path}.svg", prog='dot', format='svg')
        return True
    except Exception as e:
        print(f"Error generating CFG: {str(e)}")
        return False


def analyze_repository_changes(repo_path: str) -> Tuple[Counter, Dict[str, List[Tuple[datetime, int]]]]:
    """Analyze the repository and track file changes and cyclomatic complexity."""
    commits = list(Repository(repo_path, order='reverse').traverse_commits())
    file_changes_counter = Counter()
    complexity_over_time = {}

    for commit in commits:
        for file in commit.modified_files:
            if file.filename.endswith('.py'):
                file_path = file.new_path or file.old_path
                file_changes_counter[file_path] += 1

                # Track cyclomatic complexity
                if file_path not in complexity_over_time:
                    complexity_over_time[file_path] = []
                complexity = file.complexity or 0
                complexity_over_time[file_path].append((commit.committer_date, complexity))
    
    return file_changes_counter, complexity_over_time, commits


def generate_cfgs_for_file(commits: List, file_name: str):
    """Generate CFGs for a specific file from all commits."""
    os.makedirs('cfg_images', exist_ok=True)
    for commit in commits:
        for file in commit.modified_files:
            if file.new_path == file_name and file.source_code:
                timestamp = commit.committer_date.strftime('%Y%m%d_%H%M%S')
                output_path = f'cfg_images/cfg_{timestamp}_{commit.hash}'
                if create_control_flow_graph(file.source_code, output_path):
                    print(f"Generated CFG for commit {commit.hash}")
                break


def plot_complexity_trends(complexity_history: Dict[str, List[Tuple[datetime, int]]], top_changed_file: str):
    """Plot the cyclomatic complexity evolution of the most changed file."""
    if top_changed_file in complexity_history:
        dates, complexities = zip(*sorted(complexity_history[top_changed_file]))
        plt.figure(figsize=(10, 6))
        plt.plot(dates, complexities, marker='o')
        plt.title(f'Cyclomatic Complexity Evolution: {top_changed_file}')
        plt.xlabel('Date')
        plt.ylabel('Cyclomatic Complexity')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('cyclomatic_complexity_evolution.png')


# Execution Block
repo_path = 'docker-stacks'

# Track changes and complexities
file_changes_counter, complexity_over_time, commits = analyze_repository_changes(repo_path)

# Identify the most changed file
most_changed_file = file_changes_counter.most_common(1)[0][0]
print(f"Most changed file: {most_changed_file}")

# Generate CFGs for the most changed file
generate_cfgs_for_file(commits, most_changed_file)

# Report top 3 most frequently changed files
print("\nTop 3 most frequently changed files:")
for file, count in file_changes_counter.most_common(3):
    print(f"{file}: {count} changes")

# Plot complexity trends
plot_complexity_trends(complexity_over_time, most_changed_file)
