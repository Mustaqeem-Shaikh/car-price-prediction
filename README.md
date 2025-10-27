Car Price Prediction using Machine Learning (Modular Project)
Project Overview:-
The Car Price Prediction System is a modular machine learning project designed to predict the selling price of used cars based on various features such as car name, year, kilometers driven, fuel type, seller type, transmission, and ownership history.
This project follows an industry-grade modular structure that separates each component (like data ingestion, transformation, training, and prediction) for better scalability, maintainability, and deployment readiness.


Project Architecture:- 
Car Price Prediction/
│
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD pipeline
│
├── .env                        # Environment variables (GitHub Secrets used for deployment)
├── Dockerfile                  # Docker container for deployment
├── README.md                   # Project documentation
│
├── config/
│   └── config.yaml             # Global configuration file for project paths and parameters
│
├── src/
│   └── Car/
│       ├── components/         # All modular ML components
│       │   ├── data_ingestion.py
│       │   ├── data_transformation.py
│       │   ├── model_trainer.py
│       │   └── model_evaluation.py
│       │
│       ├── entity/             # Entity classes for data structures (artifacts, configs)
│       │   ├── config_entity.py
│       │   └── artifact_entity.py
│       │
│       ├── pipeline/           # Orchestrates all steps end-to-end
│       │   ├── training_pipeline.py
│       │   └── prediction_pipeline.py
│       │
│       ├── utils/              # Helper functions (YAML I/O, logging, model saving, etc.)
│       │   └── utils.py
│       │
│       ├── exception.py        # Custom exception handling
│       ├── logger.py           # Centralized logging system
│       └── __init__.py
│
├── notebooks/
│   └── EDA.ipynb               # Exploratory Data Analysis notebook
│
├── artifacts/                  # Automatically generated artifacts (datasets, models, reports)
│
├── app.py                      # Flask web application for prediction
├── requirements.txt            # Python dependencies
└── setup.py                    # Project setup file for packaging

Features & Workflow

Data Ingestion:-
Reads the dataset from a CSV file or external source.
Splits the data into training and testing sets.
Stores raw and processed data in the artifacts/ folder.

Data Transformation:-
Handles missing values, feature encoding, and scaling.
Uses LabelEncoder and OneHotEncoder for categorical features.
Saves the transformation pipeline as a .pkl file.

Model Training:-
Trains multiple regression models such as:
Linear Regression
Random Forest
Gradient Boosting
Uses GridSearchCV for hyperparameter tuning.
Saves the best-performing model to artifacts/model.pkl.

Model Evaluation:-
Evaluates model performance on the test set.
Generates metrics such as R² score, MAE, and RMSE.

Prediction Pipeline:-
Takes user input through a Flask web app.
Loads the trained model and preprocessing pipeline.
Returns the predicted car price instantly.

Cloudd Deployment:-
The project is fully Dockerized and supports CI/CD with GitHub Actions and AWS ECR + EC2 deployment.

Technologies Used:
Machine Learning: Scikit-learn, Pandas, NumPy
Backend: Flask
Version Control: GitHub
CI/CD: GitHub Actions
Containerization: Docker
Cloud Deployment: AWS ECR + EC2

Modular Approach Benefits:-
1) Clean and reusable codebase

2) Easier debugging and logging

3) Clear separation of configuration, entities, and components

4) Scalable and ready for production deployment

Example Input
name	year	km_driven	fuel transmission	owner
Maruti Swift	2019	45000	Petrol	Dealer	Manual	First Owner

Predicted Price: ₹5.6 Lakhs

The below things we can do in this project for the Future Improvements are mentioned below:-

1) We can also integrate MLOps tools like MLflow or DVC for version controling

2) We can extend deployment to AWS S3 + Lambda + API Gateways 

3) We can  build  a React frontend for better UI
