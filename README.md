Car Price Prediction using Machine Learning (Modular Project)
Project Overview:-
The Car Price Prediction System is a modular machine learning project designed to predict the selling price of used cars based on various features such as car name, year, kilometers driven, fuel type, seller type, transmission, and ownership history.
This project follows an industry-grade modular structure that separates each component (like data ingestion, transformation, training, and prediction) for better scalability, maintainability, and deployment readiness.

<img width="883" height="332" alt="Screenshot 2025-10-27 203507" src="https://github.com/user-attachments/assets/443aae62-ed98-4060-ab5e-1f912c51e391" />
<img width="802" height="372" alt="Screenshot 2025-10-27 203533" src="https://github.com/user-attachments/assets/74d547d1-014d-4fe9-bdb7-e980bf94533f" />
<img width="854" height="433" alt="Screenshot 2025-10-27 203552" src="https://github.com/user-attachments/assets/c821a585-ce06-487c-9318-cfe062fe4fe2" />



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
name	             year	        km_driven        	fuel          transmission     	    owner
Maruti Swift	     2019	          45000	         Petrol		         Manual        	   First Owner

Predicted Price: ₹5.6 Lakhs

The below things we can do in this project for the Future Improvements:-

1) We can also integrate MLOps tools like MLflow or DVC for version controling

2) We can extend deployment to AWS S3 + Lambda + API Gateways 

3) We can  build  a React frontend for better UI



