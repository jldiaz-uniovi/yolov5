# This is the script which runs gunicorn with the appropriate number of workers
# To run this script at startup using systemctl, write /etc/systemd/system/gunicorn.service
# with the following contents:

# [Unit]
# After=network.target

# [Service]
# User=ubuntu
# Group=www-data
# WorkingDirectory=/home/ubuntu/yolov5
# ExecStart=/bin/bash start-gunicorn.sh

# [Install]
# WantedBy=multi-user.target

export NUM_CPUS=`nproc`
export NUM_WORKERS=$((2*$NUM_CPUS +0))
echo $NUM_WORKERS > /tmp/gunicorn_num_workers
/home/ubuntu/venvs/yolo5/bin/gunicorn --workers $NUM_WORKERS --bind localhost:5000 server:app
