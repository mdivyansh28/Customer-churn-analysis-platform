import pandas as pd


class RevenueAnalytics:

    def __init__(self, df):

        self.df = df.copy()

        # Convert numeric columns safely
        self.df["TotalCharges"] = pd.to_numeric(
            self.df["TotalCharges"],
            errors="coerce"
        )

        self.df["MonthlyCharges"] = pd.to_numeric(
            self.df["MonthlyCharges"],
            errors="coerce"
        )

        self.df.fillna(0, inplace=True)

    def total_revenue(self):

        return round(
            self.df["TotalCharges"].sum(),
            2
        )

    def monthly_revenue(self):

        return round(
            self.df["MonthlyCharges"].sum(),
            2
        )

    def arpu(self):

        return round(
            self.df["MonthlyCharges"].mean(),
            2
        )

    def revenue_loss(self):

        churned = self.df[
            self.df["Churn"] == "Yes"
        ]

        return round(
            churned["MonthlyCharges"].sum(),
            2
        )

    def customer_lifetime_value(self):

        self.df["CLV"] = (
            self.df["MonthlyCharges"]
            * self.df["tenure"]
        )

        return round(
            self.df["CLV"].mean(),
            2
        )

    def revenue_by_contract(self):

        return (
            self.df.groupby("Contract")["MonthlyCharges"]
            .sum()
            .reset_index()
        )

    def revenue_forecast(self):

        monthly = self.monthly_revenue()

        forecast = []

        for month in range(1, 13):

            forecast.append({
                "Month": month,
                "ForecastRevenue": monthly
            })

        return pd.DataFrame(forecast)