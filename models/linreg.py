from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score

def linear_regression_model_tuned(data):
    # Separate features and target
    X = data.drop('quality', axis=1)
    y = data['quality']

    # Split the data into training, validation, and testing sets
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42) # 60% for training
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42) # Split the 40% equally for validation and test

    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)

    # Define the range of alpha values to explore
    alpha_values = [13.0, 14.0, 15.0, 16.0]
    best_alpha = None
    best_score = float('-inf')

    # Manually search for the best alpha value
    for alpha in alpha_values:
        model = Ridge(alpha=alpha)
        model.fit(X_train_scaled, y_train)
        val_score = model.score(X_val_scaled, y_val)
        if val_score > best_score:
            best_alpha = alpha
            best_score = val_score

    # Train the model with the best alpha value on the combined training and validation set
    X_train_val_scaled = scaler.fit_transform(X_train.append(X_val))
    y_train_val = y_train.append(y_val)
    best_model = Ridge(alpha=best_alpha)
    best_model.fit(X_train_val_scaled, y_train_val)

    # Evaluate the best model on the test set
    test_score = best_model.score(scaler.transform(X_test), y_test)

    # Print the best alpha value and test score
    print(f'Best alpha parameter: {best_alpha}')
    print(f'Best Model Test Score (R^2): {test_score:.4f}')

    return best_model
