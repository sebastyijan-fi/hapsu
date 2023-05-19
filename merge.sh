#!/bin/bash

# Check out the development branch
git checkout development

# Pull the latest changes
git pull origin development

# Switch to the github branch
git checkout github

# Pull the latest changes from github (in case someone else has pushed in the meantime)
git pull origin github

# Merge development into github
git merge development

# Push the merged changes to github on GitHub
git push origin github


# ./merge.sh to run