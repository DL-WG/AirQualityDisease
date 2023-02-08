
import pandas as pd
from scipy import stats


def calc_corr(aq_path, dise_path, aq='no2', diseases=['Cystic Fibrosis', 'COVID', 'ABPA', 'Asthma'], min_patients=3):
    df_aq = pd.read_excel(aq_path)
    df_dise = pd.read_excel(dise_path)
    # df_all = df_aq.merge(df_dise, on='postcode', how='left')
    corr = {}
    for disease in diseases:
        df_dise_sel = df_dise[df_dise[disease] > min_patients]
        df_temp = df_aq.merge(df_dise_sel[['postcode', disease]], on='postcode', how='left')
        df_temp.dropna(inplace=True)
        r, p_value = stats.pearsonr(df_temp[aq].values, df_temp[disease].values)
        corr[disease] = r
    return corr


if __name__ == '__main__':
    aq = 'no2'
    aq_path = f'data/postcode_{aq}.xlsx'
    dise_path = 'data/postcode_diseases.xlsx'
    corr = calc_corr(aq_path, dise_path, aq=aq)
    print(corr)


