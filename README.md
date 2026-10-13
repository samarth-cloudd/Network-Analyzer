# 🌐 Network Health & Security Analyzer

A web-based network monitoring project designed to analyze network performance and provide a clear overview of network health. The project combines a visual dashboard with a Python Flask backend to retrieve network telemetry data.

**Live Demo:** [https://network-analyzer-frontend.vercel.app/](https://network-analyzer-frontend.vercel.app/)

**GitHub Repository:** [https://github.com/samarth-cloudd/Network-Analyzer](https://github.com/samarth-cloudd/Network-Analyzer)

> 🚧 **Project Status:** Work in Progress — this project is actively being developed. New monitoring features, security analysis capabilities, and performance improvements will be added over time.

## 📌 About the Project

The Network Health & Security Analyzer aims to make network monitoring easier through an interactive dashboard. It collects network performance metrics from a backend API and displays the results in a visual interface.

The project is intended as a learning and development project for understanding computer networks, Python backend development, API communication, and web deployment.

## ✨ Current Features

- **Network Latency:** Displays average response time.
- **Jitter Monitoring:** Displays variation in response time.
- **DNS Response Time:** Measures the time taken for DNS resolution.
- **Network Health Score:** Calculates a score using latency and packet-loss data.
- **Route Information:** Displays route-related fields; actual traceroute measurements are planned for a future update.
- **Interactive Dashboard:** Presents network metrics through a visual web interface.
- **Cloud Deployment:** Frontend hosted on Vercel and backend hosted on Render.
- **Mobile Support:** Dashboard can be accessed from mobile and desktop browsers.

## 🛠️ Technology Stack

| Component               | Technology            |
| ----------------------- | --------------------- |
| Frontend                | HTML, CSS, JavaScript |
| Dashboard Visualization | Three.js              |
| Styling                 | Tailwind CSS          |
| Backend                 | Python, Flask         |
| Network Testing         | Ping, DNS resolution  |
| API Communication       | REST API, JSON        |
| Deployment              | Vercel, Render        |
| Version Control         | Git and GitHub        |

## 🏗️ Project Structure

```text
Network-Analyzer/
├── backend/
│   ├── app.py
│   ├── ping_test.py
│   ├── dns_test.py
│   ├── trace_test.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   └── index.html
└── README.md
```

## 🚀 Getting Started

### Prerequisites

Install the following on Ubuntu:

- Python 3
- Git
- pip
- A modern web browser

### 1. Clone the Repository

```bash
git clone https://github.com/samarth-cloudd/Network-Analyzer.git
cd Network-Analyzer
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Install Network Utilities

```bash
sudo apt update
sudo apt install iputils-ping dnsutils traceroute
```

### 5. Start the Backend

```bash
cd backend
python app.py
```

The Flask server should start on the configured local address and port. Check `app.py` for the exact port and configuration.

### 6. Open the Frontend

Open `frontend/index.html` in your browser, or serve the frontend using a local static web server.

**Note:** The frontend currently calls the deployed Render API. If you want to test a local backend, update the API URL in `frontend/index.html` to match your local server and configure CORS if necessary.

## 🔌 API Endpoint

The backend provides a network telemetry endpoint:

```http
GET /api/network?target=google.com
```

Example deployed endpoint:

[https://network-analyzer-2-0tl8.onrender.com/api/network?target=google.com](https://network-analyzer-2-0tl8.onrender.com/api/network?target=google.com)

The API returns JSON containing network metrics. Example fields include:

```json
{
  "target": "google.com",
  "ip": "142.250.73.110",
  "average_latency": 7.67,
  "jitter": 0.29,
  "dns_response": 14.55,
  "packet_loss": 0.0,
  "packets_sent": 4,
  "packets_received": 4,
  "route_hops": 0,
  "route_dropouts": 0
}
```

*Example response only. IP addresses and measurements vary with the target, network, and time.*

## 🗺️ Development Roadmap

The following features are planned for future development:

- [ ] Implement real traceroute-based route-hop and dropout measurements.
- [ ] Add target selection so users can analyze different hosts.
- [ ] Improve network health scoring and explain the score.
- [ ] Add historical telemetry and performance graphs.
- [ ] Add network availability and uptime monitoring.
- [ ] Improve API error handling and loading indicators.
- [ ] Add network security checks and useful security alerts.
- [ ] Improve mobile responsiveness and dashboard usability.
- [ ] Add automated testing and deployment improvements.
- [ ] Improve documentation and usage examples.

The roadmap may change as development progresses.

## 🔐 Security and Responsible Use

This project is intended for educational and authorized network monitoring. Only analyze systems and networks you own or have permission to test.

Future security features will be developed with safe testing practices in mind.

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Test your changes.
5. Submit a pull request.

## 📄 License

A license has not yet been specified. Add a `LICENSE` file before distributing the project under a particular open-source license.

## 👨‍💻 Author

**Samarth**

GitHub: [https://github.com/samarth-cloudd](https://github.com/samarth-cloudd)

---

⭐ If you find this project interesting, consider starring the repository. Follow the project as it continues to grow!

