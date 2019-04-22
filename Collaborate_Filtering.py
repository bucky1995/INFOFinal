import csv
import numpy as np
import pandas as pd
from mlxtend.preprocessing import minmax_scaling
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error
from math import sqrt
from itertools import permutations

# min-max ranking
def change(x):
    x = 5*x
    return x

# without log
def ranking1(df):
    game_list = df.columns.values.tolist()
    df = df.apply(np.log10)
    df = minmax_scaling(df, columns = game_list)
    df = df.apply(change)
    df = df.apply(np.ceil)
    return df

#with log
def ranking2(df):
    game_list = df.columns.values.tolist()
    df = df.apply(np.log10)
    df = minmax_scaling(df, columns = game_list)
    df = df.apply(change)
    df = df.apply(np.ceil)
    return df

#hybrid ranking
def recent_metric(df):
    df = df + 1
    df = df.apply(np.log10)
    df = (1/2)**df
    return df

def ranking3(df1,df2):
    df3 = df1 + (df1-0.5)*df2
    game_list = df3.columns.values.tolist()
    df3 = minmax_scaling(df3, columns = game_list)
    df3 = df3.apply(change)
    df3 = df3.apply(np.ceil)
    return df3

#pearsonr
def person(df,new_user):
    sim = []
    for i in range(df.shape[0]):
        existed_user = df.iloc[i].values.tolist()
        person = pearsonr(existed_user, new_user)
        sim.append(person[0])
    df_user = df.copy()
    df_user['sim'] = sim
    return df_user

#collaborative filtering
def collaborative_filtering(df, new_user):
    df2 = df[df['sim'] > 0].copy()
    if df2.shape[0] == 0:
        user = new_user
        max_num_index_list = np.array(user).argsort()[-3:-1][::-1].tolist()
    else:
        index = []
        user = new_user.copy()
        for i in range(len(user)):
             if user[i] == 0:
                index.append(i)
        for i in index:
            sim = []
            rank = []
            for j in range(df2.shape[0]):
                if df2.iloc[j][i] != 0:
                    sim.append(df2.iloc[j]['sim'])
                    rank.append(df2.iloc[j][i])
            mutiply = np.multiply(np.array(sim), np.array(rank))
            user[i] = sum(mutiply.tolist()) / sum(sim)

        max_num_index_list = np.array(user).argsort()[-6:-3][::-1].tolist()
    return user, max_num_index_list

#evaluation rmse
def evaluation(df):
    # train-test
    test_df = df.sample(frac=0.1)
    train_df = df.drop(test_df.index)
    test_df = test_df.reset_index()
    test_df = test_df.iloc[:, 1:]
    train_df = train_df.reset_index()
    train_df = train_df.iloc[:, 1:]

    # test: create user and truth
    really_test = test_df.copy()
    really_test.iloc[:, 10:] = 0

    # start evaluation
    y_truth = []
    y_predict = []
    for i in range(test_df.shape[0]):
        new_user = really_test.iloc[i].values.tolist()
        real_user = test_df.iloc[i].values.tolist()
        index = []
        for j in range(len(real_user)):
            if real_user[j] != 0 and j > 9:
                index.append(j)
        train = person(train_df, new_user)
        new_user, index_list = collaborative_filtering(train, new_user)
        for m in index:
            y_truth.append(real_user[m])
            y_predict.append(new_user[m])
    rmse = sqrt(mean_squared_error(y_truth, y_predict))
    return rmse

