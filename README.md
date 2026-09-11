#🤖 AI Analytics Copilot

An AI-powered Data Analyst dashboard that combines **Python/Pandas analytics, anomaly detection, sales forecasting, and local Llama 3.2 AI** to turn raw business data into actionable insights.

## 📌 Project Overview

**AI Analytics Copilot – Intelligent Data Assistant** is an interactive analytics application built with Streamlit.

Users can upload a CSV or Excel dataset, apply business filters, explore KPIs and charts, detect unusual sales/profit records, generate a sales forecast, and ask natural-language questions about the data.

A key design principle is that **Python/Pandas performs numerical calculations while the local LLM provides business-language interpretation**. This reduces the risk of incorrect AI-generated calculations.

## ✨ Features

### 📊 Interactive Business Dashboard
- Total Sales
- Total Profit
- Total Orders
- Quantity Sold
- Total Customers
- Sales trend over time
- Sales by category
- Sales by region
- Profit by category
- Top 10 products by sales
- Monthly sales and profit

### 🎛️ Dynamic Filters
- Region
- Category
- Customer Type
- Payment Method

### 🧹 Data Cleaning
- Detect missing values
- Detect duplicate rows
- Automatic missing-value handling
- Before/after cleaning metrics

### 🚨 Anomaly Detection
Uses the **IQR (Interquartile Range)** method to identify unusual:
- Sales values
- Profit values

### 🔮 Sales Forecasting
Generates a **3-month sales forecast** using a simple 3-month moving-average baseline.

### 🤖 AI Analyst
Supports natural-language questions such as:

- Which category has the highest sales?
- Which region has the highest sales?
- Which product has the highest sales?
- Which category has the highest profit?
- Which product has the lowest sales?
- Show me the top 3 products.
- Compare Electronics and Fashion sales.
- Give me 3 business recommendations.

For numerical questions, **Python/Pandas performs the calculation first**, while Llama 3.2 provides the natural-language interpretation.

### 📥 Data Export
- Download cleaned dataset
- Download anomaly report

## 🧠 Architecture

```text
CSV / Excel Upload
        ↓
Data Processing — Pandas
        ↓
 ┌──────┼─────────┐
 ↓      ↓         ↓
Dashboard  Anomaly  Forecasting
Analytics  Detection
 └──────┼─────────┘
        ↓
Verified Python Metrics
        ↓
Local Llama 3.2
        ↓
Business Insights
