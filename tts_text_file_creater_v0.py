import os

txt_file_path = '/home1/srallaba/data/VCTK-Corpus/txt/'
spks = sorted(os.listdir(os.chdir(txt_file_path)))
print(spks)
for spk in spks:
    if spk =='p226':
       print('yesy')
       spk_files= sorted(os.listdir(os.chdir(spk)))
print(spk_files)

g = open('/home1/srallaba/data/VCTK-Corpus/p226.data','w')
f= open('/home1/srallaba/data/VCTK-Corpus/p226.txt')
for i, line in enumerate(f):

    line = line.split('\n')[0]
    g.write(spk_files[i].split('.')[0] + ' ' + str(line) + '\n')
g.close()
