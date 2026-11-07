<div align="center">


<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=27&duration=3300&pause=1100&color=58A6FF&center=true&vCenter=true&width=700&repeat=true&lines=Patrik+Thormodsen;Computer+Engineering+Student;Full-stack+Developer" alt="Patrik Thormodsen" />

<a href="https://portfolio.patreek.no">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="dark_mode.svg" />
    <img src="light_mode.svg" alt="Patrik Thormodsen: Computer Engineering student at HVL in Bergen. Java, TypeScript, Python. Self-hosting, homelab, gym, padel and gaming." width="100%" />
  </picture>
</a>

</div>

<h3 align="center">About me</h3>

I'm a Computer Engineering student at HVL in Bergen, Norway. I enjoy programming and spend a lot of my free time working on personal projects.
I mainly work with Java, Spring Boot, React and TypeScript, and enjoy both developing applications and figuring out how to deploy and run them.
Lately, I've also been getting into self-hosting and running my own homelab with Proxmox, Docker and Kubernetes (k3s).
Outside of programming, I enjoy going to the gym, playing padel and spending time with friends. I'm also into gaming, especially Soulslike games.

<p align="center"><a href="https://portfolio.patreek.no"><b>Portfolio</b></a></p>

---

<h3 align="center">Tech Stack</h3>

<div align="center">

**Languages**

<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=java%2Cts%2Cjs%2Cpy%2Chaskell&theme=light" />
  <img src="https://skillicons.dev/icons?i=java,ts,js,py,haskell&theme=dark" alt="Java, TypeScript, JavaScript, Python, Haskell" height="44" />
</picture>

<br>

**Frameworks & Databases**

<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=spring%2Creact%2Cfastapi%2Cpostgres%2Ctailwind&theme=light" />
  <img src="https://skillicons.dev/icons?i=spring,react,fastapi,postgres,tailwind&theme=dark" alt="Spring Boot, React, FastAPI, PostgreSQL, Tailwind CSS" height="44" />
</picture>

<br>

**Infrastructure & Tools**

<p>
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=linux%2Cdocker%2Ckubernetes&theme=light" />
    <img src="https://skillicons.dev/icons?i=linux,docker,kubernetes&theme=dark" alt="Linux, Docker, Kubernetes" height="44" />
  </picture>
  <img src="https://cdn.simpleicons.org/proxmox/E57000" height="44" alt="Proxmox VE" />
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="https://skillicons.dev/icons?i=cloudflare%2Cgithubactions%2Cgit&theme=light" />
    <img src="https://skillicons.dev/icons?i=cloudflare,githubactions,git&theme=dark" alt="Cloudflare, GitHub Actions, Git" height="44" />
  </picture>
</p>

</div>

---

<h3 align="center">Featured Projects</h3>

<div align="center">

| Project | Description | Links |
| :--- | :--- | :--- |
| **SeatSense** | IoT-based seat occupancy monitoring using ESP32 sensors and React. | [Demo](https://seatsense.patreek.no) · [Code](https://github.com/pthormodsen/SeatSense) |
| **QuizApp** | Full-stack study application built with Spring Boot and React. | [Demo](https://quiz.patreek.no) · [Code](https://github.com/pthormodsen/QuizApp) |
| **Phishing URL Detector** | Machine learning URL classifier with FastAPI and a React frontend. | [Demo](https://phishing.patreek.no) · [Code](https://github.com/pthormodsen/PhishingURL) |
| **Chess** | Java chess application with Stockfish integration. | [Demo](https://chess.patreek.no) · [Code](https://github.com/pthormodsen/Chess) |
| **Portfolio** | My personal site and blog, with a typing test and shared leaderboard. | [Site](https://portfolio.patreek.no) · [Code](https://github.com/pthormodsen/portfolio) |

All demos are self-hosted on my own k3s cluster.

</div>

---

<h3 align="center">Homelab</h3>

I run a small homelab on **Proxmox VE** with three machines: **zoro**, **sanji** and **luffy**. Zoro and sanji are always on, luffy is my loudest PC and only gets turned on for game servers.

Most of my projects run on a **k3s** cluster across zoro and sanji, with two replicas of each app spread over both machines, so one of them can go down without the sites going offline. Traffic comes in through **Cloudflare Tunnels**, images are built with **GitHub Actions** and stored on **GHCR**, and I use **Tailscale** for remote access and **Uptime Kuma** for monitoring.

The databases still only run on one machine, so next up is adding a small third node and setting up replicated Postgres, so those can survive a machine going down too.

<p align="center">
  <img src="assets/proxmox.png" alt="Proxmox cluster with zoro, sanji and luffy" width="100%" />
  <br><br>
  <img src="assets/k9s.png" alt="k9s showing every app running as two replicas across both nodes" width="100%" />
</p>

<p align="center"><a href="https://portfolio.patreek.no/blog/moving-my-homelab-to-k3s">How I set it up →</a></p>

---

<h3 align="center">GitHub Activity</h3>

<div align="center">

<picture>
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/pthormodsen/pthormodsen/output/github-snake.svg" />
  <img src="https://raw.githubusercontent.com/pthormodsen/pthormodsen/output/github-snake-dark.svg" alt="GitHub Contribution Snake" />
</picture>

</div>
