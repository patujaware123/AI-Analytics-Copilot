# 🤖 AI Analytics Copilot – Intelligent Data Assistant

An AI-powered data analytics dashboard that helps users explore sales data, detect anomalies, generate forecasts, and ask natural-language questions using a local LLM.

## 🚀 Live Demo

👉 https://ai-analytics-copilot-cpwxvt2dpembwbzbzcv42q.streamlit.app/

## 💻 GitHub Repository

👉 https://github.com/patujaware123/AI-Analytics-Copilot

---

## 📊 Project Overview

**AI Analytics Copilot** is an interactive data analytics application built with Python and Streamlit.

It combines traditional data analytics with AI to help users:

- Upload CSV or Excel datasets
- Clean and validate data automatically
- Analyze sales and profit performance
- Detect potential data anomalies
- Forecast future sales
- Generate business insights
- Ask questions about the dataset using natural language
- Export cleaned data and anomaly reports

The goal is to simulate an **AI-powered Data Analyst** that can transform raw business data into actionable insights.

---

## ✨ Key Features

### 📁 Data Upload

- Upload CSV files
- Upload Excel files
- Automatic dataset loading
- Dataset preview

### 🧹 Data Cleaning

Automatically handles:

- Missing values
- Duplicate records
- Data validation

The application displays data quality information before and after cleaning.

### 📊 Business Dashboard

Interactive KPIs including:

- Total Sales
- Total Profit
- Total Orders
- Quantity Sold
- Total Customers

### 🔎 Interactive Filters

Users can filter the dataset by:

- Region
- Category
- Customer Type
- Payment Method

All dashboard metrics and charts update according to the selected filters.

---

## 📈 Data Visualizations

The dashboard provides multiple interactive visualizations:

- Sales Trend Over Time
- Sales by Category
- Sales by Region
- Profit by Category
- Top 10 Products by Sales
- Monthly Sales & Profit

These visualizations help identify sales trends, product performance, regional performance, and profitability.

---

## 🚨 AI Anomaly Detection

The application detects potential anomalies using the **Interquartile Range (IQR)** method.

Anomalies are identified in:

- Sales
- Profit

The dashboard also shows:

- Missing values before cleaning
- Missing values after cleaning
- Duplicate records
- Clean rows
- Sales anomalies
- Profit anomalies
- Total unique anomaly rows

This helps identify unusual business transactions and potential data-quality issues.

---

## 🔮 Sales Forecasting

The dashboard includes a simple sales forecasting module.

It:

1. Aggregates historical sales by month
2. Calculates a 3-month moving-average baseline
3. Forecasts the next 3 months
4. Displays historical and forecasted sales visually

> Forecast values are estimates based on historical sales patterns and should not be treated as guaranteed future results.

---

## 🤖 AI Analyst

Users can ask natural-language questions about the dataset.

The AI Analyst combines **Python/Pandas calculations with a local Llama 3.2 model**.

Python performs the actual data calculations, while the AI generates a clear business-friendly explanation of the verified results.

### 💬 Example Questions

```text
Which category has the highest sales?

Which region has the highest sales?

Which product has the highest sales?

Which category has the highest profit?

Show me the top 3 products by sales.

Which product has the lowest sales?

Compare Electronics and Fashion sales.

Give me 3 business recommendations based on the sales and profit data.
