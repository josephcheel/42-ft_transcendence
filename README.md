<!--HEADER-->
<h1 align="center"> ft_transcendence | 
  <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://cdn.simpleicons.org/42/white">
  <img alt="42" width=40 align="center" src="https://cdn.simpleicons.org/42/Black">
 </picture>
 Cursus 
  <img alt="Complete" src="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/dark-theme/complete.svg">
</h1>
<!--FINISH HEADER-->

> A web application focused on replicating the classic Pong game. It includes features like real-time multiplayer gameplay, tournaments, and user management for a competitive and engaging experience.

https://github.com/user-attachments/assets/63c137d9-7b9b-4e65-b5f0-1edf1cb4a676

> [!WARNING]
> 🔴***MORE VIDEOS AND IMAGES BELOW AT THE GALLERY SECTION!🖼️🖼️🖼️*** 


## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation-and-configuration)
- [Usage](#usage)
- [Gallery](#gallery)

## Introduction
## Features

- **Backend** powered by [Django](https://www.djangoproject.com/)
- **Frontend** built with [Vue.js](https://vuejs.org/) and styled using [Bootstrap](https://getbootstrap.com/)
- **Data storage** using [PostgreSQL](https://www.postgresql.org/) database
- **Blockchain integration** for secure and transparent tournament results
- **Real-time gameplay** with WebSockets for remote players
- **Tournaments** and **local match** support for competitive and casual play
- **Friends system** to connect and play with others
- **User & game statistics dashboards** for insightful analytics
- **Log management** via the ELK Stack (Elasticsearch, Logstash, Kibana)
- **Monitoring & alerting** with [Prometheus](https://prometheus.io/) and [Grafana](https://grafana.com/)
- **Microservices architecture** with RESTful APIs
- **Responsive design** for seamless use across devices
- **Multilingual support** for a global user base

## Installation and Configuration
### 📦 Prerequisites for Installation

Before installing and running the project, make sure the following are available on your system:

- **Docker**  
- **Docker Compose**
- **Make** (for running setup commands)
- **.env** file with the required environment variables

### 1. Copy the **env_sample** as **.env** and change whatever you consider

### 2. (OPTIONAL) Set a variable if you want to be availeable for your network, if not set defaults to localhost
```bash
export IP_ADDR="{YOUR_IP}"
```


### 3. (OPTIONAL) You can also chage the SSL_CERT_FILE and SSL_CERT_KEY in the .env to add your own certificates paths, if you don't specify a SSL_CERT_FILE and SSL_CERT_KEY by default will generate a selfsigned.crt and selfsigned.key  
```
SSL_CERT_FILE="{YOUR_FILE_CRT_PATH}"
SSL_CERT_KEY="{YOUR_FILE_KEY_PATH}"
```

### 4. Execute
```bash
make
```

## Usage
> [!NOTE]
> If you've done the second step of the [Installation and Configuration section](#installation-and-configuration) you'll use the first option
if you set your own IP_ADDR environment variable then access via:
```
https://{YOUR_IP}:8000 
https://{YOUR_IP}:4000
```

if you have not set IP_ADDR then use:
```
https://localhost:8000 
https://localhost:4000
```

## Gallery
<div align="center">

<h3><strong>A few example of the application showing what our project can do.</strong> </h3>

---

https://github.com/user-attachments/assets/5e5b75f8-6c7c-47a8-9729-9ed38ac4a776

***Register preview***


---

https://github.com/user-attachments/assets/e0c0020f-957a-437a-97c5-3a56e5914ca3

***Game on Phone***

---

![](https://github.com/josephcheel/42-ft_transcendence/blob/main/readme/Games.webp)

***Games Page***

---
![](https://github.com/josephcheel/42-ft_transcendence/blob/main/readme/Game1.webp)

***Game Screenshot***



![Friends](https://github.com/josephcheel/42-ft_transcendence/blob/main/readme/friends.webp)

***Friends Page***
</div>
