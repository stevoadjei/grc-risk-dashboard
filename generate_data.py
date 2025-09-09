import pandas as pd
import numpy as np
import random


# Number of vendors to generate
NUM_VENDORS = 100

# Lists of possible values for our data columns
vendor_names = [f"Vendor_{i:03d}" for i in range(1, NUM_VENDORS + 1)]
service_types = ['Cloud Services', 'SaaS Platform', 'Data Processor', 'AI Model Provider', 'Managed IT', 'Consulting']
countries = ['USA', 'UK', 'Germany', 'India', 'Canada', 'Ghana', 'Singapore']
compliance_status = ['Compliant', 'Partially Compliant', 'Non-Compliant']
nist_adoption = ['High', 'Medium', 'Low']

# Generate the base data
data = {
    'VendorID': range(1, NUM_VENDORS + 1),
    'VendorName': vendor_names,
    'ServiceType': [random.choice(service_types) for _ in range(NUM_VENDORS)],
    'Country': [random.choice(countries) for _ in range(NUM_VENDORS)],
    'RiskImpact': np.random.randint(1, 6, size=NUM_VENDORS), # Scale of 1-5
    'RiskLikelihood': np.random.randint(1, 6, size=NUM_VENDORS), # Scale of 1-5
    'OpenVulnerabilities': np.random.randint(0, 50, size=NUM_VENDORS),
    'IncidentHistory': np.random.randint(0, 5, size=NUM_VENDORS),
    'ISO27001_Compliance': [random.choice(compliance_status) for _ in range(NUM_VENDORS)],
    'NIST_CSF_Adoption': [random.choice(nist_adoption) for _ in range(NUM_VENDORS)],
}

# Create a DataFrame
df = pd.DataFrame(data)

# --- Feature Engineering & Calculation ---

# 1. Calculate Overall Risk Score
# A simple but effective formula: Impact * Likelihood
df['OverallRiskScore'] = df['RiskImpact'] * df['RiskLikelihood']

# 2. Add the "AI Vendor" flag based on ServiceType
df['Is_AI_Vendor'] = df['ServiceType'].apply(lambda x: True if x == 'AI Model Provider' else False)

# 3. Add OWASP for LLM checks for AI vendors
# For non-AI vendors, this will be N/A. For AI vendors, give them a random status.
owasp_llm_risks = ['Prompt Injection', 'Data Leakage', 'Insecure Output', 'Model Theft']
owasp_status = ['Vulnerable', 'Mitigated']
def assign_owasp_llm_risk(is_ai):
    if is_ai:
        return f"{random.choice(owasp_llm_risks)}: {random.choice(owasp_status)}"
    return "N/A"

df['OWASP_LLM_Check'] = df['Is_AI_Vendor'].apply(assign_owasp_llm_risk)


# 4. Calculate the "Breach Likelihood Score" (our predictive feature)
# A weighted score based on vulnerabilities, compliance, and history
def calculate_breach_likelihood(row):
    score = 0
    # Weight vulnerabilities heavily
    score += row['OpenVulnerabilities'] * 0.5
    # Add points for non-compliance
    if row['ISO27001_Compliance'] == 'Non-Compliant':
        score += 20
    elif row['ISO27001_Compliance'] == 'Partially Compliant':
        score += 10
    # Add points for past incidents
    score += row['IncidentHistory'] * 15
    return min(int(score), 100) # Cap the score at 100

df['BreachLikelihoodScore'] = df.apply(calculate_breach_likelihood, axis=1)


# --- Final Touches ---

# Save the DataFrame to a CSV file
output_path = 'vendor_risk_data.csv'
df.to_csv(output_path, index=False)

print(f"✅ Successfully generated synthetic data for {NUM_VENDORS} vendors.")
print(f"✅ File saved to: {output_path}")
print("\nFirst 5 rows of the data:")
print(df.head())