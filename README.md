<h1 align="center">Remote Device Monitoring System</h1>

## Overview
This project is an **Enterprise Remote Device Monitoring System** designed to manage, monitor, and update multiple remote devices seamlessly. It includes automated script deployment, data collection, and a centralized control dashboard.

The system is divided into four main components:

1. **Startup Script Downloader** – Automatically downloads and deploys updated scripts to remote devices via FTP, ensuring continuous operation and updates.  
2. **Device Monitor Agent** – Runs on each device to collect system data, screenshots, and logs, and reports them back to the central dashboard.  
3. **FTP Image Downloader** – Fetches screenshots and other image files from devices via FTP and organizes them for monitoring and analysis.  
4. **Device Control Dashboard** – Centralized interface for monitoring all devices, executing remote commands, and visualizing collected data.

---

## Features
- Automated script deployment and updates  
- Real-time device monitoring  
- Remote command execution from a secure dashboard  
- FTP-based data transfer and storage  
- Organized storage for images and logs  
- Enterprise-level centralized management system  

---

## FTP & Hosting
- **FTP Server for Scripts:** [MonsterASP](https://www.monsterasp.net/)  
- **Database Hosting:** [InfinityFree](https://dash.infinityfree.com/)  

Scripts and image files are transferred securely via FTP and managed centrally through the dashboard.

---

## GUI Examples

**Image Downloader GUI**  
<img src="path_to_your_image1.png" alt="FTP Image Downloader GUI" width="600">

**Device Startup Script GUI**  
<img src="path_to_your_image2.png" alt="Startup Script Downloader GUI" width="600">

---

## Technologies Used
- Python (for agents and downloaders)  
- FTP for file transfer  
- Windows Startup folder for automated execution  
- MySQL or similar (hosted on InfinityFree) for database  
- GUI interfaces for management and monitoring  
