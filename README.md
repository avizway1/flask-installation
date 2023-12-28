# flask-installation


**STEP 1: Install Python 3 and pip and Required dependencies**

```bash
sudo yum install python3 -y
```

```bash
sudo yum install gcc python3-devel -y
```
**Install Virtualenv and activate it (Optional step but recommended to use)**

```bash
sudo pip3 install virtualenv
```

**Navigate to the project path and Activate the virtual environment**

My present working directory is /home/ec2-user and am creating my project directory in this location. 

```bash
mkdir myflask-proj
```

```bash
cd /home/ec2-user/myflask-proj
```

When you run below command, it will create a directory named venv (or whatever name you specified) in the current working directory. Inside this directory, it will set up a complete Python environment, including a copy of the Python interpreter, the standard library, and various supporting files

```bash
python3 -m venv venv
```
After creating the virtual environment, you need to activate it. Activation is a process that modifies your shell's environment to use the Python interpreter and other tools from the virtual environment. You can observer (venv) in terminal.

```bash
source venv/bin/activate
```

**Step 2 : Install Flask and Dependencies**

```bash
pip install Flask gunicorn
```

**Create a sample flask application**

Create a file with name app.py and add below content.

```bash
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='Home', content='Hello, Flask!')

if __name__ == '__main__':
    app.run(debug=True)
```

Now create a folder and name it as "templates" and create the required webpages.

```bash
mkdir templates
```

inside the templates folder create index.html file and add below content.

```bash
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ content }}</h1>
</body>
</html>

```

also, create a file with name 500.html in templates path

```bash
touch /home/ec2-user/myflask-proj/templates/500.html
```

provide read permissions to the flask app content

```bash
sudo chmod -R +r /home/ec2-user/myflask-proj
```


**Step 3: Run Flask Application**

This command runs Gunicorn with 2 worker processes, binding to all available network interfaces on port 5000. Adjust the number of workers based on your server's resources. Make sure your ec2 instance is opened with port 5000.

```bash
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

Above process will run flask application, but when you press Ctrl+C this stop working.


**Step 4 : Set Up Nginx as a Reverse Proxy (Optional step but recommended to use)**

Install nginx

```bash
sudo amazon-linux-extras install nginx1
```

Create a new Nginx configuration file:

```bash
vim /etc/nginx/conf.d/flask-app.conf
```

add below content to the flask-app.conf file, Make sure you adjust the paths of your project accordingly.

```bash
server {
    listen 80;
    server_name ec2-52-66-143-134.ap-south-1.compute.amazonaws.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /home/ec2-user/myflask-proj/static;
    }

    location /favicon.ico {
        alias /home/ec2-user/myflask-proj/favicon.ico;
    }

    error_page 500 502 503 504 /500.html;
    location = /500.html {
        root /home/ec2-user/myflask-proj/templates;
    }
}
```

Now adjust the nginx configuration file as below:

**Note** : you can add below one line to the configuration file. For reference am sharing entire nginx configuration here.

Add this **server_names_hash_bucket_size 128;** under http. 

Nginx conf file path : /etc/nginx/nginx.conf


```bash

# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 4096;

server_names_hash_bucket_size 128;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

    server {
        listen       80;
        listen       [::]:80;
        server_name  _;
        root         /usr/share/nginx/html;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        error_page 404 /404.html;
        location = /404.html {
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
        }
    }

# Settings for a TLS enabled server.
#
#    server {
#        listen       443 ssl http2;
#        listen       [::]:443 ssl http2;
#        server_name  _;
#        root         /usr/share/nginx/html;
#
#        ssl_certificate "/etc/pki/nginx/server.crt";
#        ssl_certificate_key "/etc/pki/nginx/private/server.key";
#        ssl_session_cache shared:SSL:1m;
#        ssl_session_timeout  10m;
#        ssl_ciphers PROFILE=SYSTEM;
#        ssl_prefer_server_ciphers on;
#
#        # Load configuration files for the default server block.
#        include /etc/nginx/default.d/*.conf;
#
#        error_page 404 /404.html;
#            location = /40x.html {
#        }
#
#        error_page 500 502 503 504 /50x.html;
#            location = /50x.html {
#        }
#    }

}
```

run below command to test the nginx syntax errors or misconfigurations.

```bash
sudo nginx -t
```

Now, restart the nginx server. verify the log file for error. 


```bash
sudo systemctl restart nginx
```

if you are getting forbidden error, provide read permissions to the flask app content again.

```bash
sudo chmod -R +r /home/ec2-user/myflask-proj
```

***To run Gunicorn in the background more persistently, you can use the nohup command.***

```bash
nohup gunicorn -w 1 -b 127.0.0.1:5000 app:app > gunicorn.log 2>&1 &
```

If you want to stop the Gunicorn process, you can use the pkill command:

```bash
pkill gunicorn
```

nginx log file verification.

```bash
sudo tail -n 20 /var/log/nginx/error.log
```

To verify gunicon logs

```bash
tail -f gunicorn.log
```

=====================

if you want to try with some other code, you can replace the app.py and copy remaining data to "templates" folder.
