import pandas as pd
import warnings
from sklearn import preprocessing
from collections import Counter

def clean_data():
    # PREPARE DATA
    data = pd.read_csv('../data/train.csv').set_index("ID")
    test = pd.read_csv('../data/test.csv').set_index("ID")

    # remove constants
    nunique = pd.Series([data[col].nunique() for col in data.columns], index = data.columns)
    constants = nunique[nunique<2].index.tolist()
    data = data.drop(constants,axis=1)
    test = test.drop(constants,axis=1)

    pd.Series(constants).to_csv("../data/constants_index.csv")

def test_clean_data():
    data = pd.read_csv('../data/train_trial.csv').set_index('ID')
    constants = pd.read_csv('../data/constants_index.csv').values[:,1]
    data = data.drop(constants, axis=1)
    print data.columns

def constants_index():
    constants = pd.read_csv('../data/constants_index.csv').values[:,1]
    return constants


def find_unconverted_cols():
    warnings.filterwarnings('error')
    data = pd.read_csv('../data/train_trial.csv').set_index('ID')
    test = pd.read_csv('../data/test_trial.csv').set_index('ID')
    constants = pd.read_csv('../data/constants_index.csv').values[:,1]
    data = data.drop(constants, axis=1)
    unconverted_cols = pd.DataFrame()
    warnings_cols = pd.DataFrame()

    # encode string
    strings = data.dtypes == 'object'; strings = strings[strings].index.tolist(); encoders = {}
    for col in strings:
        encoders[col] = preprocessing.LabelEncoder()
        fill_gap(data, col)
        try:
            data[col] = encoders[col].fit_transform(data[col])
            try:
                test[col] = encoders[col].transform(test[col])
            except:
                unconverted_cols[col] = test[col]
        except:
            warnings_cols[col] = data[col]

    unconverted_cols.to_csv('../data/unconverted_cols.csv', index=False, header=True)
    warnings_cols.to_csv('../data/warnings_cols.csv', index=False, header=True)

def test_fill_gap():
    warnings.filterwarnings('error')
    data = pd.read_csv('../data/train_trial.csv').set_index('ID')
    fill_gap(data, "VAR_0274")
    print Counter(data["VAR_0274"])

def fill_gap(data, col):
    if any(data[col] == '-1') or any(data[col] == '') or any(pd.isnull(data[col])):
        data_counter = Counter(data[col])
        most = data_counter.most_common()[0][0]
        most_count = data_counter.most_common()[0][1]
        sum_total = sum(data_counter.values())
        if most != '-1' and \
           most != '' and \
           False == pd.isnull(most) and \
           (float)(most_count)/sum_total > 0.6 :
            if any(data[col] == '-1') :
                data[col] = data[col].replace('-1', most)
            if any(data[col] == '') :
                data[col] = data[col].replace('', most)
            if any(pd.isnull(data[col])):
                data.ix[pd.isnull(data[col]), col] = most


if __name__ == '__main__':
    find_unconverted_cols()
