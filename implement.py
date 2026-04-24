import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input

X = np.array([
    [1.5, 45],
    [2.0, 60],
    [2.5, 65],
    [3.0, 70],
    [3.5, 80],
    [4.0, 85],
    [4.5, 90],
    [5.0, 95]
], dtype=float)


y = np.array([0, 0, 0, 1, 1, 1, 1, 1], dtype=float)


X = X / np.max(X)


model = Sequential([
    Input(shape=(2,)),                
    Dense(6, activation='relu'),      
    Dense(1, activation='sigmoid')   
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])


model.fit(X, y, epochs=500, verbose=0)  


loss, acc = model.evaluate(X, y, verbose=0)
print(f"\nTraining Accuracy: {acc:.3f}")


predictions = model.predict(X)
print("\nPredictions:")
for i in range(len(X)):
    predicted_label = int(round(predictions[i][0]))
    actual_label = int(y[i])
    print(f"Input: {X[i]*np.max(X)} → Predicted: {'Pass' if predicted_label==1 else 'Fail'} → Actual: {'Pass' if actual_label==1 else 'Fail'}")
