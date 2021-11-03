import os
import glob
from utils.display import *
from utils.dsp import *
from utils import hparams as hp
from multiprocessing import Pool, cpu_count
from utils.paths import Paths
import pickle
import argparse
from utils.text.recipes import arctic
from utils.files import get_files
from pathlib import Path
import numpy

# Helper functions for argument types
def valid_n_workers(num):
    n = int(num)
    if n < 1:
        raise argparse.ArgumentTypeError('%r must be an integer greater than 0' % num)
    return n

parser = argparse.ArgumentParser(description='Preprocessing for WaveRNN and Tacotron')
parser.add_argument('--path', '-p', help='directly point to dataset path (overrides hparams.wav_path')
parser.add_argument('--extension', '-e', metavar='EXT', default='.wav', help='file extension to search for in dataset folder')
parser.add_argument('--num_workers', '-w', metavar='N', type=valid_n_workers, default=cpu_count()-1, help='The number of worker threads to use for preprocessing')
parser.add_argument('--hp_file', metavar='FILE', default='hparams.py', help='The file to use for the hyperparameters')
args = parser.parse_args()

hp.configure(args.hp_file)  # Load hparams from file
if args.path is None:
    args.path = hp.wav_path

extension = args.extension
path = args.path
#print("wav folder is", path)


##### Creating Unique speakers for 1-hot-k representation #####

uniq_spk = []
files = os.listdir(os.chdir(path))
##print("files are", files)
for file in files:
    spkname = file.split('_')[0]
    if not spkname in uniq_spk:
       uniq_spk.append(spkname)
###print("unique_speakers are", uniq_spk, "length is", len(uniq_spk))
###print(one_hot_k)

###############################################################

def convert_file(path: Path):
    y = load_wav(path)
###    print("path in convert is", path, os.path.basename(path).split('.')[0])
    peak = np.abs(y).max()
    if hp.peak_norm or peak > 1.0:
        y /= peak
    mel = melspectrogram(y)

############ concatenating mel and 1 hot k representation #######

###    print("mel is", numpy.shape(mel), "mel is", mel)
    one_hot_k = numpy.zeros((71, numpy.shape(mel)[1]))
###    print("spk id in convert file is", os.path.basename(path).split('.')[0].split('_')[0])
    if os.path.basename(path).split('.')[0].split('_')[0] in uniq_spk:
       one_hot_k[uniq_spk.index(os.path.basename(path).split('.')[0].split('_')[0])]=1
###       print("one hot k i", one_hot_k, "vec 2 shape is", numpy.shape(one_hot_k))
    hk_mel = numpy.concatenate([one_hot_k,mel], axis=0)    
###    print("hk mel shape is", numpy.shape(hk_mel), hk_mel)
    if hp.voc_mode == 'RAW':
        quant = encode_mu_law(y, mu=2**hp.bits) if hp.mu_law else float_2_label(y, bits=hp.bits)
    elif hp.voc_mode == 'MOL':
        quant = float_2_label(y, bits=16)
    #print("quant is", quant)
    return mel.astype(np.float32), quant.astype(np.int64)



def process_wav(path: Path):
    wav_id = path.stem
    m, x = convert_file(path)
    np.save(paths.mel/f'{wav_id}.npy', m, allow_pickle=False)
    np.save(paths.quant/f'{wav_id}.npy', x, allow_pickle=False)
    return wav_id, m.shape[-1]


wav_files = get_files(path, extension)
paths = Paths(hp.data_path, hp.voc_model_id, hp.tts_model_id)

print(f'\n{len(wav_files)} {extension[1:]} files found in "{path}"\n')

if len(wav_files) == 0:

    print('Please point wav_path in hparams.py to your dataset,')
    print('or use the --path option.\n')

else:

    if not hp.ignore_tts:

        text_dict = arctic(path)

        with open(paths.data/'text_dict.pkl', 'wb') as f:
            pickle.dump(text_dict, f)

    n_workers = max(1, args.num_workers)

    simple_table([
        ('Sample Rate', hp.sample_rate),
        ('Bit Depth', hp.bits),
        ('Mu Law', hp.mu_law),
        ('Hop Length', hp.hop_length),
        ('CPU Usage', f'{n_workers}/{cpu_count()}')
    ])

    pool = Pool(processes=n_workers)
    dataset = []

    for i, (item_id, length) in enumerate(pool.imap_unordered(process_wav, wav_files), 1):
        dataset += [(item_id, length)]
        bar = progbar(i, len(wav_files))
        message = f'{bar} {i}/{len(wav_files)} '
        stream(message)

    print("paths . data is", paths.data)
    with open(paths.data/'dataset.pkl', 'wb') as f:
        pickle.dump(dataset, f)

    print('\n\nCompleted. Ready to run "python train_tacotron.py" or "python train_wavernn.py". \n')
