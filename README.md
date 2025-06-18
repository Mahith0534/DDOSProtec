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
# Copy nginx configuration
sudo nano /etc/nginx/nginx.conf
```
```bash

```

#### 2. fail2ban Setup
```bash
# Install custom filters and actions
sudo cp configs/fail2ban/jail.local /etc/fail2ban/
sudo cp configs/fail2ban/filters/* /etc/fail2ban/filter.d/
sudo systemctl restart fail2ban
```

#### 3. ModSecurity WAF
```bash
# Install ModSecurity
sudo apt install libmodsecurity3 modsecurity-crs
# Configure with OWASP CRS
sudo cp configs/modsecurity/* /etc/modsecurity/
```

#### 4. CrowdSec
```bash
# Install CrowdSec
curl -s https://install.crowdsec.net | sudo sh
sudo cp configs/crowdsec/* /etc/crowdsec/
```

#### 5. Zeek Installation
```bash
# Install Zeek
sudo apt install zeek zeek-flowmeter
sudo cp configs/zeek/* /opt/zeek/share/zeek/site/
```

#### 6. Monitoring Stack
```bash
# Deploy with Docker Compose
docker-compose up -d prometheus grafana node-exporter
```

## ⚙️ Configuration

### Environment Variables
```bash
export DDOS_THRESHOLD=1000
export RATE_LIMIT=100
export ML_MODEL_PATH="/opt/ddos-protection/models/random_forest.pkl"
export GRAFANA_ADMIN_PASSWORD="your-secure-password"
```

### Key Configuration Files
- `configs/nginx/nginx.conf` - Main Nginx configuration
- `configs/fail2ban/jail.local` - fail2ban rules and thresholds
- `configs/iptables/rules.v4` - iptables DDoS protection rules
- `configs/modsecurity/main.conf` - ModSecurity WAF configuration
- `configs/crowdsec/config.yaml` - CrowdSec behavioral analysis
- `configs/zeek/local.zeek` - Zeek monitoring scripts
- `docker-compose.yml` - Monitoring stack deployment

## 📈 Monitoring & Dashboards

### Grafana Dashboards
- **DDoS Protection Overview**: Real-time attack statistics
- **System Performance**: Resource utilization and health
- **Network Traffic Analysis**: Flow patterns and anomalies
- **ML Model Performance**: Prediction accuracy and alerts

### Key Metrics
- Requests per second and connection counts
- Blocked IPs and attack patterns
- System resource utilization
- ML model prediction confidence
- Response times and availability

## 🔧 Usage

### Starting the Protection System
```bash
# Start all services
sudo systemctl start nginx fail2ban crowdsec zeek
sudo iptables-restore < /etc/iptables/rules.v4

# Start monitoring
docker-compose up -d

# Start ML detection service
python3 ml_detector/ddos_detector.py --config configs/ml_config.yaml
```

### Monitoring Commands
```bash
# Check fail2ban status
sudo fail2ban-client status

# View CrowdSec decisions
sudo cscli decisions list

# Check blocked IPs
sudo iptables -L -n | grep DROP

# Monitor Zeek logs
tail -f /opt/zeek/logs/current/conn.log
```

## 🚨 Alert Configuration

### Prometheus Alerts
- High request rate detection
- System resource exhaustion
- ML model anomaly threshold exceeded
- Service availability issues

### Integration Options
- **Slack/Discord**: Real-time notifications
- **Email**: Critical alert summaries
- **PagerDuty**: Incident management
- **Webhook**: Custom integrations

## 📋 Testing

### Load Testing
```bash
# Apache Bench stress test
ab -n 10000 -c 100 http://your-server/

# Custom DDoS simulation
python3 tests/ddos_simulator.py --target http://your-server --threads 50
```

### Validation Scripts
```bash
# Test all components
bash tests/system_test.sh

# Validate ML model
python3 tests/ml_model_test.py
```

## 🐛 Troubleshooting

### Common Issues
1. **High False Positives**: Adjust ML model threshold in `ml_config.yaml`
2. **Legitimate Traffic Blocked**: Review and whitelist in `fail2ban/jail.local`
3. **Performance Issues**: Tune rate limits in `nginx.conf`
4. **Memory Usage**: Monitor Zeek and adjust retention policies

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

## 📞 Support

For questions, issues, or contributions:
- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)
- **Email**: [your-email@domain.com]

---

**⚠️ Security Notice**: This system is designed for legitimate DDoS protection. Ensure compliance with local laws and regulations when deploying in production environments.
