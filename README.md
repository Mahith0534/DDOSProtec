# DDoS Protection System for Cloud Architecture

A comprehensive, multi-layered DDoS protection system designed for cloud environments, combining traditional security tools with machine learning-based threat detection.

## 🛡️ Architecture Overview

This system implements defense-in-depth strategy using multiple security layers:

- **Web Application Firewall (WAF)** - ModSecurity v3 with OWASP Core Rule Set
- **Rate Limiting** - Nginx-based traffic control
- **Intrusion Prevention** - fail2ban with automated blocking
- **Network Filtering** - iptables rules for packet-level protection
- **Behavioral Analysis** - CrowdSec community-driven threat intelligence
- **Network Monitoring** - Zeek with Zeek Flowmeter for traffic analysis
- **Machine Learning Detection** - Random Forest model for anomaly detection
- **Monitoring & Alerting** - Prometheus, Node Exporter, and Grafana stack

## 🚀 Features

### Core Protection Mechanisms
- **Real-time DDoS detection and mitigation**
- **Automated threat response and blocking**
- **Machine learning-based traffic classification**
- **Community-driven threat intelligence integration**
- **Comprehensive network traffic analysis**
- **Advanced rate limiting and throttling**

### Monitoring & Analytics
- **Real-time dashboards and visualization**
- **Performance metrics and system health monitoring**
- **Automated alerting for security events**
- **Historical attack pattern analysis**

## 🏗️ System Components

### 1. Nginx Rate Limiting
- Custom configuration rules for traffic shaping
- Geographic and IP-based rate limiting
- Burst handling and connection limits

### 2. fail2ban
- Automated IP banning based on suspicious patterns
- Custom filters for application-specific attacks
- Integration with iptables for dynamic blocking

### 3. iptables
- Kernel-level packet filtering
- DDoS-specific rules and connection tracking
- Rate limiting at network layer

### 4. ModSecurity v3 WAF
- OWASP Core Rule Set (CRS) implementation
- Application-layer attack prevention
- Custom rules for DDoS pattern detection

### 5. CrowdSec
- Community-driven threat intelligence
- Behavioral analysis and IP reputation
- Automated response and blocking decisions

### 6. Zeek Network Monitor
- Deep packet inspection and protocol analysis
- Zeek Flowmeter for enhanced flow monitoring
- Custom scripts for DDoS pattern detection

### 7. Machine Learning Model
- **Algorithm**: Random Forest Classifier
- **Training Datasets**:
  - CSE-CIC-IDS2018-AWS
  - CICIDS2017
  - CIC DoS 2016
- **Purpose**: Real-time traffic classification and anomaly detection

### 8. Monitoring Stack
- **Prometheus**: Metrics collection and storage
- **Node Exporter**: System-level metrics
- **Grafana**: Visualization and dashboards

## 📊 Machine Learning Model

### Training Data
The ML model is trained on three comprehensive datasets:
- **CSE-CIC-IDS2018-AWS**: Cloud-based intrusion detection dataset
- **CICIDS2017**: Modern intrusion detection evaluation dataset
- **CIC DoS 2016**: Specialized denial-of-service attack dataset

### Model Performance
- **Algorithm**: Random Forest
- **Features**: Network flow characteristics, packet statistics, timing patterns
- **Output**: Binary classification (Normal/Attack) with confidence scores

## 🛠️ Installation

### Prerequisites
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y
sudo apt install nginx fail2ban iptables-persistent

# CentOS/RHEL
sudo yum update
sudo yum install nginx fail2ban iptables-services
```

### Component Installation

#### 1. Nginx Configuration
```bash
sudo nano /etc/nginx/nginx.conf
```
##### Add in http module
```bash
client_body_timeout 10s;
        client_header_timeout 10s;
        keepalive_timeout 65;
        send_timeout 10s;
        limit_conn_zone $binary_remote_addr zone=conn_limit_per_ip:10m;
        limit_conn conn_limit_per_ip 20;
        limit_req_zone $binary_remote_addr zone=req_limit_per_ip:10m rate=5r/s;

        log_format ddos '$remote_addr - [$time_local] "$request" '
                        'Status: $status BodyBytes: $body_bytes_sent '
                        'ReqPerSecLimit: $limit_req_status ConnLimit: $connecti>
```
```bash
sudo nano /etc/nginx/sites-available/default
```
##### Add in server module
```bash
        access_log /var/log/nginx/ddos.log ddos;
        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                limit_req zone=req_limit_per_ip burst=10 nodelay;
                limit_conn conn_limit_per_ip 10;
                try_files $uri $uri/ =404;

