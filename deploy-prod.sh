#!/bin/zsh
cd ~/Documents/Code/CS121/image-colorizer/
git add .
git commit -m "deploy"
git push heroku `git subtree split --prefix frontend $(git rev-parse --abbrev-ref HEAD)`:main --force