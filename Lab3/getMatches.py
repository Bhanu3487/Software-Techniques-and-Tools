import pandas as pd

input_csv = r'/home/set-iitgn-vm/Desktop/Lab3/docker-stacks_results/commits_info.csv'
output_csv = r'/home/set-iitgn-vm/Desktop/Lab3/docker-stacks_results/commits_info_with_matches.csv'


df = pd.read_csv(input_csv)

df['matches'] = df.apply(lambda row: "Yes" if row['diff_myers'] == row['diff_histogram'] else "No", axis=1)

df.to_csv(output_csv, index=False)

print(f"Dataset updated with 'matches' column and saved to docker-stacks_results")