#read all data
df_1 = pd.read_csv("/Users/chengmo/Desktop/sample/570_playtime_forever.csv")
df_1 = df_1.drop_duplicates(subset='userid', keep='first')
df_1.columns=['userid','570']
df_all = df_1
df_2 = pd.read_csv("/Users/chengmo/Desktop/sample/730_playtime_forever.csv")
df_2 = df_2.drop_duplicates(subset='userid', keep='first')
df_2.columns=['userid','730']
df_all = pd.merge(df_all, df_2, on='userid', how='outer')
df_3 = pd.read_csv("/Users/chengmo/Desktop/sample/72850_playtime_forever.csv")
df_3 = df_3.drop_duplicates(subset='userid', keep='first')
df_3.columns=['userid','72850']
df_all = pd.merge(df_all, df_3, on='userid', how='outer')
df_4 = pd.read_csv("/Users/chengmo/Desktop/sample/209160_playtime_forever.csv")
df_4 = df_4.drop_duplicates(subset='userid', keep='first')
df_4.columns=['userid','209160']
df_all = pd.merge(df_all, df_4, on='userid', how='outer')
df_5 = pd.read_csv("/Users/chengmo/Desktop/sample/218620_playtime_forever.csv")
df_5 = df_5.drop_duplicates(subset='userid', keep='first')
df_5.columns=['userid','218620']
df_all = pd.merge(df_all, df_5, on='userid', how='outer')
df_6 = pd.read_csv("/Users/chengmo/Desktop/sample/271590_playtime_forever.csv")
df_6 = df_6.drop_duplicates(subset='userid', keep='first')
df_6.columns=['userid','271590']
df_all = pd.merge(df_all, df_6, on='userid', how='outer')
df_7 = pd.read_csv("/Users/chengmo/Desktop/sample/292030_playtime_forever.csv")
df_7 = df_7.drop_duplicates(subset='userid', keep='first')
df_7.columns=['userid','292030']
df_all = pd.merge(df_all, df_7, on='userid', how='outer')
df_8 = pd.read_csv("/Users/chengmo/Desktop/sample/359550_playtime_forever.csv")
df_8 = df_8.drop_duplicates(subset='userid', keep='first')
df_8.columns=['userid','359550']
df_all = pd.merge(df_all, df_8, on='userid', how='outer')
df_9 = pd.read_csv("/Users/chengmo/Desktop/sample/365590_playtime_forever.csv")
df_9 = df_9.drop_duplicates(subset='userid', keep='first')
df_9.columns=['userid','365590']
df_all = pd.merge(df_all, df_9, on='userid', how='outer')
df_10 = pd.read_csv("/Users/chengmo/Desktop/sample/374320_playtime_forever.csv")
df_10 = df_10.drop_duplicates(subset='userid', keep='first')
df_10.columns=['userid','374320']
df_all = pd.merge(df_all, df_10, on='userid', how='outer')
df_11 = pd.read_csv("/Users/chengmo/Desktop/sample/377160_playtime_forever.csv")
df_11 = df_11.drop_duplicates(subset='userid', keep='first')
df_11.columns=['userid','377160']
df_all = pd.merge(df_all, df_11, on='userid', how='outer')
df_12 = pd.read_csv("/Users/chengmo/Desktop/sample/530620_playtime_forever.csv")
df_12 = df_12.drop_duplicates(subset='userid', keep='first')
df_12.columns=['userid','530620']
df_all = pd.merge(df_all, df_12, on='userid', how='outer')
df_13 = pd.read_csv("/Users/chengmo/Desktop/sample/578080_playtime_forever.csv")
df_13 = df_13.drop_duplicates(subset='userid', keep='first')
df_13.columns=['userid','578080']
df_all = pd.merge(df_all, df_13, on='userid', how='outer')
df_14 = pd.read_csv("/Users/chengmo/Desktop/sample/582010_playtime_forever.csv")
df_14 = df_14.drop_duplicates(subset='userid', keep='first')
df_14.columns=['userid','582010']
df_all = pd.merge(df_all, df_14, on='userid', how='outer')
df_15 = pd.read_csv("/Users/chengmo/Desktop/sample/582160_playtime_forever.csv")
df_15 = df_15.drop_duplicates(subset='userid', keep='first')
df_15.columns=['userid','582160']
df_all = pd.merge(df_all, df_15, on='userid', how='outer')
df_16 = pd.read_csv("/Users/chengmo/Desktop/sample/812140_playtime_forever.csv")
df_16 = df_16.drop_duplicates(subset='userid', keep='first')
df_16.columns=['userid','812140']
df_all = pd.merge(df_all, df_16, on='userid', how='outer')
df_17 = pd.read_csv("/Users/chengmo/Desktop/sample/814380_playtime_forever.csv")
df_17 = df_17.drop_duplicates(subset='userid', keep='first')
df_17.columns=['userid','814380']
df_all = pd.merge(df_all, df_17, on='userid', how='outer')
df_18 = pd.read_csv("/Users/chengmo/Desktop/sample/841370_playtime_forever.csv")
df_18 = df_18.drop_duplicates(subset='userid', keep='first')
df_18.columns=['userid','841370']
df_all = pd.merge(df_all, df_18, on='userid', how='outer')
df_19 = pd.read_csv("/Users/chengmo/Desktop/sample/863550_playtime_forever.csv")
df_19 = df_19.drop_duplicates(subset='userid', keep='first')
df_19.columns=['userid','863550']
df_all = pd.merge(df_all, df_19, on='userid', how='outer')
df_20 = pd.read_csv("/Users/chengmo/Desktop/sample/883710_playtime_forever.csv")
df_20 = df_20.drop_duplicates(subset='userid', keep='first')
df_20.columns=['userid','883710']
df_all = pd.merge(df_all, df_20, on='userid', how='outer')

