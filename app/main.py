import streamlit as st
import pandas as pd
import ollama

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Analytics Copilot",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# HEADER
# =========================================================

st.title("🤖 AI Analytics Copilot")
st.subheader("Intelligent Data Assistant")

st.write(
    "Upload your CSV or Excel file and get interactive analytics, "
    "AI-powered insights, anomaly detection and forecasting."
)

# =========================================================
# FILE UPLOADER
# =========================================================

uploaded_file = st.file_uploader(
    "📂 Upload your dataset",
    type=["csv", "xlsx"]
)

# =========================================================
# DATA PROCESSING
# =========================================================

if uploaded_file is not None:

    # Read CSV / Excel
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ Dataset uploaded successfully!")

    # =====================================================
    # SIDEBAR FILTERS
    # =====================================================

    st.sidebar.header("🎛️ Dashboard Filters")

    selected_regions = st.sidebar.multiselect(
        "🌍 Select Region",
        options=sorted(df["Region"].dropna().unique()),
        default=sorted(df["Region"].dropna().unique())
    )

    selected_categories = st.sidebar.multiselect(
        "🛍️ Select Category",
        options=sorted(df["Category"].dropna().unique()),
        default=sorted(df["Category"].dropna().unique())
    )

    selected_customer_types = st.sidebar.multiselect(
        "👤 Customer Type",
        options=sorted(df["Customer_Type"].dropna().unique()),
        default=sorted(df["Customer_Type"].dropna().unique())
    )

    selected_payment_methods = st.sidebar.multiselect(
        "💳 Payment Method",
        options=sorted(df["Payment_Method"].dropna().unique()),
        default=sorted(df["Payment_Method"].dropna().unique())
    )

    # =====================================================
    # APPLY FILTERS
    # =====================================================

    filtered_df = df[
        (df["Region"].isin(selected_regions))
        & (df["Category"].isin(selected_categories))
        & (df["Customer_Type"].isin(selected_customer_types))
        & (df["Payment_Method"].isin(selected_payment_methods))
    ].copy()

    # =====================================================
    # EMPTY DATA CHECK
    # =====================================================

    if filtered_df.empty:
        st.warning("⚠️ No data available for the selected filters.")
        st.stop()

    # =====================================================
    # DATA CLEANING + ANOMALY DETECTION
    # =====================================================

    st.subheader("🧹 Data Cleaning & 🚨 Anomaly Detection")

    # Work on a copy so the uploaded dataset remains unchanged.
    analysis_df = filtered_df.copy()

    # Basic automatic cleaning for common missing values.
    numeric_columns = analysis_df.select_dtypes(include="number").columns.tolist()
    categorical_columns = analysis_df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()

    missing_before = int(analysis_df.isnull().sum().sum())
    duplicate_before = int(analysis_df.duplicated().sum())

    for column in numeric_columns:
        if analysis_df[column].isnull().any():
            analysis_df[column] = analysis_df[column].fillna(
                analysis_df[column].median()
            )

    for column in categorical_columns:
        if analysis_df[column].isnull().any():
            mode_values = analysis_df[column].mode()
            if not mode_values.empty:
                analysis_df[column] = analysis_df[column].fillna(
                    mode_values.iloc[0]
                )

    duplicate_after_cleaning = int(analysis_df.duplicated().sum())
    missing_after = int(analysis_df.isnull().sum().sum())

    clean_col1, clean_col2, clean_col3, clean_col4 = st.columns(4)

    with clean_col1:
        st.metric("Missing Before", f"{missing_before:,}")

    with clean_col2:
        st.metric("Missing After", f"{missing_after:,}")

    with clean_col3:
        st.metric("Duplicates Found", f"{duplicate_before:,}")

    with clean_col4:
        st.metric("Clean Rows", f"{len(analysis_df):,}")

    # -----------------------------------------------------
    # IQR-based anomaly detection
    # -----------------------------------------------------

    def iqr_bounds(series):
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - (1.5 * iqr)
        upper = q3 + (1.5 * iqr)
        return lower, upper

    sales_lower, sales_upper = iqr_bounds(analysis_df["Sales"])
    profit_lower, profit_upper = iqr_bounds(analysis_df["Profit"])

    analysis_df["Sales_Anomaly"] = (
        (analysis_df["Sales"] < sales_lower)
        | (analysis_df["Sales"] > sales_upper)
    )

    analysis_df["Profit_Anomaly"] = (
        (analysis_df["Profit"] < profit_lower)
        | (analysis_df["Profit"] > profit_upper)
    )

    analysis_df["Any_Anomaly"] = (
        analysis_df["Sales_Anomaly"]
        | analysis_df["Profit_Anomaly"]
    )

    sales_anomalies = analysis_df[analysis_df["Sales_Anomaly"]].copy()
    profit_anomalies = analysis_df[analysis_df["Profit_Anomaly"]].copy()
    all_anomalies = analysis_df[analysis_df["Any_Anomaly"]].copy()

    anomaly_col1, anomaly_col2, anomaly_col3 = st.columns(3)

    with anomaly_col1:
        st.metric(
            "🚨 Sales Anomalies",
            f"{len(sales_anomalies):,}"
        )

    with anomaly_col2:
        st.metric(
            "⚠️ Profit Anomalies",
            f"{len(profit_anomalies):,}"
        )

    with anomaly_col3:
        st.metric(
            "🔎 Total Anomaly Rows",
            f"{len(all_anomalies):,}"
        )

    if len(all_anomalies) > 0:

        st.warning(
            "⚠️ Potential unusual sales/profit records detected "
            "using the IQR method."
        )

        anomaly_display_columns = [
            column for column in [
                "Order_ID",
                "Order_Date",
                "Product",
                "Category",
                "Region",
                "Sales",
                "Profit",
                "Sales_Anomaly",
                "Profit_Anomaly"
            ]
            if column in all_anomalies.columns
        ]

        st.dataframe(
            all_anomalies[anomaly_display_columns].head(20),
            use_container_width=True
        )

    else:

        st.success(
            "✅ No sales or profit anomalies detected in the "
            "currently selected data."
        )

    # =====================================================
    # DATASET INFORMATION
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Rows",
            f"{filtered_df.shape[0]:,}"
        )

    with col2:
        st.metric(
            "Total Columns",
            f"{filtered_df.shape[1]:,}"
        )

    # =====================================================
    # BUSINESS KPIs
    # =====================================================

    st.subheader("📈 Business Overview")

    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_orders = filtered_df["Order_ID"].nunique()
    total_quantity = filtered_df["Quantity"].sum()
    total_customers = filtered_df["Customer_ID"].nunique()

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

    with kpi1:
        st.metric(
            "💰 Total Sales",
            f"₹{total_sales:,.0f}"
        )

    with kpi2:
        st.metric(
            "📈 Total Profit",
            f"₹{total_profit:,.0f}"
        )

    with kpi3:
        st.metric(
            "🛒 Total Orders",
            f"{total_orders:,}"
        )

    with kpi4:
        st.metric(
            "📦 Quantity Sold",
            f"{total_quantity:,}"
        )

    with kpi5:
        st.metric(
            "👥 Customers",
            f"{total_customers:,}"
        )

    # =====================================================
    # DATE CONVERSION
    # =====================================================

    filtered_df["Order_Date"] = pd.to_datetime(
        filtered_df["Order_Date"],
        errors="coerce"
    )

    # =====================================================
    # SALES TREND
    # =====================================================

    st.subheader("📈 Sales Trend Over Time")

    sales_trend = (
        filtered_df
        .groupby("Order_Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Order_Date")
    )

    st.line_chart(
        sales_trend,
        x="Order_Date",
        y="Sales"
    )

    # =====================================================
    # CATEGORY-WISE SALES
    # =====================================================

    st.subheader("🛍️ Sales by Category")

    category_sales = (
        filtered_df
        .groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    st.bar_chart(
        category_sales,
        x="Category",
        y="Sales"
    )

    # =====================================================
    # REGION-WISE SALES
    # =====================================================

    st.subheader("🌍 Sales by Region")

    region_sales = (
        filtered_df
        .groupby("Region", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    st.bar_chart(
        region_sales,
        x="Region",
        y="Sales"
    )

    # =====================================================
    # PROFIT BY CATEGORY
    # =====================================================

    st.subheader("💰 Profit by Category")

    category_profit = (
        filtered_df
        .groupby("Category", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )

    st.bar_chart(
        category_profit,
        x="Category",
        y="Profit"
    )

    # =====================================================
    # TOP 10 PRODUCTS
    # =====================================================

    st.subheader("🏆 Top 10 Products by Sales")

    top_products = (
        filtered_df
        .groupby("Product", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(10)
    )

    st.bar_chart(
        top_products,
        x="Product",
        y="Sales"
    )

    # =====================================================
    # MONTHLY SALES & PROFIT
    # =====================================================

    st.subheader("📅 Monthly Sales & Profit")

    monthly_data = filtered_df.copy()

    monthly_data["Month"] = (
        monthly_data["Order_Date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_summary = (
        monthly_data
        .groupby("Month", as_index=False)[["Sales", "Profit"]]
        .sum()
    )

    st.line_chart(
        monthly_summary,
        x="Month",
        y=["Sales", "Profit"]
    )

    # =====================================================
    # SALES FORECASTING
    # =====================================================

    st.subheader("🔮 Sales Forecast")

    forecast_data = (
        analysis_df.copy()
        if "analysis_df" in locals()
        else filtered_df.copy()
    )

    forecast_data["Order_Date"] = pd.to_datetime(
        forecast_data["Order_Date"],
        errors="coerce"
    )

    monthly_sales_forecast = (
        forecast_data
        .dropna(subset=["Order_Date"])
        .set_index("Order_Date")["Sales"]
        .resample("MS")
        .sum()
    )

    if len(monthly_sales_forecast) >= 3:

        # A simple, transparent baseline forecast:
        # average of the latest 3 available months.
        forecast_window = monthly_sales_forecast.tail(3)
        forecast_value = forecast_window.mean()

        last_month = monthly_sales_forecast.index.max()

        # Forecast must always start AFTER the latest historical month.
        future_start = (
            last_month.to_period("M").to_timestamp()
            + pd.offsets.MonthBegin(1)
        )

        future_dates = pd.date_range(
            start=future_start,
            periods=3,
            freq="MS"
        )

        forecast_df = pd.DataFrame({
            "Month": future_dates,
            "Forecast Sales": [forecast_value] * 3
        })

        historical_chart = monthly_sales_forecast.reset_index()
        historical_chart.columns = ["Month", "Sales"]

        historical_chart["Forecast Sales"] = pd.NA

        future_chart = forecast_df.copy()

        future_chart["Sales"] = pd.NA

        forecast_chart = pd.concat(
            [historical_chart, future_chart],
            ignore_index=True
        )

        st.line_chart(
            forecast_chart,
            x="Month",
            y=["Sales", "Forecast Sales"]
        )

        forecast_col1, forecast_col2, forecast_col3 = st.columns(3)

        with forecast_col1:
            st.metric(
                "📅 Forecast Month 1",
                future_dates[0].strftime("%b %Y")
            )

        with forecast_col2:
            st.metric(
                "📅 Forecast Month 2",
                future_dates[1].strftime("%b %Y")
            )

        with forecast_col3:
            st.metric(
                "📅 Forecast Month 3",
                future_dates[2].strftime("%b %Y")
            )

        st.info(
            f"📈 Estimated monthly sales baseline for the next 3 months: "
            f"**₹{forecast_value:,.0f}**."
        )

        st.caption(
            "Forecast method: simple 3-month moving-average baseline. "
            "This is an estimate, not a guaranteed prediction."
        )

    else:

        st.info(
            "ℹ️ At least 3 months of historical sales data are required "
            "to generate a forecast."
        )

    # =====================================================
    # AUTOMATIC BUSINESS INSIGHTS
    # =====================================================

    st.subheader("🧠 Automatic Business Insights")

    top_category = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )

    top_category_sales = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .max()
    )

    top_region = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .idxmax()
    )

    top_region_sales = (
        filtered_df
        .groupby("Region")["Sales"]
        .sum()
        .max()
    )

    top_product = (
        filtered_df
        .groupby("Product")["Sales"]
        .sum()
        .idxmax()
    )

    top_product_sales = (
        filtered_df
        .groupby("Product")["Sales"]
        .sum()
        .max()
    )

    most_profitable_category = (
        filtered_df
        .groupby("Category")["Profit"]
        .sum()
        .idxmax()
    )

    most_profitable_category_profit = (
        filtered_df
        .groupby("Category")["Profit"]
        .sum()
        .max()
    )

    insight1, insight2 = st.columns(2)

    with insight1:

        st.info(
            f"🛍️ **Top Category:** {top_category} "
            f"generated ₹{top_category_sales:,.0f} in sales."
        )

        st.info(
            f"🌍 **Top Region:** {top_region} "
            f"generated ₹{top_region_sales:,.0f} in sales."
        )

    with insight2:

        st.info(
            f"🏆 **Top Product:** {top_product} "
            f"generated ₹{top_product_sales:,.0f} in sales."
        )

        st.success(
            f"💰 **Most Profitable Category:** "
            f"{most_profitable_category} generated "
            f"₹{most_profitable_category_profit:,.0f} profit."
        )

    # =====================================================
    # AI ANALYST - NATURAL LANGUAGE + VERIFIED PYTHON + LOCAL LLAMA
    # =====================================================

    st.subheader("🤖 Ask AI Analyst")

    user_question = st.text_input(
        "Ask a question about your data:",
        placeholder="Example: Which category has the highest sales?"
    )

    if st.button("🚀 Ask AI Analyst"):

        if not user_question.strip():

            st.warning("⚠️ Please enter a question.")

        else:

            question = user_question.lower().strip()

            # =================================================
            # VERIFIED PYTHON CALCULATIONS
            # Python is the source of truth for all numbers.
            # =================================================

            category_sales_verified = (
                filtered_df.groupby("Category")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            region_sales_verified = (
                filtered_df.groupby("Region")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            product_sales_verified = (
                filtered_df.groupby("Product")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            category_profit_verified = (
                filtered_df.groupby("Category")["Profit"]
                .sum()
                .sort_values(ascending=False)
            )

            region_profit_verified = (
                filtered_df.groupby("Region")["Profit"]
                .sum()
                .sort_values(ascending=False)
            )

            product_profit_verified = (
                filtered_df.groupby("Product")["Profit"]
                .sum()
                .sort_values(ascending=False)
            )

            # =================================================
            # NATURAL-LANGUAGE HELPERS
            # =================================================

            def money(value):
                return f"₹{value:,.0f}"

            def find_named_items(text, items):
                return [
                    item for item in items
                    if item.lower() in text
                ]

            # =================================================
            # EXACT / VERIFIED QUESTIONS
            # =================================================

            if (
                ("highest" in question or "top" in question or "best" in question)
                and "sales" in question
                and "category" in question
            ):

                category = category_sales_verified.index[0]
                sales = category_sales_verified.iloc[0]

                st.success("📊 Verified Analysis")

                st.markdown(
                    f"""
### 🛍️ Highest Sales Category

**{category}**

💰 **Sales:** {money(sales)}
"""
                )

                st.info(
                    f"💡 {category} is the highest-revenue category "
                    f"among the currently selected filters."
                )

            elif (
                ("highest" in question or "top" in question or "best" in question)
                and "sales" in question
                and "region" in question
            ):

                region = region_sales_verified.index[0]
                sales = region_sales_verified.iloc[0]

                st.success("📊 Verified Analysis")

                st.markdown(
                    f"""
### 🌍 Highest Sales Region

**{region}**

💰 **Sales:** {money(sales)}
"""
                )

                st.info(
                    f"💡 {region} is the highest-revenue region "
                    f"among the currently selected filters."
                )

            elif (
                ("highest" in question or "top" in question or "best" in question)
                and "sales" in question
                and "product" in question
            ):

                product = product_sales_verified.index[0]
                sales = product_sales_verified.iloc[0]

                st.success("📊 Verified Analysis")

                st.markdown(
                    f"""
### 🏆 Best-Selling Product

**{product}**

💰 **Sales:** {money(sales)}
"""
                )

                st.info(
                    f"💡 {product} is the top-selling product "
                    f"among the currently selected filters."
                )

            elif (
                ("highest" in question or "most profitable" in question or "top" in question)
                and "profit" in question
                and "category" in question
            ):

                category = category_profit_verified.index[0]
                profit = category_profit_verified.iloc[0]

                st.success("📊 Verified Analysis")

                st.markdown(
                    f"""
### 💰 Most Profitable Category

**{category}**

📈 **Profit:** {money(profit)}
"""
                )

                st.info(
                    f"💡 {category} generates the highest total profit "
                    f"among the currently selected filters."
                )

            elif (
                ("lowest" in question or "bottom" in question or "least" in question)
                and "sales" in question
                and "product" in question
            ):

                product = product_sales_verified.index[-1]
                sales = product_sales_verified.iloc[-1]

                st.success("📊 Verified Analysis")

                st.markdown(
                    f"""
### 📉 Lowest Sales Product

**{product}**

💰 **Sales:** {money(sales)}
"""
                )

            elif (
                ("lowest" in question or "bottom" in question or "least" in question)
                and "sales" in question
                and "category" in question
            ):

                category = category_sales_verified.index[-1]
                sales = category_sales_verified.iloc[-1]

                st.success("📊 Verified Analysis")

                st.markdown(
                    f"""
### 📉 Lowest Sales Category

**{category}**

💰 **Sales:** {money(sales)}
"""
                )

            elif (
                ("lowest" in question or "bottom" in question or "least" in question)
                and "sales" in question
                and "region" in question
            ):

                region = region_sales_verified.index[-1]
                sales = region_sales_verified.iloc[-1]

                st.success("📊 Verified Analysis")

                st.markdown(
                    f"""
### 📉 Lowest Sales Region

**{region}**

💰 **Sales:** {money(sales)}
"""
                )

            elif (
                "total sales" in question
                or question in {"sales", "what are the total sales", "what is total sales"}
            ):

                st.success("📊 Verified Analysis")

                st.markdown(
                    f"""
### 💰 Total Sales

**{money(total_sales)}**
"""
                )

            elif (
                "total profit" in question
                or question in {"profit", "what is the total profit", "what are the total profit"}
            ):

                st.success("📊 Verified Analysis")

                st.markdown(
                    f"""
### 📈 Total Profit

**{money(total_profit)}**
"""
                )

            elif "total orders" in question or "number of orders" in question:

                st.success("📊 Verified Analysis")

                st.markdown(
                    f"""
### 🛒 Total Orders

**{total_orders:,}**
"""
                )

            elif (
                "total customers" in question
                or "number of customers" in question
            ):

                st.success("📊 Verified Analysis")

                st.markdown(
                    f"""
### 👥 Total Customers

**{total_customers:,}**
"""
                )

            elif "quantity sold" in question or "total quantity" in question:

                st.success("📊 Verified Analysis")

                st.markdown(
                    f"""
### 📦 Quantity Sold

**{total_quantity:,}**
"""
                )

            # =================================================
            # TOP N / BOTTOM N
            # =================================================

            elif (
                ("top" in question or "best" in question)
                and "product" in question
            ):

                n = 3
                for candidate in [10, 5, 3]:
                    if str(candidate) in question:
                        n = candidate
                        break

                results = product_sales_verified.head(n)

                st.success("📊 Verified Analysis")

                st.markdown(f"### 🏆 Top {n} Products by Sales")

                for rank, (product, sales) in enumerate(results.items(), start=1):
                    st.write(f"**{rank}. {product}** — {money(sales)}")

            elif (
                ("bottom" in question or "lowest" in question or "least" in question)
                and "product" in question
                and ("top" not in question)
            ):

                n = 3
                for candidate in [10, 5, 3]:
                    if str(candidate) in question:
                        n = candidate
                        break

                results = product_sales_verified.tail(n).sort_values()

                st.success("📊 Verified Analysis")

                st.markdown(f"### 📉 Bottom {n} Products by Sales")

                for rank, (product, sales) in enumerate(results.items(), start=1):
                    st.write(f"**{rank}. {product}** — {money(sales)}")

            # =================================================
            # COMPARE TWO CATEGORIES / REGIONS / PRODUCTS
            # =================================================

            elif "compare" in question and "sales" in question:

                if "category" in question or any(
                    item.lower() in question
                    for item in category_sales_verified.index
                ):

                    items = find_named_items(
                        question,
                        category_sales_verified.index
                    )
                    data_series = category_sales_verified
                    item_type = "categories"

                elif "region" in question or any(
                    item.lower() in question
                    for item in region_sales_verified.index
                ):

                    items = find_named_items(
                        question,
                        region_sales_verified.index
                    )
                    data_series = region_sales_verified
                    item_type = "regions"

                else:

                    items = find_named_items(
                        question,
                        product_sales_verified.index
                    )
                    data_series = product_sales_verified
                    item_type = "products"

                if len(items) >= 2:

                    item_1 = items[0]
                    item_2 = items[1]

                    sales_1 = data_series.loc[item_1]
                    sales_2 = data_series.loc[item_2]

                    difference = abs(sales_1 - sales_2)

                    better_item = item_1 if sales_1 >= sales_2 else item_2

                    st.success("📊 Verified Comparison")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric(item_1, money(sales_1))

                    with col2:
                        st.metric(item_2, money(sales_2))

                    with col3:
                        st.metric("Difference", money(difference))

                    st.info(
                        f"💡 **{better_item}** has higher sales "
                        f"among the selected {item_type}."
                    )

                else:

                    st.warning(
                        "⚠️ Please mention two matching categories, regions, "
                        "or products to compare."
                    )

            # =================================================
            # GENERAL AI QUESTIONS
            # =================================================

            else:

                with st.spinner(
                    "🤖 AI Analyst is preparing your business insight..."
                ):

                    try:

                        verified_context = f"""
You are an AI Business Analyst.

Python has already performed all numerical calculations.
The values below are VERIFIED and are the source of truth.

IMPORTANT RULES:
1. Do NOT calculate, modify, divide, multiply, estimate, or invent numbers.
2. If you mention a number, copy it EXACTLY from the verified data.
3. Display money as whole Indian rupees with ₹ and commas.
4. Do NOT add decimal places.
5. Do not create unsupported percentages, averages, growth rates, ratios, or forecasts.
6. If the user's question requires a calculation not already present, clearly say that the requested metric is not directly available rather than guessing.
7. You may explain trends, observations, and business implications using only the verified data.
8. For recommendations, connect them to the available verified categories, regions, products, sales, and profit.
9. Keep the answer concise and professional.
10. Use bullet points for multiple recommendations.

==================================================
VERIFIED BUSINESS DATA
==================================================

Total Sales:
₹{total_sales:,.0f}

Total Profit:
₹{total_profit:,.0f}

Total Orders:
{total_orders:,}

Quantity Sold:
{total_quantity:,}

Total Customers:
{total_customers:,}

==================================================
SALES BY CATEGORY
==================================================

{category_sales_verified.to_dict()}

==================================================
SALES BY REGION
==================================================

{region_sales_verified.to_dict()}

==================================================
SALES BY PRODUCT
==================================================

{product_sales_verified.to_dict()}

==================================================
PROFIT BY CATEGORY
==================================================

{category_profit_verified.to_dict()}

==================================================
PROFIT BY REGION
==================================================

{region_profit_verified.to_dict()}

==================================================
PROFIT BY PRODUCT
==================================================

{product_profit_verified.to_dict()}

==================================================
SALES FORECAST
==================================================

Forecast method:
Simple 3-month moving-average baseline.

Forecast available:
{{"Yes" if len(monthly_sales_forecast) >= 3 else "No"}}

Next 3 forecast months:
{{forecast_df[["Month", "Forecast Sales"]].to_dict(orient="records") if len(monthly_sales_forecast) >= 3 else "Not available"}}

Important:
Forecast values are estimates generated by Python.
Do not present them as guaranteed results.

==================================================

==================================================
ANOMALY DETECTION
==================================================

Method:
IQR (Interquartile Range)

Sales anomaly rows:
{{len(sales_anomalies):,}}

Profit anomaly rows:
{{len(profit_anomalies):,}}

Total anomaly rows:
{{len(all_anomalies):,}}

Missing values before cleaning:
{{missing_before:,}}

Missing values after cleaning:
{{missing_after:,}}

Duplicate rows found:
{{duplicate_before:,}}

Important:
Anomaly counts are verified by Python.
Do not invent anomaly counts or calculate new anomaly metrics.

==================================================
==================================================
USER QUESTION
==================================================

{user_question}

==================================================
RESPONSE RULES
==================================================

Answer the user's question directly.
Use only the verified information above.
Never invent or recalculate numerical values.
Do not output unnecessary decimal places.
If the data is insufficient, say so clearly.
For anomaly-related questions, use only the verified anomaly counts and cleaning information supplied above.
Do not invent an anomaly reason for an individual row unless the supplied data supports it.
"""

                        response = ollama.chat(
                            model="llama3.2",
                            messages=[
                                {
                                    "role": "user",
                                    "content": verified_context
                                }
                            ]
                        )

                        answer = response["message"]["content"]

                        st.success("🤖 AI Business Interpretation")

                        st.markdown(answer)

                    except Exception as e:

                        st.error(
                            "❌ AI Analyst could not connect to Ollama."
                        )

                        st.code(str(e))

    # =====================================================
    # DOWNLOAD ANALYSIS DATA
    # =====================================================

    st.subheader("📥 Export Data")

    export_col1, export_col2 = st.columns(2)

    clean_export_columns = [
        column for column in analysis_df.columns
        if column not in ["Sales_Anomaly", "Profit_Anomaly", "Any_Anomaly"]
    ]

    cleaned_csv = analysis_df[clean_export_columns].to_csv(index=False).encode("utf-8")

    anomaly_csv = all_anomalies.to_csv(index=False).encode("utf-8")

    with export_col1:
        st.download_button(
            "📥 Download Cleaned Data",
            data=cleaned_csv,
            file_name="cleaned_sales_data.csv",
            mime="text/csv",
            use_container_width=True
        )

    with export_col2:
        st.download_button(
            "🚨 Download Anomaly Report",
            data=anomaly_csv,
            file_name="sales_anomaly_report.csv",
            mime="text/csv",
            use_container_width=True
        )

    # =====================================================
    # DATASET PREVIEW
    # =====================================================

    st.subheader("📊 Dataset Preview")

    st.dataframe(
        filtered_df.head(10),
        use_container_width=True
    )

    # =====================================================
    # DATA QUALITY
    # =====================================================

    st.subheader("🔍 Data Quality")

    quality_col1, quality_col2, quality_col3, quality_col4 = st.columns(4)

    with quality_col1:
        st.metric(
            "Original Rows",
            f"{len(filtered_df):,}"
        )

    with quality_col2:
        st.metric(
            "Missing Values",
            f"{missing_before:,}"
        )

    with quality_col3:
        st.metric(
            "Duplicate Rows",
            f"{duplicate_before:,}"
        )

    with quality_col4:
        st.metric(
            "Clean Rows",
            f"{len(analysis_df):,}"
        )

    st.caption(
        "Data Quality shows the original filtered dataset. "
        "Cleaning metrics above show the result after automatic missing-value handling."
    )

    quality_summary = pd.DataFrame({
        "Metric": [
            "Original Rows",
            "Missing Values Before Cleaning",
            "Missing Values After Cleaning",
            "Duplicate Rows Found",
            "Clean Rows"
        ],
        "Value": [
            len(filtered_df),
            missing_before,
            missing_after,
            duplicate_before,
            len(analysis_df)
        ]
    })

    st.dataframe(
        quality_summary,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # COLUMN INFORMATION
    # =====================================================

    st.subheader("📋 Column Information")

    column_info = pd.DataFrame({
        "Column": filtered_df.columns,
        "Data Type": filtered_df.dtypes.astype(str).values,
        "Missing Values": filtered_df.isnull().sum().values
    })

    st.dataframe(
        column_info,
        use_container_width=True
    )

else:

    st.info(
        "👆 Please upload a CSV or Excel dataset to start analysis."
    )
