import pandas as pd
import numpy as np


def extract_disease(patient_path, diseases=['Cystic Fibrosis', 'COVID', 'ABPA', 'Asthma']):
    df = pd.read_csv(patient_path)
    dis_df = pd.DataFrame(columns=['postcode'] + diseases)
    # dis_stat = pd.DataFrame(columns = ['postcode']+diseases)
    dis_stat = {}
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
            dis_stat[postcode] += flag

    for postcode in dis_stat:
        row = {name:value for name, value in zip(['postcode'] + diseases, [postcode] + list(dis_stat[postcode]))}
        dis_df = dis_df.append(row, ignore_index=True)

    return dis_df
