# 🛡️ GRC Third-Party Risk Assessment Dashboard

**Live Demo:** https://share.streamlit.io/-/auth/app?redirect_uri=https%3A%2F%2Fgrcdashboard.streamlit.app%2F

An interactive dashboard for assessing third-party vendor risk, built with Python, Streamlit, and Plotly. This tool provides a data-driven approach to help organizations prioritize threats and avoid costly compliance failures.


## 🎯 The Business Problem

Ineffective vendor oversight can lead to data breaches and massive regulatory fines, such as the **$200M+ fines faced by Morgan Stanley**. This dashboard simulates a real-world GRC solution, empowering risk managers to visualize complex data, identify high-risk vendors, and make informed decisions quickly.

## ✨ Key Features

* **Interactive Risk Matrix:** A heatmap visualizing the likelihood and impact of vendor risks.
* **Dynamic Filtering:** Users can drill down into the data by risk level, service type, and country.
* **Compliance Tracking:** Monitors vendor compliance against key frameworks like ISO 27001.
* **Specialized AI Risk View:** A dedicated tab assesses AI vendors against emerging threats from the OWASP Top 10 for LLMs.
* **Predictive Scoring:** Each vendor is assigned a "Breach Likelihood Score" based on vulnerabilities and compliance gaps.

## 🛠️ Tech Stack

* **Language:** Python 3.8
* **Core Libraries:** Streamlit, Pandas, Plotly, NumPy
* **Environment:** venv (Virtual Environment)
* **IDE:** Visual Studio Code
* **Deployment:** Streamlit Community Cloud

## 🚀 Getting Started

Follow these instructions to set up and run the project locally.

### Prerequisites

* Python 3.8 or higher
* Git

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/grc-risk-dashboard.git](https://github.com/your-username/grc-risk-dashboard.git)
    cd grc-risk-dashboard
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv env
    source env/bin/activate

    # For Windows
    python -m venv env
    .\env\Scripts\activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```
    Your browser will automatically open with the running application.

