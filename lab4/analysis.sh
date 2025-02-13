#!/bin/bash

#pre-clean and setup
echo "performing pre-clean and setup..."
#rm -rf temp
rm -rf $1_results
rm -f *.xml *.dot
mkdir $1_results

#collect last 500 non-merge commits
python3 getCommits.py $1 > $1_results/$1.commits
python3 getCommitsInfo.py $1

# Run the CFGs (Control Flow Graphs) analysis
python3 getCFGS.py

#rm -rf $1

echo "Analysis complete!"

