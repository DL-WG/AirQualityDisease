import pandas as pd
from libs.disease.extract_disease import extract_disease


if __name__ == '__main__':
    patient_path = './data/patient/london_patients_postcode_details.csv'
    diseases = ['Cystic Fibrosis', 'COVID', 'ABPA', 'Asthma']
    df_patient = extract_disease(patient_path, diseases)
    postcode_path = './data/postcode_no2.xlsx'
    df_postcode = pd.read_excel(postcode_path)
    df_postcode_pati = df_postcode.merge(df_patient, on='postcode', how='left')
    df_postcode_pati = df_postcode_pati.drop(columns=['no2', 'polygons'])
    df_postcode_pati.to_excel('./data/postcode_diseases.xlsx', index=False)






