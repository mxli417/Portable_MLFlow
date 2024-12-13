import mlflow.sklearn
from mlflow.models import infer_signature
from sklearn.datasets import load_diabetes
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

import mlflow

# setup for the local mlflow server
mlflow.set_tracking_uri("http://localhost:5001")

if __name__ == "__main__":
    # model run with logging and model artifacts
    with mlflow.start_run():
        db = load_diabetes()
        X_train, X_test, y_train, y_test = train_test_split(db.data, db.target)

        # Create and train models.
        rf = RandomForestRegressor(n_estimators=100, max_depth=6, max_features=3)
        rf.fit(X_train, y_train)
        score = rf.score(X_train, y_train)
        print(f"Score: {score}")
        mlflow.log_metric("train_score", score)

        # Use the model to make predictions on the test dataset.
        predictions = rf.predict(X_test)
        score = rf.score(X_test, y_test)
        print(f"Score: {score}")
        mlflow.log_metric("test_score", score)

        signature = infer_signature(X_test, predictions)
        mlflow.sklearn.log_model(
            sk_model=rf,
            artifact_path="rf-model",
            signature=signature,
            registered_model_name="sk-learn-random-forest-reg-model",
        )
        print(f"Model saved in run {mlflow.active_run().info.run_uuid}")
