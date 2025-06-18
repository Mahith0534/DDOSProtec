import pandas as pd
import joblib
import subprocess

# Load the trained model
model = joblib.load("model.joblib")

# Read the CSV
df = pd.read_csv("zeek_features.csv")

# Extract Src IPs separately
src_ips = df['Src IP']

# Drop non-feature columns
features_df = df.drop(columns=['Src IP'])

# Predict using the model
predictions = model.predict(features_df)

# Open file to write predictions
with open("ip_predictions.txt", "w") as f:
    for ip, label in zip(src_ips, predictions):
        f.write(f"{ip} {label}\n")
        if label.lower() == 'ddos':
            print(f"Blocking IP: {ip}")
            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
