import glob
from scipy.io import wavfile
from pylab import *

male = [85, 155]
female = [165, 255]


def hps(signal, iterations=6):
    original_signal = copy(signal)
    for i in range(2, iterations):
        tmp = copy(original_signal[::i])
        signal = signal[:len(tmp)]
        signal *= tmp
    return signal


def gender_voice_recognition(rate, data):
    seconds = int(floor(len(data) / rate))
    samples = [data[i * rate: (i + 1) * rate] for i in range(seconds)]
    results = []
    for sample in samples:
        fft_sample = abs(fft(sample)) / rate
        results.append(hps(fft_sample))
    result = [0] * results[0]
    for res in results:
        result += res
    if sum(result[male[0]:male[1]]) > sum(result[female[0]:female[1]]):
        return 1
    return 0


# 1 - male, 0 - female
M = [[0, 0], [0, 0]]
files = glob.glob("samples/*.wav")
for f in files:
    rate, data = wavfile.read(f)
    correct_answer = int(f[-5] == "M")
    answer = gender_voice_recognition(rate, data)
    M[correct_answer][answer] += 1


print(M)
percentage = (M[0][0] + M[1][1]) / (sum(M[0]) + sum(M[1]))
print(percentage)
