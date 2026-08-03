"""

Generates the synthetic diabetes dataset.
 
Health parameters used:
    age                  (years)
    weight               (kg)
    height               (cm)
    bmi                  (calculated from weight and height)
    blood_pressure       (mm Hg)
    glucose              (mg/dL)
    family_history       (1 = has a close relative with diabetes, 0 = no)
    physical_activity    (hours of exercise per week)
"""
 
import numpy as np
import pandas as pd
 
 
def generate_synthetic_diabetes_dataset(num_rows=2000, save_path='synthetic_diabetes_dataset.csv'):
    random_generator = np.random.default_rng(42)
 
    age = random_generator.integers(18, 80, num_rows)
    height = random_generator.normal(168, 10, num_rows).clip(140, 200)
    weight = random_generator.normal(75, 18, num_rows).clip(40, 160)
    bmi = weight / ((height / 100) ** 2)
 
    blood_pressure = random_generator.normal(70, 12, num_rows).clip(30, 130)
    glucose = random_generator.normal(120, 30, num_rows).clip(50, 250)
    family_history = random_generator.binomial(1, 0.3, num_rows)
    physical_activity = random_generator.gamma(2, 1.5, num_rows).clip(0, 15)
 
    risk_score = (
        0.015 * glucose
        + 0.04 * bmi
        + 0.015 * age
        + 0.7 * family_history
        - 0.08 * physical_activity
        - 5.0
    )
    diabetes_probability = 1 / (1 + np.exp(-risk_score))
    has_diabetes = random_generator.binomial(1, diabetes_probability)
 
    dataset = pd.DataFrame({
        'Age': age,
        'Weight': weight.round(1),
        'Height': height.round(1),
        'BMI': bmi.round(1),
        'BloodPressure': blood_pressure.round(1),
        'Glucose': glucose.round(1),
        'FamilyHistory': family_history,
        'PhysicalActivity': physical_activity.round(1),
        'Outcome': has_diabetes
    })
 
    if save_path:
        dataset.to_csv(save_path, index=False)
 
    return dataset
 
 
if __name__ == "__main__":
    dataset = generate_synthetic_diabetes_dataset()
    print(f"Generated {len(dataset)} rows.")
    print(f"Diabetic: {dataset['Outcome'].sum()}, Non-diabetic: {(dataset['Outcome']==0).sum()}")