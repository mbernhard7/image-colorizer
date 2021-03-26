#!/bin/zsh
cd ~/Documents/Code/CS121/image-colorizer/frontend
php -S localhost:8001 &
cd ~/Documents/Code/CS121/image-colorizer/backend
flask run -h localhost -p 8002