#read recent data
df_1 = pd.read_csv("/Users/chengmo/Desktop/sample/570_playtime_last_two_weeks.csv")
df_1 = df_1.drop_duplicates(subset='userid', keep='first')
df_1.columns=['userid','570']
df_recent = df_1
df_2 = pd.read_csv("/Users/chengmo/Desktop/sample/730_playtime_last_two_weeks.csv")
df_2 = df_2.drop_duplicates(subset='userid', keep='first')
df_2.columns=['userid','730']
df_recent = pd.merge(df_recent, df_2, on='userid', how='outer')
df_3 = pd.read_csv("/Users/chengmo/Desktop/sample/72850_playtime_last_two_weeks.csv")
df_3 = df_3.drop_duplicates(subset='userid', keep='first')
df_3.columns=['userid','72850']
df_recent = pd.merge(df_recent, df_3, on='userid', how='outer')
df_4 = pd.read_csv("/Users/chengmo/Desktop/sample/209160_playtime_last_two_weeks.csv")
df_4 = df_4.drop_duplicates(subset='userid', keep='first')
df_4.columns=['userid','209160']
df_recent = pd.merge(df_recent, df_4, on='userid', how='outer')
df_5 = pd.read_csv("/Users/chengmo/Desktop/sample/218620_playtime_last_two_weeks.csv")
df_5 = df_5.drop_duplicates(subset='userid', keep='first')
df_5.columns=['userid','218620']
df_recent = pd.merge(df_recent, df_5, on='userid', how='outer')
df_6 = pd.read_csv("/Users/chengmo/Desktop/sample/271590_playtime_last_two_weeks.csv")
df_6 = df_6.drop_duplicates(subset='userid', keep='first')
df_6.columns=['userid','271590']
df_recent = pd.merge(df_recent, df_6, on='userid', how='outer')
df_7 = pd.read_csv("/Users/chengmo/Desktop/sample/292030_playtime_last_two_weeks.csv")
df_7 = df_7.drop_duplicates(subset='userid', keep='first')
df_7.columns=['userid','292030']
df_recent = pd.merge(df_recent, df_7, on='userid', how='outer')
df_8 = pd.read_csv("/Users/chengmo/Desktop/sample/359550_playtime_last_two_weeks.csv")
df_8 = df_8.drop_duplicates(subset='userid', keep='first')
df_8.columns=['userid','359550']
df_recent = pd.merge(df_recent, df_8, on='userid', how='outer')
df_9 = pd.read_csv("/Users/chengmo/Desktop/sample/365590_playtime_last_two_weeks.csv")
df_9 = df_9.drop_duplicates(subset='userid', keep='first')
df_9.columns=['userid','365590']
df_recent = pd.merge(df_recent, df_9, on='userid', how='outer')
df_10 = pd.read_csv("/Users/chengmo/Desktop/sample/374320_playtime_last_two_weeks.csv")
df_10 = df_10.drop_duplicates(subset='userid', keep='first')
df_10.columns=['userid','374320']
df_recent = pd.merge(df_recent, df_10, on='userid', how='outer')
df_11 = pd.read_csv("/Users/chengmo/Desktop/sample/377160_playtime_last_two_weeks.csv")
df_11 = df_11.drop_duplicates(subset='userid', keep='first')
df_11.columns=['userid','377160']
df_recent = pd.merge(df_recent, df_11, on='userid', how='outer')
df_12 = pd.read_csv("/Users/chengmo/Desktop/sample/530620_playtime_last_two_weeks.csv")
df_12 = df_12.drop_duplicates(subset='userid', keep='first')
df_12.columns=['userid','530620']
df_recent = pd.merge(df_recent, df_12, on='userid', how='outer')
df_13 = pd.read_csv("/Users/chengmo/Desktop/sample/578080_playtime_last_two_weeks.csv")
df_13 = df_13.drop_duplicates(subset='userid', keep='first')
df_13.columns=['userid','578080']
df_recent= pd.merge(df_recent, df_13, on='userid', how='outer')
df_14 = pd.read_csv("/Users/chengmo/Desktop/sample/582010_playtime_last_two_weeks.csv")
df_14 = df_14.drop_duplicates(subset='userid', keep='first')
df_14.columns=['userid','582010']
df_recent = pd.merge(df_recent, df_14, on='userid', how='outer')
df_15 = pd.read_csv("/Users/chengmo/Desktop/sample/582160_playtime_last_two_weeks.csv")
df_15 = df_15.drop_duplicates(subset='userid', keep='first')
df_15.columns=['userid','582160']
df_recent = pd.merge(df_recent, df_15, on='userid', how='outer')
df_16 = pd.read_csv("/Users/chengmo/Desktop/sample/812140_playtime_last_two_weeks.csv")
df_16 = df_16.drop_duplicates(subset='userid', keep='first')
df_16.columns=['userid','812140']
df_recent = pd.merge(df_recent, df_16, on='userid', how='outer')
df_17 = pd.read_csv("/Users/chengmo/Desktop/sample/814380_playtime_last_two_weeks.csv")
df_17 = df_17.drop_duplicates(subset='userid', keep='first')
df_17.columns=['userid','814380']
df_recent = pd.merge(df_recent, df_17, on='userid', how='outer')
df_18 = pd.read_csv("/Users/chengmo/Desktop/sample/841370_playtime_last_two_weeks.csv")
df_18 = df_18.drop_duplicates(subset='userid', keep='first')
df_18.columns=['userid','841370']
df_recent= pd.merge(df_recent, df_18, on='userid', how='outer')
df_19 = pd.read_csv("/Users/chengmo/Desktop/sample/863550_playtime_last_two_weeks.csv")
df_19 = df_19.drop_duplicates(subset='userid', keep='first')
df_19.columns=['userid','863550']
df_recent = pd.merge(df_recent, df_19, on='userid', how='outer')
df_20 = pd.read_csv("/Users/chengmo/Desktop/sample/883710_playtime_last_two_weeks.csv")
df_20 = df_20.drop_duplicates(subset='userid', keep='first')
df_20.columns=['userid','883710']
df_recent = pd.merge(df_recent, df_20, on='userid', how='outer')

