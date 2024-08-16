import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import pickle

class DecisionTreeRegressorModel:
    def __init__(self, csv_path, target_feature):
        self.csv_path = csv_path
        self.target_feature = target_feature
        self.model = None
        self.scaler = None

    def load_and_preprocess_data(self):
        # Load data from CSV
        data = pd.read_csv(self.csv_path)
        
        # Drop columns that are purely numerical (like 1, 2, 3, ...)
        data = data.loc[:, ~data.columns.str.match(r'^\d+$')]
        
        # Split data into features and target
        X = data.drop(columns=[self.target_feature])
        y = data[self.target_feature]
        
        # Normalize the features
        self.scaler = StandardScaler()
        X_normalized = self.scaler.fit_transform(X)
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X_normalized, y, test_size=0.2, random_state=42)
        
        return X_train, X_test, y_train, y_test

    def train(self):
        # Load and preprocess data
        X_train, X_test, y_train, y_test = self.load_and_preprocess_data()
        
        # Initialize and train the Decision Tree Regressor
        self.model = DecisionTreeRegressor(random_state=42)
        self.model.fit(X_train, y_train)
        
        # Predict and evaluate the model
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f'Mean Squared Error: {mse}')
        
        # Save the trained model
        self.save_model()
        
        # Generate a usage file
        self.generate_usage_instructions()

    def save_model(self):
        model_filename = 'decision_tree_model.pkl'
        scaler_filename = 'scaler.pkl'
        
        # Save the model and scaler to disk
        with open(model_filename, 'wb') as model_file:
            pickle.dump(self.model, model_file)
        
        with open(scaler_filename, 'wb') as scaler_file:
            pickle.dump(self.scaler, scaler_file)
        
        print(f'Model saved as {model_filename}')
        print(f'Scaler saved as {scaler_filename}')
    
    def generate_usage_instructions(self):
        instructions = (
            "To use the saved model:\n"
            "1. Load the model and scaler using pickle:\n"
            "   with open('decision_tree_model.pkl', 'rb') as model_file:\n"
            "       model = pickle.load(model_file)\n\n"
            "   with open('scaler.pkl', 'rb') as scaler_file:\n"
            "       scaler = pickle.load(scaler_file)\n\n"
            "2. Prepare your data (make sure it has the same features as the training data):\n"
            "   X_new = ...  # Your new data\n\n"
            "3. Normalize the new data using the loaded scaler:\n"
            "   X_new_normalized = scaler.transform(X_new)\n\n"
            "4. Predict using the loaded model:\n"
            "   predictions = model.predict(X_new_normalized)\n"
        )
        
        with open('model_usage_instructions.txt', 'w') as file:
            file.write(instructions)
        
        print('Instructions for using the saved model have been written to model_usage_instructions.txt')

    def predict(self, X_new):
        # Normalize the new data using the same scaler
        X_new_normalized = self.scaler.transform(X_new)
        
        # Predict using the trained model
        predictions = self.model.predict(X_new_normalized)
        return predictions
