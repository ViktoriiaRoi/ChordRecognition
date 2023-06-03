import os
import pandas as pd
import regex as re
import librosa

def get_music_files(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if f[-3:]=="mp3"]

def read_music(music_path):
    samples, sampling_rate = librosa.load(music_path)
    return samples, sampling_rate

def read_annotation(music_path):
    path = os.path.splitext(music_path)[0] + ".lab"
    annotation = pd.read_csv(path, sep=" ", header=None)
    annotation.columns = ['start', 'end', 'chord']
    annotation['chord'] = __simplify_chords(annotation)
    annotation.loc[annotation['chord'] == 'N', 'chord'] = annotation['chord'].mode()[0]
    return list(zip(annotation['start'], annotation['end'], annotation['chord']))

def __simplify_chords(chords_df):
    processed = chords_df['chord'].str.split(':maj')
    processed = [elem[0] for elem in processed]
    processed = [elem.split('/')[0] for elem in processed]
    processed = [elem.split('aug')[0] for elem in processed]
    processed = [elem.split(':(')[0] for elem in processed]
    processed = [elem.split('(')[0] for elem in processed]
    processed = [elem.split(':sus')[0] for elem in processed]
    processed = [re.split(":?\d", elem)[0] for elem in processed]
    processed = [elem.replace(':min', 'm') for elem in processed]
    processed = [elem.replace(':dim', 'm') for elem in processed]
    processed = [elem.replace(':hmin', 'm') for elem in processed]
    processed = [re.split(":$", elem)[0] for elem in processed]
    return processed
