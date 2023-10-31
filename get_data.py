import opendatasets as od

dataset = 'https://www.kaggle.com/datasets/felipeesc/shark-attack-dataset/attacks.csv'
od.download(dataset, data_dir="./ressources")