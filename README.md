# 📊 PhonePe Transaction Insights

A data engineering and analytics project that extracts insights from PhonePe transaction data. This project loads transaction data from JSON files, stores it into a MySQL database, and enables analysis using Python and SQL.

---

## 🚀 Features

- Parse and load JSON data (e.g., transactions by state, district, category).
- Store structured data into MySQL tables.
- Automate schema creation based on JSON keys.
- Insert data with proper type detection (int, float, string, datetime).
- Enables SQL-based analysis and dashboards.

---

## 🛠️ Tech Stack

- **Python** (Data loading & ETL)
- **MySQL** (Relational database)
- **SQLAlchemy** (ORM + connection handling)
- **Pandas** (Data manipulation)
- **JSON** (Data source)

---

## 📁 Folder Structure

- 📂 phonepe-insights/
- ├── data/
- │ └── transactions.json
- ├── scripts/
- │ └── insert_to_mysql.py
- ├── requirements.txt
- └── README.md

---

## ⚙️ Setup Instructions

1. **Clone the repository**

git clone https://github.com/Aastha2675/phonepe-insights.git
cd phonepe-insights

2. **Install dependencies**

pip install -r requirements.txt


3. **Configure MySQL**

Create a database named phonepe_db
Update the connection details in insert_to_mysql.py


4. **Run the script**


## 📈 Future Improvements

- 🗺️ Enhance choropleth map with **3D visualization** using advanced Plotly or WebGL libraries.
- 🤯 Build a **"Fun Facts" section** to highlight interesting and surprising statistics from the data.
- 📊 Add an **Insights & Conclusion page** to summarize key findings and trends from the analysis.
- 🔄 Add support for **nested JSON parsing** for more complex PhonePe data structures.
- 🌐 Build an interactive **dashboard using Streamlit or Plotly Dash**.
- ⏱️ Schedule **automated ETL jobs** using Airflow or Cron for regular updates.
- ✅ Add **unit tests and data validation checks** for robustness.  


## 📜 License

This project is licensed under the MIT License.

## 👩‍💻 Author
Aastha Mhatre
Data & Software Enthusiast | Python | SQL | ML | React

---



