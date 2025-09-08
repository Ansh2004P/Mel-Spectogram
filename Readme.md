# Mel Spectrogram Generator

A Python script for generating and visualizing mel spectrograms from audio files. This tool is useful for audio analysis, machine learning preprocessing, and acoustic research.

## Features

- Generate mel spectrograms from various audio formats (MP3, WAV, FLAC, etc.)
- Visualize spectrograms with customizable parameters
- Save high-quality spectrogram images to results folder
- Support for different mel filter bank sizes and hop lengths

## Prerequisites

- Python 3.7 or higher
- Git (for cloning the repository)

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd Spectogram
```

### 2. Create Virtual Environment

**On Windows (using bash):**
```bash
python -m venv venv
source venv/Scripts/activate
```

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python mel_spectogram.py path/to/your/audio/file.mp3
```

### Example

```bash
python mel_spectogram.py ./sounds/boar_sound.mp3
```

### Parameters

The script accepts the following parameters (modify in code):

- `n_mels`: Number of mel filter banks (default: 128)
- `hop_length`: Number of samples between successive frames (default: 512)
- `show_plot`: Display the plot (default: True)
- `save_plot`: Save the plot to results folder (default: True)

## Output

- **Display**: Shows the mel spectrogram visualization
- **Save**: Automatically saves high-resolution PNG files to the `result/` folder
- **Naming**: Output files are named as `{audio_filename}_mel_spectrogram.png`

## Project Structure

```
Spectogram/
├── mel_spectogram.py      # Main script
├── requirements.txt       # Python dependencies
├── sounds/               # Audio files directory
│   └── .gitkeep         # Keeps folder in Git
├── result/              # Generated spectrograms
│   └── .gitkeep         # Keeps folder in Git
├── venv/                # Virtual environment (not tracked)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## Dependencies

- `librosa`: Audio analysis library
- `matplotlib`: Plotting library
- `numpy`: Numerical computing

## Supported Audio Formats

- MP3
- WAV
- FLAC
- AAC
- OGG
- M4A

## Example Output

The script generates mel spectrograms showing:
- **X-axis**: Time (seconds)
- **Y-axis**: Mel frequency bins
- **Color**: Amplitude in decibels (dB)
- **Scale**: -80 dB (dark) to 0 dB (bright)

## Troubleshooting

### Virtual Environment Issues

If you encounter activation issues:

**Windows:**
```bash
source venv/Scripts/activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Missing Dependencies

If you get import errors:
```bash
pip install -r requirements.txt
```

### Audio File Not Found

Ensure your audio file path is correct:
```bash
# Use relative path
python mel_spectogram.py ./sounds/your_file.mp3

# Or absolute path
python mel_spectogram.py /full/path/to/your_file.mp3
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source. Please check the license file for more details.

## Contact

For questions or issues, please open an issue in the repository.