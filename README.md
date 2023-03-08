This repo is a pipeline of VITS finetuning for fast speaker adaptation TTS, and any-to-any voice conversion. 
Forked from [here](https://github.com/Plachtaa/VITS-fast-fine-tuning) to be adapted to Spanish.
Ideally all changes should be done adding spanish as an option and not as a replacement, so that it then could be PRd to the main repo.

TODO list:
- [x] Add sentences to [](user_voice/user_voice.txt) in spanish. Some valid options could be from the [Commmon Voice Dataset](https://commonvoice.mozilla.org/en/datasets), these are shorter and more accessible, or the [CSS10 Dataset](https://github.com/Kyubyong/css10), far bigger and more complex but those are the sentences the original model was trained on.
- [ ] Add spanish.py to [](text), although I don't know what could be addeed there, and spanish to cleaners (the original model used multilingual cleaners, we could start on that an improve it later, as long as it does ot break the original model, which has happend to us before). More importantly, it seems [](configs/finetune_speaker.json) and [](configs/modified_finetune_speaker.json) provide one single cleaner cjke that fuses all language cleanings, so maybe that is where we should focus.
- [ ] From above, expand_numbers on spanish.py is yet to be tackled because a number to text is a pretty big task and it might not be super necessary ye if we choose the training sentences correclty, but it should be done in the future. 
- [x] Find a valid link for getting the spanish model (or maybe load it on Google Drive or this same repo) from coqui-AI. **Created a [model on HuggingFace](https://huggingface.co/lopezjm96/spanishVITS)**
- [x] Add spanish model with utils.load_model() on [](finetune_speaker.py) and figure out how to set it so Spanish setting uses that. **Changed utils.load_model(G_trilingual.pth) to utils.load_model(G_spanish.pth) this will make other languages impossible to use, but I couldn't find a way to include a condition on when to load which, maybe we can send language through the hps parameter of the run function, so:**
- [ ] change utils.load_model() on [](finetune_speaker.py) to differentiate when to load spanish and when trilingual.
- [ ] see if we can get an pretrained model in these models format, if not change the load_checkpoint function in [](utils.py) to include replace with default values when parameters are not found (such as `if 'iteration' not in model_checkpoint.keys(): model_checkpoint['iteration'] = 0`)
- [x] Add "\[ES\]" to strip in [](user_voice_collect.py) (or maybe use a regex solution?)
- [ ] I see [](utils.py) has a lastest_checkpoint_path function wich default search value is "G_*.pth", which got me thinking, since we won't use G_trilingual.pth as a base model if we should change not only this behaviour but also the saving process. We should be careful not to break the English & Japanese modes when doing so to be able to do PR later.
- [x] Add spanish on the different points of [](VC_inference.py)
- [ ] [](voice_upload.py) and [](whisper_transcribe.py) seem to be useful for character training. If that's the case we can see what we can provide to add more data to this paradigm too.
- [x] Since the original Colab Notebook clones the original repo, using it won't have all these modifications, so create a new notebook to use until we might get a PR and Spanish can be used in the original one.
- [ ] Since we are at it, create a README_ES.md file.
- [ ] Download part of the [CSS10 Dataset](https://www.kaggle.com/datasets/bryanpark/spanish-single-speaker-speech-dataset) to cover the same function as sample4ft did for the trilingual model. **Attempting [here](https://colab.research.google.com/github/lopezjuanma96/VITS-fast-fine-tuning/blob/main/ntbk/custom.ipynb)**
- [ ] Ask why this happens when using hotfix (and if it could affect training):
```
on checkpoint ./pretrained_models/G_trilingual.pth (actually our spanish model replacing G_trilingual) model has no iteration so setting to default 0
on checkpoint ./pretrained_models/G_trilingual.pth (actually our spanish model replacing G_trilingual) model has learning_rate so setting to default 0.001
on checkpoint ./pretrained_models/G_trilingual.pth (actually our spanish model replacing G_trilingual) model has optimizer but it is not a string

on checkpoint ./pretrained_models/D_trilingual.pth model has iteration but it is not a string
on checkpoint ./pretrained_models/D_trilingual.pth model has learning_rate but it is not a string
on checkpoint ./pretrained_models/D_trilingual.pth model has no optimizer  so setting to default AdamW
```
- [ ] From above: Appareantly the model from coqui is not directly compatible with this, but using it runs training as if it was a new model, so, two options:
    - Find a way to adapt the coqui model to this
    - First do the CSS10 Dataset item above, once that is done use it to retrain a compatible model from scratch, using it as the base user voice. **Attempting [here](https://colab.research.google.com/github/lopezjuanma96/VITS-fast-fine-tuning/blob/main/ntbk/custom.ipynb)**

[中文文档请点击这里](https://github.com/Plachtaa/VITS-fast-fine-tuning/blob/main/README_ZH.md)
# VITS Fast Fine-tuning
This repo will guide you to add your own character voices, or even your own voice, into an existing VITS TTS model
to make it able to do the following tasks in less than 1 hour:  

1. Any-to-any voice conversion between you & any characters you added & preset characters
2. English, Japanese & Chinese Text-to-Speech synthesis with the characters you added & preset characters  
  

Welcome to play around with the base model, a Trilingual Anime VITS!
[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Plachta/VITS-Umamusume-voice-synthesizer)

### Currently Supported Tasks:
- [x] Convert user's voice to characters listed [here](https://github.com/SongtingLiu/VITS_voice_conversion/blob/main/configs/finetune_speaker.json)
- [x] Chinese, English, Japanese TTS with user's voice
- [x] Chinese, English, Japanese TTS with custom characters!

### Currently Supported Characters for TTS & VC:
- [x] Umamusume Pretty Derby (Used as base model pretraining)
- [x] Sanoba Witch (Used as base model pretraining)
- [x] Genshin Impact (Used as base model pretraining)
- [x] Any character you wish as long as you have their voices!




## Fine-tuning
It's recommended to perform fine-tuning on [Google Colab](https://colab.research.google.com/github/lopezjuanma96/VITS-fast-fine-tuning/blob/main/ntbk/custom.ipynb)
because the original VITS has some dependencies that are difficult to configure.

### How long does it take? 
1. Install dependencies (2 min)
2. Record at least 20 your own voice, the content to read will be presented in UI, less than 20 words per sentence. (5~10 min)
3. Upload your character voices, which should be a `.zip` file,
it's file structure should be like:
```
Your-zip-file.zip
├───Character_name_1
├   ├───xxx.wav
├   ├───...
├   ├───yyy.mp3
├   └───zzz.wav
├───Character_name_2
├   ├───xxx.wav
├   ├───...
├   ├───yyy.mp3
├   └───zzz.wav
├───...
├
└───Character_name_n
    ├───xxx.wav
    ├───...
    ├───yyy.mp3
    └───zzz.wav
```
Note that the format & name of the audio files does not matter as long as they are audio files.  
Audio quality requirements: >=2s, <=10s per audio, background noise should be as less as possible.
Audio quantity requirements: at least 10 per character, better if 20+ per character.   
You can either choose to perform step 2, 3, or both, depending on your needs.  

4. Fine-tune (30 min)  
After everything is done, download the fine-tuned model & model config

## Inference or Usage (Currently support Windows only)
0. Remember to download your fine-tuned model!
1. Download the latest release
2. Put your model & config file into the folder `inference`, make sure to rename the model to `G_latest.pth` and config file to `finetune_speaker.json`
3. The file structure should be as follows:
```shell
inference
├───inference.exe
├───...
├───finetune_speaker.json
└───G_latest.pth
```
4. run `inference.exe`, the browser should pop up automatically.