```
```bash
sudo nginx -t
```

```bash
sudo systemctl reload nginx
```
#### 2. fail2ban Setup
```bash
# Install custom filters and actions
sudo nano /etc/fail2ban/filter.d/nginx-req-limit.conf
```

```bash
[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 3
bantime = 600

[nginx-botsearch]
enabled = true
filter = nginx-botsearch
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 2
bantime = 3600

[nginx-badbots]
enabled = true
filter = nginx-badbots
port = http,https
logpath = /var/log/nginx/access.log
maxretry = 2
bantime = 86400

[nginx-req-limit]
enabled = true
filter = nginx-req-limit
action = iptables-multiport[name=ReqLimit, port="http,https"]
logpath = /var/log/nginx/error.log
findtime = 600
bantime = 7200
maxretry = 10
```
```bash
sudo nano /etc/fail2ban/filter.d/nginx-req-limit.conf
```
```bash
[Definition]
failregex = limiting requests, excess:.* by zone.*client: <HOST>
ignoreregex =
```
```bash
sudo systemctl enable fail2ban
```

```bash
sudo systemctl restart fail2ban
```

```bash
sudo systemctl status fail2ban
```
#### 3. ModSecurity WAF
```bash
sudo apt update && sudo apt upgrade
# Install ModSecurity
sudo apt install gcc make build-essential autoconf automake libtool libcurl4-openssl-dev liblua5.3-dev libfuzzy-dev ssdeep gettext pkg-config libgeoip-dev libyajl-dev doxygen libpcre++-dev libpcre2-16-0 libpcre2-dev libpcre2-posix3 zlib1g zlib1g-dev -y

cd /opt && sudo git clone https://github.com/owasp-modsecurity/ModSecurity.git

cd ModSecurity

cd /opt && sudo git clone https://github.com/owasp-modsecurity/ModSecurity-nginx.git

sudo add-apt-repository ppa:ondrej/nginx -y

sudo apt update

sudo apt install nginx -y

sudo systemctl enable nginx


sudo systemctl status nginx

cd /opt && sudo wget https://nginx.org/download/nginx-1.25.4.tar.gz

sudo tar -xzvf nginx-1.25.4.tar.gz

cd nginx-1.25.4

sudo ./configure --with-compat --add-dynamic-module=/opt/ModSecurity-nginx

sudo make

sudo make modules

sudo git submodule init

sudo git submodule update

sudo ./build.sh

sudo ./configure

sudo make

sudo make install

sudo cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules-enabled/

sudo cp /opt/ModSecurity/modsecurity.conf-recommended /etc/nginx/modsecurity.conf

sudo cp /opt/ModSecurity/unicode.mapping /etc/nginx/unicode.mapping

sudo nano /etc/nginx/nginx.conf
# Add this line to main configuration
load_module /etc/nginx/modules-enabled/ngx_http_modsecurity_module.so;

sudo nano /etc/nginx/sites-enabled/default
modsecurity on;
modsecurity_rules_file /etc/nginx/modsecurity.conf;

sudo nano /etc/nginx/modsecurity.conf
SecRuleEngine On

sudo nginx -t

sudo systemctl restart nginx
# Configure with OWASP CRS
sudo cp configs/modsecurity/* /etc/modsecurity/
```

#### 4. CrowdSec
```bash
# Install CrowdSec
curl -s https://packagecloud.io/install/repositories/crowdsec/crowdsec/script.deb.sh | sudo bash
sudo apt install crowdsec
sudo apt install crowdsec-firewall-bouncer-iptables
sudo systemctl enable --now crowdsec
sudo systemctl status crowdsec
sudo cscli decisions list
```

#### 5. Zeek Installation
```bash
# Install Zeek
sudo apt install -y cmake make gcc g++ flex bison libpcap-dev libssl-dev python3 python3-dev swig zlib1g-dev libbz2-dev libcurl4-openssl-dev git
git clone --recursive https://github.com/zeek/zeek
cd zeek
./configure
make -j$(nproc)
sudo make install
zeek --version
echo 'export PATH=/usr/local/zeek/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

pip3 install zkg --user
echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
zkg autoconfig
zkg install zeek/zeek-flowmeter
@load zeek-flowmeter
echo "@load zeek-flowmeter" | sudo tee -a /usr/local/zeek/share/zeek/site/local.zeek
# Test Zeek
zeek -i eth0
# Test Zeek + Flowmeter
sudo zeek -i enp0s3 /usr/local/zeek/share/zeek/site/flowmeter/flowmeter.zeek
```

#### 6. Machine Learning Model
##### Extraction of features from Zeek
```bash
python3 extract.py
```
##### Import joblib file from repo
```bash
python3 ml.py
```

#### 7. Prometheus Setup
```bash
sudo useradd --no-create-home --shell /bin/false prometheus

sudo mkdir /etc/prometheus
sudo mkdir /var/lib/prometheus

sudo chown prometheus:prometheus /var/lib/prometheus

cd /tmp/
wget https://github.com/prometheus/prometheus/releases/download/v2.46.0/prometheus-2.46.0.linux-amd64.tar.gz

tar -xvf prometheus-2.46.0.linux-amd64.tar.gz
cd prometheus-2.46.0.linux-amd64
sudo mv console* /etc/prometheus
sudo mv prometheus.yml /etc/prometheus
sudo chown -R prometheus:prometheus /etc/prometheus

sudo mv prometheus /usr/local/bin/
sudo chown prometheus:prometheus /usr/local/bin/prometheus

sudo nano /etc/prometheus/prometheus.yml
sudo nano /etc/systemd/system/prometheus.service
```
```bash
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
    --config.file /etc/prometheus/prometheus.yml \
    --storage.tsdb.path /var/lib/prometheus/ \
    --web.console.templates=/etc/prometheus/consoles \
    --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl start prometheus
sudo systemctl enable prometheus
sudo systemctl status prometheus
```

```bash
sudo ufw allow 9090/tcp

http://server-IP-or-Hostname:9090
```

#### 8. Node Exporter Setup
```bash
cd /tmp
wget https://github.com/prometheus/node_exporter/releases/download/v1.6.1/node_exporter-1.6.1.linux-amd64.tar.gz
sudo tar xvfz node_exporter-*.*-amd64.tar.gz
sudo mv node_exporter-*.*-amd64/node_exporter /usr/local/bin/
sudo useradd -rs /bin/false node_exporter
sudo nano /etc/systemd/system/node_exporter.service
```
```bash
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl daemon-reload
sudo systemctl start node_exporter
sudo systemctl enable node_exporter
sudo systemctl status node_exporter
```
```bash
sudo nano /etc/prometheus/prometheus.yml
```
```bash
- job_name: 'Node_Exporter'
    scrape_interval: 5s
    static_configs:
      - targets: ['<Server_IP_of_Node_Exporter_Machine>:9100']
```
```bash
sudo systemctl restart prometheus
```

#### 9. Install Grafana
```bash
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt update
sudo apt install grafana
sudo systemctl start grafana-server
sudo systemctl status grafana-server
sudo systemctl enable grafana-server
```
http://your_ip:3000
Username – admin
Password – admin
- Add Data Source
- Name Prometheus and give prometheus source IP
- Save
- At the top right go to + icon
- Import Dashboard, Import from Grafana.com, 14513

## 📋 Testing

### Load Testing
```bash
# Apache Bench stress test
ab -n 10000 -c 100 http://your-server/

# Custom DDoS simulation
python3 tests/ddos_simulator.py --target http://your-server --threads 50
```
### Log Locations
- Nginx: `/var/log/nginx/`
- fail2ban: `/var/log/fail2ban.log`
- CrowdSec: `/var/log/crowdsec.log`
- Zeek: `/opt/zeek/logs/`
- ML Detector: `/var/log/ddos-ml/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

### Development Guidelines
- Follow security best practices
- Include tests for new features
- Update documentation
- Validate against test datasets

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OWASP Foundation** for the Core Rule Set
- **CrowdSec Community** for threat intelligence
- **Zeek Project** for network monitoring capabilities
- **Canadian Institute for Cybersecurity** for the training datasets
- **Elastic Security Research** for ML techniques and methodologies

## 📚 References

- [OWASP ModSecurity Core Rule Set](https://owasp.org/www-project-modsecurity-core-rule-set/)
- [CrowdSec Documentation](https://docs.crowdsec.net/)
- [Zeek Network Security Monitor](https://zeek.org/)
- [CSE-CIC-IDS2018 Dataset](https://www.unb.ca/cic/datasets/ids-2018.html)
- [CICIDS2017 Dataset](https://www.unb.ca/cic/datasets/ids-2017.html)

---

**⚠️ Security Notice**: This system is designed for legitimate DDoS protection. Ensure compliance with local laws and regulations when deploying in production environments.
