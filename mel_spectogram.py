import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import soundfile as sf


class MelSpectrogramPlotter:
    """
    A class to compute and plot mel spectrogram frames from an audio file.
    """

    def __init__(
        self,
        audio_path,
        n_mels=128,
        hop_length=512,
        frame_length=1.0,
        overlap=0.5,
        fmax=8000,
    ):
        self.audio_path = audio_path
        self.n_mels = n_mels
        self.hop_length = hop_length
        self.frame_length = frame_length
        self.overlap = overlap
        self.fmax = fmax
        self.sr = None
        self.audio = None
        self.frames = []

        # Directory handling: create folder based on audio file name
        base_name = os.path.splitext(os.path.basename(audio_path))[0]
        self.result_dir = os.path.join("result", base_name)
        os.makedirs(self.result_dir, exist_ok=True)

    def load_audio(self):
        """Load audio from file."""
        self.audio, self.sr = librosa.load(self.audio_path, sr=None)

    def split_frames(self):
        """Split audio into overlapping frames."""
        frame_size = int(self.frame_length * self.sr)
        step_size = int(frame_size * (1 - self.overlap))
        self.frames = []
        for start in range(0, len(self.audio) - frame_size + 1, step_size):
            end = start + frame_size
            self.frames.append(self.audio[start:end])

    def remove_silence(self, top_db=40):
        """
        Remove silence from the loaded audio using librosa.effects.split.
        - top_db: threshold (in dB) below reference to consider as silence.
        Returns a new audio array with silence removed.
        """
        intervals = librosa.effects.split(self.audio, top_db=top_db)
        processed_audio = np.concatenate(
            [self.audio[start:end] for start, end in intervals]
        )
        return processed_audio

    def compute_mel_spectrogram(self, frame):
        """Compute mel spectrogram for a single frame."""
        S = librosa.feature.melspectrogram(
            y=frame,
            sr=self.sr,
            n_mels=self.n_mels,
            hop_length=self.hop_length,
            fmax=self.fmax,
        )
        return librosa.power_to_db(S, ref=np.max)

    def save_frame_plot(self, S_dB, frame_idx):
        """Save spectrogram plot for a single frame."""
        plt.figure(figsize=(8, 4))
        librosa.display.specshow(
            S_dB,
            sr=self.sr,
            hop_length=self.hop_length,
            x_axis="time",
            y_axis="mel",  # <- this gives mel scale
            cmap="magma",
            fmax=self.fmax,
        )
        plt.colorbar(format="%+2.0f dB")
        plt.title(f"Frame {frame_idx + 1}")
        plt.tight_layout()

        output_path = os.path.join(self.result_dir, f"frame_{frame_idx + 1}.png")
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Saved: {output_path}")

    def process(self, save_individual=True, show_plot=False):
        """Run full pipeline and save plots per frame."""
        self.load_audio()

        processed_audio = self.remove_silence(top_db=40)

        output_wav = os.path.join(self.result_dir, "audio_no_silence.wav")
        sf.write(output_wav, processed_audio, self.sr)
        print(f"Saved silence-removed audio: {output_wav}")

        self.audio = processed_audio

        # Now continue as before
        self.split_frames()

        for i, frame in enumerate(self.frames):
            S_db = self.compute_mel_spectrogram(frame)
            if save_individual:
                self.save_frame_plot(S_db, i)

        if show_plot:
            plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python mel_spectrogram.py path_to_audio_file")
        sys.exit(1)

    audio_path = sys.argv[1]
    plotter = MelSpectrogramPlotter(audio_path, fmax=8000)
    plotter.process()
