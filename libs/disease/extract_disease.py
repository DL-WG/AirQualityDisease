import os
import glob
import pandas as pd
import numpy as np


def extract_disease(patient_path, diseases=['Cystic Fibrosis', 'COVID', 'ABPA', 'Asthma'], drop_no_CT=True):
    df = pd.read_csv(patient_path)
    dis_df = pd.DataFrame(columns=['postcode', 'patient_num'] + diseases)
    if drop_no_CT:
        path = 'data/patient/london_CT_comments'
        all_files = os.listdir(path)
        csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))
        patient_id = [int(csv_name.split('_')[0]) for csv_name in csv_files]
        df = df[df.PATIENT_RK.isin(patient_id)]

    # dis_stat = pd.DataFrame(columns = ['postcode']+diseases)
    dis_stat = {}
    patient_num = {}
    for idx, row in df.iterrows():
        postcodes = eval(row['postcode and visit no']).keys()
        # flag = [1 if row[d] else 0 for d in diseases]
        flag = []
        for disease in diseases:
            if isinstance(row[disease], str) and row[disease]=='FALSE':
                row[disease] = False
            if row[disease]:
                flag.append(1)
            else:
                flag.append(0)

        for postcode in postcodes:
            if postcode not in dis_stat.keys():
                dis_stat[postcode] = np.zeros(len(diseases))
                patient_num[postcode] = 0
            dis_stat[postcode] += flag
            patient_num[postcode] += 1

    for postcode in dis_stat:
        row = {name:value for name, value in zip(['postcode', 'patient_num'] + diseases,
                                                 [postcode, patient_num[postcode]] + list(dis_stat[postcode]))}
        dis_df = dis_df.append(row, ignore_index=True)

    return dis_df
