import pandas as pd


class ChurnAnalytics:

    def __init__(self, df):
        self.df = df

    def churn_by_gender(self):

        return pd.crosstab(
            self.df["gender"],
            self.df["Churn"]
        )

    def churn_by_contract(self):

        return pd.crosstab(
            self.df["Contract"],
            self.df["Churn"]
        )

    def churn_by_payment(self):

        return pd.crosstab(
            self.df["PaymentMethod"],
            self.df["Churn"]
        )

    def churn_by_internet(self):

        return pd.crosstab(
            self.df["InternetService"],
            self.df["Churn"]
        )

    def churn_by_tenure(self):

        return (
            self.df.groupby("tenure")["Churn"]
            .count()
            .reset_index()
        )

    def correlation_matrix(self):

        numeric = self.df.select_dtypes(
            include=["int64","float64"]
        )

        return numeric.corr()

    def churn_summary(self):

        churned = self.df[
            self.df["Churn"] == "Yes"
        ]

        active = self.df[
            self.df["Churn"] == "No"
        ]

        return {
            "churned": len(churned),
            "active": len(active)
        }