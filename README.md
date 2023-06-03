# Chord Recognition
The script that converts any song's audio recording into a list of recognized chords along with their respective timestamps.

## Usage
```
pip install -r requirements.txt
python main.py <model> <action> <path/to/folder>
```
Arguments:
* model: can be `template`, (`hmm` is not implemented yet)
* action: can be `test` (return accuracy) or `predict` (return predicted list of chords)
* path: folder with `.mp3` files, and the for test action corresponding `.lab` files
