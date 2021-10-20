import os

data_path = '../../../../data/VCTK-Corpus/wav48/'
one_hot_k = [0] * 109
print("spkj is", one_hot_k)
files = os.listdir(os.chdir(data_path))
for i in range(0,len(files)):

    print("i is", i)
    one_hot_k[i]='1'
    print("spk is", one_hot_k)
    one_hot_k = [0]*109
