### unique spkrs

import os

data_path = '../../../../data/VCTK-Corpus/full_wav'
#one_hot_k = [0] * 109
uniq_spk = []
files = os.listdir(os.chdir(data_path))
print("files are", files)
for file in files:
    spkname = file.split('_')[0]
    if not spkname in uniq_spk:
       uniq_spk.append(spkname)
print("unique_speakers are", uniq_spk, "length is", len(uniq_spk))
one_hot_k = [0] * int(len(uniq_spk))
print(one_hot_k)


for spk_data in files:
    if spk_data.split('_')[0] in uniq_spk:
       print("spk is", spk_data.split('_')[0], "index is", uniq_spk.index(spk_data.split('_')[0]))

       one_hot_k[uniq_spk.index(spk_data.split('_')[0])] =1
       print("spk is", one_hot_k)
       one_hot_k = [0] * int(len(uniq_spk))
