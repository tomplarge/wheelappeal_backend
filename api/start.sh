exec nohup  gunicorn api:flask_app --bind 0.0.0.0:5000 >> /home/ec2-user/api.log 2>&1
