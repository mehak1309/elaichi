import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import json
import math
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader
import librosa
import soundfile as sf
import commons
import utils
from data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
import pandas as pd
from scipy.io.wavfile import write
import torchaudio as ta

def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm


# hps = utils.get_hparams_from_file("/home/tts/ttsteam/repos/repos-oov-h100/vits/logs/oov-vits/hi-itts/config.json")
# hps = utils.get_hparams_from_file("/home/tts/ttsteam/repos/vits/logs/oov-vits/hi-cha/config.json")
hps = utils.get_hparams_from_file("/home/tts/ttsteam/repos/vits/logs/oov-vits/hi-ivr/config.json") #change config json file
# hps = utils.get_hparams_from_file("/home/tts/ttsteam/repos/vits/logs/logs/in_tts_1k_cont/config.json") #change config json file
# hps = utils.get_hparams_from_file("/home/tts/ttsteam/repos/vits/logs/oov-vits/hi_synth/config.json") #change config json file

# hps = utils.get_hparams_from_file("/home/tts/ttsteam/repos/vits/logs/oov-vits/indic_30_cha_new/config.json")

# hps = utils.get_hparams_from_file("/home/tts/ttsteam/repos/vits/logs/oov-vits/hi-cha/config.json")

# hps = utils.get_hparams_from_file("/home/tts/ttsteam/repos/vits/logs/oov-vits/hi_1k_ivr_synth/config.json")  # 1k + Ivr + synth







net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    n_speakers=hps.data.n_speakers,
    n_emotions=hps.data.n_emotions,
    **hps.model).cuda()
_ = net_g.eval()

# _ = utils.load_checkpoint("/nlsasfs/home/ai4bharat/praveens/ttsteam/repos/vits/logs/indictts_base/G_56000.pth", net_g, None)
# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/logs/in_tts_1k_cont/G_273000.pth", net_g, None)
# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/indictts-all-13-cont/G_143000.pth", net_g, None)
# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/indictts-all-13-cont/G_65000.pth", net_g, None)


# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/oov-vits/hi-cha/G_140000.pth", net_g, None) #chnage checkpoint
# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/ckpts/checkpoints/indic_1k_latest/G_644000.pth", net_g, None) #chnage checkpoint
# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/oov-vits/hi_synth/G_80000.pth", net_g, None) #chnage checkpoint


# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/oov-vits/hi_synth/G_55000.pth", net_g, None) #change checkpoint

# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/ta-itts-ivr-ml-cont/G_30000.pth", net_g, None) #change checkpoint



### Final Set 

# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/repos-oov-h100/vits/logs/oov-vits/hi-itts/G_90000.pth", net_g, None)   # Checkpoint for base model hindi
# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/oov-vits/hi-cha/G_240000.pth", net_g, None) # Checkpoint for base + chha
# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/oov-vits/hi-ivr/G_50000.pth", net_g, None) # Checkpoint for base + IVR

# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/oov-vits/indic_30_cha_new/G_175000.pth", net_g, None) # IndicTTS All + chh
# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/logs/in_tts_1k_cont/G_644000.pth", net_g, None) # 1k hour model
# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/oov-vits/hi_synth/G_110000.pth", net_g, None) # base + synthetic model

_ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/oov-vits/hi-chha-ivr/G_170000.pth", net_g, None) # base + chha + ivr
# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/oov-vits/hi_1k_ivr_synth/G_152000.pth", net_g, None) # 1k + ivr + synth








### Ends here

# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/oov-vits/multi_itts_cls/G_205000.pth", net_g, None) #change checkpoint


# _ = utils.load_checkpoint("/home/tts/ttsteam/repos/vits/logs/oov-vits/ta_synth_2/G_70000.pth", net_g, None) #change checkpoint

# _ = utils.load_checkpoint("/nlsasfs/home/ai4bharat/praveens/ttsteam/repos/vits/logs/indictts_ta/G_211000.pth", net_g, None)
# _ = utils.load_checkpoint("/nlsasfs/home/ai4bharat/praveens/ttsteam/repos/vits/logs/indictts_hi/G_180000.pth", net_g, None)
# _ = utils.load_checkpoint("/nlsasfs/home/ai4bharat/praveens/ttsteam/repos/vits/logs/indictts_ta/G_211000.pth", net_g, None)

# df = pd.read_csv("/home/tts/ttsteam/repos/datasets/indictts/hi/metadata_test.csv", header=None, sep="|", names = ['id', 'text', 'speaker', 'emotion']) #chnage test file csv

df = pd.read_csv("/home/tts/ttsteam/repos/oov_plus_plus/lf_final_sentences.csv", header = None, sep = '|', names = ['id', 'text', 'speaker', 'emotion', 'bigram'])


audio_path = '/home/tts/ttsteam/repos/oov_plus_plus/eval/hindi_lf_final/base_chha_ivr'
 #changes outfile folder
os.makedirs(audio_path, exist_ok = True)

for ix, row in tqdm(df.iterrows()):
    stn_tst = get_text(f'  {row[1]}  .', hps)  # TODO Change this later
    with torch.no_grad():
        x_tst = stn_tst.cuda().unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)]).cuda()
        sid = torch.LongTensor([int(row[2])]).cuda()
        eid = torch.LongTensor([int(row[3])]).cuda()
        audio = net_g.infer(x_tst, x_tst_lengths, sid=sid, eid=eid, noise_scale=.667, noise_scale_w=0.8, length_scale=1)[0][0,0].data.cpu().float().numpy() #TODO change the length scale back to 1

        audio_file = os.path.join(audio_path, str(row[0])+'.wav')
        # audio_file = os.path.join(audio_path, os.path.basename(str(row[0]))+ '.wav')
        print (audio_file)
        write(audio_file, 24000, audio)

