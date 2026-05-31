class RecommendationEngine:

    def __init__(self):
        pass

    def get_risk_bucket(self, probability):

        if probability >= 0.80:
            return "Critical Risk"

        elif probability >= 0.60:
            return "High Risk"

        elif probability >= 0.40:
            return "Medium Risk"

        return "Low Risk"

    def generate(self, probability):

        risk = self.get_risk_bucket(
            probability
        )

        recommendations = []

        if risk == "Critical Risk":

            recommendations.extend([
                "25% Discount Offer",
                "Premium Customer Support",
                "Dedicated Relationship Manager",
                "Free Upgrade Plan",
                "Loyalty Rewards Program"
            ])

        elif risk == "High Risk":

            recommendations.extend([
                "15% Discount",
                "Personalized Email Campaign",
                "Special Retention Package",
                "Priority Support"
            ])

        elif risk == "Medium Risk":

            recommendations.extend([
                "Engagement Campaign",
                "Value Added Services",
                "Customer Feedback Call"
            ])

        else:

            recommendations.extend([
                "Maintain Current Relationship",
                "Cross Sell Services"
            ])

        return {

            "Risk Category": risk,
            "Recommendations": recommendations
        }