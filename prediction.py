import pandas as pd
import pickle
import re

def pred(data_path):
    with open('./strage/cols.p', 'rb') as f:
        cols = pickle.load(f)
    with open('./strage/lgbm_model.pickle', 'rb') as f:
        model = pickle.load(f)

    testest=pd.read_csv(data_path)
    every_station = pd.read_csv('./strage/daily_every_station.csv')
    min_price=pd.read_excel('./strage/wage.xlsx')#各都道府県の最低賃金

    def income(ex_str):
        nums = []
        num1 = ""
        ex_str = str(ex_str)
        if (ex_str.find("【月収例】")) == -1:
            return -1
        else:
            nums = re.findall(r'\d+', ex_str)  # 数値部分のみを抽出（リスト）、最初の二つが給与になっている
            if len(nums) < 2:
                return 0
            else:
                if len(nums[1]) == 3:  # 桁の数を合わせる
                    num1 = "0" + nums[1]
                elif len(nums[1]) == 2:
                    num1 = "00" + nums[1]
                elif len(nums[1]) == 1:
                    num1 = "000" + nums[1]
                else:
                    num1 = nums[1]
                gessyuu = nums[0] + num1
                return int(gessyuu)

    # 最寄駅の1日の利用者
    def rep_st_num(xx):
        xx['station_daily_num1'] = 0
        xx['station_daily_num2'] = 0

        st_pref = every_station['pref']
        st_name = every_station['S12_001']
        st_num = every_station['S12_037']
        for t in range(len(st_num)):
            xx.loc[(xx["勤務地\u3000都道府県コード"] == every_station["pref"][t]) & (
                        xx["勤務地\u3000最寄駅1（駅名）"] == every_station["S12_001"][t]), "station_daily_num1"] = \
            every_station['S12_037'][t]
            xx.loc[(xx["勤務地\u3000都道府県コード"] == every_station["pref"][t]) & (
                        xx["勤務地\u3000最寄駅2（駅名）"] == every_station["S12_001"][t]), "station_daily_num2"] = \
            every_station['S12_037'][t]
        return xx#最寄駅の1日の利用者

    min_price = min_price.reset_index()
    min_price['index'] = min_price['index'] + 1
    price_dict = dict(zip(min_price["index"], min_price['最低賃金時間額【円】']))

    testest["income"]=testest["給与/交通費　備考"].apply(income)
    testest['残業']=testest['残業月20時間以上']*2+testest['残業月20時間未満']
    testest=testest.replace({'2019/11/27':2,'2019/9/25':0,'2019/10/24':1})
    testest['最低賃金']=testest["勤務地\u3000都道府県コード"].replace(price_dict)
    testest['overtime']=testest['残業月20時間以上']*2+testest['残業月20時間未満']
    testest=rep_st_num(testest)
    testest=testest.fillna(-1)
    testest=testest[cols]

    pred=model.predict(testest)
    submit=pd.DataFrame()
    submit['お仕事No.']=testest['お仕事No.']
    submit["応募数 合計"]=pred
    submit.loc[submit['応募数 合計'] < 0, "応募数 合計"] = 0.0
    submit.to_csv(data_path,index=False)
    return data_path


