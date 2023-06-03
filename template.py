import librosa
import numpy as np

import utils
import preprocessing
import visualization

class TemplateModel:
    def __init__(self):
        self.templates = self.__generate_templates()
    
    def __generate_templates(self):
        c_maj, c_min = np.zeros((2, 12))
        c_maj[[0,4,7]] = 1
        c_min[[0,3,7]] = 1
        templates = np.zeros((12, 24))
        for shift in range(12):
            templates[:, shift] = np.roll(c_maj, shift)
            templates[:, shift+12] = np.roll(c_min, shift)
        return templates

    def __distance(self, x,y):
        return np.linalg.norm(x-y)

    def __optimal_h(self, c, w):
        return np.inner(c, w) / np.inner(c, c)

    def __find_closest_chords(self, C, W):
        N = C.shape[1]
        K = W.shape[1]
        chords = np.zeros(N, dtype=np.int8)
        for n in range(N):
            c_n = C[:, n]
            distances = np.zeros(K)
            for k in range(K):
                w_k = W[:, k]
                h_kn = self.__optimal_h(c_n, w_k)
                distances[k] = self.__distance(h_kn * c_n, w_k)
            chords[n] = np.argmin(distances)
        return chords
    
    def __get_chord_label(self, chord_num):
        labels = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        chord = labels[chord_num % 12]
        if chord_num > 11:
            chord = chord + 'm'
        return chord
    
    def __convert_to_annotation(self, chords, duration):
        annotation = []
        curr_chord = chords[0]
        start = 0
        n = len(chords)
        seconds = duration / n
        for i in range(n):
            if chords[i] != curr_chord:
                annotation.append((start*seconds, i*seconds, self.__get_chord_label(curr_chord)))
                curr_chord = chords[i]
                start = i
        annotation.append((start*seconds, n*seconds, self.__get_chord_label(curr_chord)))
        return annotation

    def __predict_annotation(self, music_file):
        samples, sr = utils.read_music(music_file)
        C = librosa.feature.chroma_stft(y=samples, sr=sr)
        C_smooth = preprocessing.smooth_signal(C)
        chords = self.__find_closest_chords(C_smooth, self.templates)
        return self.__convert_to_annotation(chords, len(samples) / sr)
    
    def test(self, folder):
        metrics = []
        for music_file in utils.get_music_files(folder):
            real_ann = utils.read_annotation(music_file)
            predicted_ann = self.__predict_annotation(music_file)
            visualization.show_annotation(real_ann)
            visualization.show_annotation(predicted_ann)
            metrics.append(visualization.calculate_accuracy(real_ann, predicted_ann))
        print('Accuracy:', np.mean(metrics))

    def predict(self, folder):
        for music_file in utils.get_music_files(folder):
            predicted_ann = self.__predict_annotation(music_file)
            visualization.show_annotation(predicted_ann)
    