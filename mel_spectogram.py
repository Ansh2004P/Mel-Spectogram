import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

def plot_mel_spectrogram(audio_path, n_mels=128, hop_length=512, show_plot=True, save_plot=True):
    y, sr = librosa.load(audio_path, sr=None)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, hop_length=hop_length)
    S_dB = librosa.power_to_db(S, ref=np.max)

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_dB, sr=sr, hop_length=hop_length, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel Spectrogram')
    plt.tight_layout()
    
    if save_plot:
        # Create result folder if it doesn't exist
        result_dir = 'result'
        os.makedirs(result_dir, exist_ok=True)
        
        # Generate output filename based on input audio file
        audio_filename = os.path.splitext(os.path.basename(audio_path))[0]
        output_path = os.path.join(result_dir, f'{audio_filename}_mel_spectrogram.png')
        
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"Mel spectrogram saved to: {output_path}")
    
    if show_plot:
        plt.show()
    else:
        plt.close()

    return S_dB

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mel_spectrogram.py path_to_audio_file")
        sys.exit(1)

    audio_path = sys.argv[1]
    plot_mel_spectrogram(audio_path)
