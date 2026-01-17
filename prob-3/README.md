# 🚀 JobMatch: The Next-Gen Job Discovery Dashboard

> **A high-performance, interactive job finding experience built with modern web technologies.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-Fast-646CFF?logo=vite&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-38B2AC?logo=tailwindcss&logoColor=white)

---

## 🔥 Overview

**JobMatch** isn't just a list of jobs; it's a dynamic discovery engine. Designed to help users find their dream role instantly, it features real-time filtering, intelligent matching scores, and a buttery-smooth UI that respects user preferences across sessions.

Whether on a massive desktop monitor or a mobile device on the go, JobMatch adapts perfectly to provide a premium experience.

## ✨ Key Features

-   **⚡ Blazing Fast Performance**: Powered by Vite and optimized React hooks.
-   **🧠 Intelligent Matching**: Custom `useJobDiscovery` hook calculates real-time match scores based on skills, experience, and salary requirements.
-   **🔗 Deep Linking**: Share your exact search results with URL synchronization. Filters update the URL, and the URL updates the filters.
-   **💾 Persistent State**: "Saved Jobs" are stored locally, so your favorites are waiting for you when you return.
-   **🎨 Responsive Design**: A mobile-first approach with a sleek drawer for filters on smaller screens and a robust sidebar for desktop.
-   **🕶️ Skeleton Loading**: Polished loading states (simulated latency) for a perceived performance boost.

## 🛠️ Tech Stack

-   **Framework**: React 19
-   **Language**: TypeScript (Strict Mode)
-   **Styling**: Tailwind CSS v4 (w/ PostCSS)
-   **Build Tool**: Vite
-   **Testing**: Jest + React Testing Library
-   **Icons**: Lucide React

## 🚀 Getting Started

### Prerequisites

-   Node.js (v18+ recommended)
-   npm or yarn

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/AgroKING/Performatives.git
    cd Performatives/prob-3
    ```

2.  **Install Dependencies**
    ```bash
    npm install
    ```

3.  **Run Development Server**
    ```bash
    npm run dev
    ```
    Open [http://localhost:5173](http://localhost:5173) in your browser.

## 🧪 Running Tests

Ensure code stability with our comprehensive test suite.

```bash
# Run all unit and integration tests
npm test

# Run type checks
npx tsc --noEmit
```

## 📂 Project Structure

```
prob-3/
├── src/
│   ├── components/       # UI Components (JobCard, FilterPanel, MatchRing)
│   ├── App.tsx           # Main Application Layout & State
│   ├── useJobDiscovery.ts # Core Logic Hook
│   ├── types.ts          # TypeScript Definitions
│   ├── jobs.json         # Mock Data
│   └── main.tsx          # Entry Point
├── package.json
├── vite.config.ts
└── tailwind.config.js
```


