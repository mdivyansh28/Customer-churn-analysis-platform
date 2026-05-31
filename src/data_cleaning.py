import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib
import os


class DataCleaner:

    def __init__(self, filepath):
        self.filepath = filepath
        self.df = None
        self.encoders = {}

    def load_data(self):
        self.df = pd.read_csv(self.filepath)
        return self.df

    def clean_data(self):

        self.df.columns = self.df.columns.str.strip()

        if "TotalCharges" in self.df.columns:
            self.df["TotalCharges"] = pd.to_numeric(
                self.df["TotalCharges"],
                errors="coerce"
            )

        self.df.fillna(0, inplace=True)

        if "customerID" in self.df.columns:
            self.df.drop("customerID", axis=1, inplace=True)

        return self.df

    def encode_features(self):

        categorical_cols = self.df.select_dtypes(
            include=["object"]
        ).columns

        for col in categorical_cols:

            encoder = LabelEncoder()

            self.df[col] = encoder.fit_transform(
                self.df[col]
            )

            self.encoders[col] = encoder

        return self.df

    def save_encoders(self):

        os.makedirs("models", exist_ok=True)

        joblib.dump(
            self.encoders,
            "models/label_encoders.pkl"
        )

    def process(self):

        self.load_data()
        self.clean_data()
        self.encode_features()
        self.save_encoders()

        self.df.to_csv(
            "data/processed_churn.csv",
            index=False
        )

        return self.df


if __name__ == "__main__":

    cleaner = DataCleaner(
        "data/Customer Churn.csv"
    )

    df = cleaner.process()

    print(df.head())