#all the possibility of input
perm = set(permutations([5,5,5,0,0,0,0,0,0,0]))
perm = list(perm)
perm2 = [0,0,0,0,0,0,0,0,0,0]
insert = []
for i in perm:
    i = list(i) + perm2
    insert.append(i)

#build the user-item matrix preprocessing and remove the only-one user
df_all = df_all[df_all['userid']!= 'userid']
df_recent = df_recent[df_recent['userid'] != 'userid']

df_user = df_all.copy()
df_user = df_user.set_index(['userid'])
user = pd.DataFrame(df_user.count(axis = 1))
user = user[user[0]>1]
user = user.index.values.tolist()
df_all = df_all[df_all.userid.isin(user)]
df_all = df_all.set_index(['userid'])
df_all = df_all.convert_objects(convert_numeric=True)

df_recent = df_recent[df_recent.userid.isin(user)]
df_recent = df_recent.set_index(['userid'])
df_recent = df_recent.convert_objects(convert_numeric=True)

#time to ranking
df_ranking1 = ranking1(df_all)
df_ranking2 = ranking2(df_all)
df_add = recent_metric(df_all)
df_ranking3 = ranking3(df_all, df_recent)
df_ranking1 = df_ranking1.fillna(0)
df_ranking2 = df_ranking2.fillna(0)
df_ranking3 = df_ranking3.fillna(0)

# write file
with open('result.csv','w') as PF:
    fieldnames = {'input','result1','result2','result3'}
    PFwriter = csv.DictWriter(PF, fieldnames=fieldnames)
    PFwriter.writeheader()
    for i in insert:
        df_person1 = person(df_ranking1,i)
        max_num_index_list1 = collaborative_filtering(df_person1, i)[1]
        df_person2 = person(df_ranking2,i)
        max_num_index_list2 = collaborative_filtering(df_person2, i)[1]
        df_person3 = person(df_ranking3, i)
        max_num_index_list3 = collaborative_filtering(df_person3, i)[1]

        PFwriter.writerow(
            {'input': i,
             'result1': max_num_index_list1,
             'result2': max_num_index_list2,
             'result3': max_num_index_list3
             })
    PF.close()
#evaluation
print(evaluation(df_ranking1))
print(evaluation(df_ranking2))
print(evaluation(df_ranking3))






