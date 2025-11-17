#!/bin/bash

# Update system packages
sudo yum update -y

# Install Python and required system packages
sudo yum install -y python3 python3-pip python3-venv nginx

# Create application directory
sudo mkdir -p /var/www/resume-bot
sudo chown -R $USER:$USER /var/www/resume-bot

# Clone the repository (if not already done)
# git clone https://github.com/yourusername/resume-bot.git /var/www/resume-bot

# Create and activate virtual environment
cd /var/www/resume-bot
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create systemd service file
sudo tee /etc/systemd/system/resume-bot.service << EOF
[Unit]
Description=Resume Bot FastAPI Application
After=network.target

[Service]
User=$USER
Group=$USER
WorkingDirectory=/var/www/resume-bot
Environment="PATH=/var/www/resume-bot/venv/bin"
ExecStart=/var/www/resume-bot/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
sudo tee /etc/nginx/conf.d/resume-bot.conf << EOF
server {
    listen 80;
    server_name 92.205.167.70;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOF

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Start the application service
sudo systemctl start resume-bot
sudo systemctl enable resume-bot

echo "Deployment completed! The application should be running at http://92.205.167.70" 