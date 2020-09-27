import pandas as pd
import pickle
import re

def pred(data_path):
    with open("./strage/lgbm_model.pickle", "rb") as f:
        model = pickle.load(f)  # 使用するモデル（数値のみを抽出して前処理最小限にしたもの）

    testest=pd.read_csv(data_path)
    testest=testest[['お仕事No.','勤務地　市区町村コード','給与/交通費　給与下限']]

    testest=testest.fillna(-1)

    pred=model.predict(testest)
    submit=pd.DataFrame()
    submit['お仕事No.']=testest['お仕事No.']
    submit["応募数 合計"]=pred
    submit.loc[submit['応募数 合計'] < 0, "応募数 合計"] = 0.0
    submit.to_csv(data_path,index=False)
    return data_path


