import pandas as pd


class CustomerAnalytics:

    def __init__(self, df):
        self.df = df

    def total_customers(self):
        return len(self.df)

    def churned_customers(self):
        return len(
            self.df[self.df["Churn"] == "Yes"]
        )

    def active_customers(self):
        return len(
            self.df[self.df["Churn"] == "No"]
        )

    def churn_rate(self):

        return round(
            self.churned_customers()
            / self.total_customers() * 100,
            2
        )

    def retention_rate(self):

        return round(
            self.active_customers()
            / self.total_customers() * 100,
            2
        )

    def gender_distribution(self):

        return (
            self.df["gender"]
            .value_counts()
            .reset_index()
        )

    def senior_citizen_analysis(self):

        return (
            self.df.groupby("SeniorCitizen")
            .size()
            .reset_index(name="Count")
        )

    def contract_analysis(self):

        return (
            self.df.groupby("Contract")
            .size()
            .reset_index(name="Customers")
        )

    def payment_analysis(self):

        return (
            self.df.groupby("PaymentMethod")
            .size()
            .reset_index(name="Customers")
        )

    def customer_segmentation(self):

        bins = [0,12,24,48,72]

        labels = [
            "New",
            "Developing",
            "Established",
            "Loyal"
        ]

        self.df["Segment"] = pd.cut(
            self.df["tenure"],
            bins=bins,
            labels=labels
        )

        return (
            self.df["Segment"]
            .value_counts()
            .reset_index()
        )

    def clv_analysis(self):

        self.df["CLV"] = (
            self.df["MonthlyCharges"]
            * self.df["tenure"]
        )

        return self.df[
            ["MonthlyCharges","tenure","CLV"]
        ]