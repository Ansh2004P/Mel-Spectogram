import os
import sys
import librosa
import soundfile as sf
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt


class MelSpectrogramPlotter:
    def __init__(
        self,
        audio_path,
        n_mels=128,
        hop_length=512,
        frame_length=1.0,
        overlap=0.5,
        fmax=8000,
        mode="mixed",   # NEW: choose between grunt, squeal, mixed
    ):
        self.audio_path = audio_path
        self.n_mels = n_mels
        self.hop_length = hop_length
        self.frame_length = frame_length
        self.overlap = overlap
        self.fmax = fmax
        self.mode = mode.lower()
        self.sr = None
        self.audio = None
        self.frames = []

        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        self.result_dir = os.path.join("result", f"{base_name}/{self.mode}")
        
        os.makedirs(self.result_dir, exist_ok=True)

    def load_audio(self):
        self.audio, self.sr = librosa.load(self.audio_path, sr=None)

    def split_frames(self):
        """Split audio into overlapping frames."""
        frame_size = int(self.frame_length * self.sr)
        step_size = int(frame_size * (1 - self.overlap))
        self.frames = []
        for start in range(0, len(self.audio) - frame_size + 1, step_size):
            end = start + frame_size
            self.frames.append(self.audio[start:end])

    def normalize_audio(self, audio):
        return audio / np.max(np.abs(audio))

    def pre_emphasize(self, audio, coeff=0.97):
        return np.append(audio[0], audio[1:] - coeff * audio[:-1])

    def remove_silence(self, top_db=None):
        if top_db is None:
            rms = librosa.feature.rms(y=self.audio).mean()
            db = librosa.amplitude_to_db([rms])[0]
            top_db = max(20, min(60, abs(db) * 0.6))
            print(f"Auto top_db set to: {top_db}")

        intervals = librosa.effects.split(self.audio, top_db=top_db)
        processed_audio = np.concatenate(
            [self.audio[start:end] for start, end in intervals]
        )
        return processed_audio

    def compute_mel_spectrogram(self, frame):
        S = librosa.feature.melspectrogram(
            y=frame,
            sr=self.sr,
            n_mels=self.n_mels,
            hop_length=self.hop_length,
            fmax=self.fmax,
        )
        return librosa.power_to_db(S, ref=np.max)

    def bandpass_filter(self, audio, sr):
        if self.mode == "grunt":
            low, high = 80, 800
        elif self.mode == "squeal":
            low, high = 500, 8000
        else:  # mixed
            low, high = 100, 8000

        nyq = 0.5 * sr
        low = low / nyq
        high = high / nyq
        b, a = butter(4, [low, high], btype="band")
        return filtfilt(b, a, audio)

    def save_frame_plot(self, S_dB, frame_idx):
        plt.figure(figsize=(8, 4))
        librosa.display.specshow(
            S_dB,
            sr=self.sr,
            hop_length=self.hop_length,
            x_axis="time",
            y_axis="mel",
            cmap="magma",
            fmax=self.fmax,
        )
        plt.colorbar(format="%+2.0f dB")
        plt.title(f"{self.mode.capitalize()} | Frame {frame_idx + 1}")
        plt.tight_layout()

        output_path = os.path.join(self.result_dir, f"frame_{frame_idx + 1}.png")
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Saved: {output_path}")

    def process(self, save_individual=True, show_plot=False):
        self.load_audio()
        self.audio = self.bandpass_filter(self.audio, self.sr)
        self.audio = self.normalize_audio(self.audio)
        self.audio = self.pre_emphasize(self.audio)
        processed_audio = self.remove_silence()

        output_wav = os.path.join(self.result_dir, "audio_no_silence.wav")
        sf.write(output_wav, processed_audio, self.sr)
        print(f"Saved silence-removed audio: {output_wav}")

        self.audio = processed_audio
        self.split_frames()

        for i, frame in enumerate(self.frames):
            S_db = self.compute_mel_spectrogram(frame)
            if save_individual:
                self.save_frame_plot(S_db, i)

        if show_plot:
            plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mel_spectrogram.py path_to_audio_file [mode]")
        print("Modes: grunt | squeal | mixed (default: mixed)")
        sys.exit(1)

    audio_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "mixed"
    plotter = MelSpectrogramPlotter(audio_path, fmax=8000, mode=mode)
    plotter.process()
