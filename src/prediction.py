import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from xgboost import XGBClassifier


class ChurnPrediction:

    def __init__(self, filepath):

        self.filepath = filepath
        self.df = None
        self.best_model = None
        self.best_score = 0

    def load_data(self):

        self.df = pd.read_csv(self.filepath)

        self.df["TotalCharges"] = pd.to_numeric(
            self.df["TotalCharges"],
            errors="coerce"
        )

        self.df.fillna(0, inplace=True)

        return self.df

    def preprocess(self):

        df = self.df.copy()

        if "customerID" in df.columns:
            df.drop("customerID", axis=1, inplace=True)

        encoders = {}

        for col in df.select_dtypes(include="object").columns:

            encoder = LabelEncoder()

            df[col] = encoder.fit_transform(df[col])

            encoders[col] = encoder

        os.makedirs("models", exist_ok=True)

        joblib.dump(
            encoders,
            "models/label_encoders.pkl"
        )

        X = df.drop("Churn", axis=1)

        y = df["Churn"]

        return train_test_split(
            X,
            y,
            test_size=0.20,
            stratify=y,
            random_state=42
        )

    def evaluate_model(self, model, X_test, y_test):

        predictions = model.predict(X_test)

        probabilities = model.predict_proba(X_test)[:,1]

        metrics = {

            "Accuracy":
            round(
                accuracy_score(
                    y_test,
                    predictions
                ) * 100,
                2
            ),

            "Precision":
            round(
                precision_score(
                    y_test,
                    predictions
                ) * 100,
                2
            ),

            "Recall":
            round(
                recall_score(
                    y_test,
                    predictions
                ) * 100,
                2
            ),

            "F1 Score":
            round(
                f1_score(
                    y_test,
                    predictions
                ) * 100,
                2
            ),

            "ROC AUC":
            round(
                roc_auc_score(
                    y_test,
                    probabilities
                ) * 100,
                2
            )
        }

        return metrics

    def train_models(self):

        self.load_data()

        X_train, X_test, y_train, y_test = self.preprocess()

        models = {

            "Logistic Regression":
            LogisticRegression(max_iter=3000),

            "Decision Tree":
            DecisionTreeClassifier(max_depth=8),

            "Random Forest":
            RandomForestClassifier(
                n_estimators=200,
                random_state=42
            ),

            "XGBoost":
            XGBClassifier(
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
        }

        results = {}

        for name, model in models.items():

            model.fit(
                X_train,
                y_train
            )

            metrics = self.evaluate_model(
                model,
                X_test,
                y_test
            )

            results[name] = metrics

            if metrics["ROC AUC"] > self.best_score:

                self.best_score = metrics["ROC AUC"]

                self.best_model = model

        joblib.dump(
            self.best_model,
            "models/churn_model.pkl"
        )

        return results

    def feature_importance(self):

        if hasattr(
            self.best_model,
            "feature_importances_"
        ):

            return pd.DataFrame({

                "Feature":
                self.best_model.feature_names_in_,

                "Importance":
                self.best_model.feature_importances_
            }).sort_values(
                by="Importance",
                ascending=False
            )

        return None

    def predict_customer(self, customer_data):

        model = joblib.load(
            "models/churn_model.pkl"
        )

        probability = model.predict_proba(
            customer_data
        )[0][1]

        prediction = (
            "Likely Churn"
            if probability > 0.5
            else "Retained"
        )

        return prediction, probability