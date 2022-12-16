# Run service in tmux app session
tmux new -s app -d
tmux send-keys -t app 'conda activate py38' Enter
tmux send-keys -t app 'cd ~/projects/StockPredictor && python stock_predictor/app.py' Enter

# Run web app in tmux webapp session
tmux new -s webapp -d
tmux send-keys -t webapp 'cd ~/projects/StockPredictor/frontend' Enter
tmux send-keys -t webapp 'npm install' Enter
tmux send-keys -t webapp 'sudo PORT=80 npm start' Enter

# Create tmux session update-data
tmux new -s update-data -d

# Install crontab list
crontab ~/projects/StockPredictor/config/update_data.crontab