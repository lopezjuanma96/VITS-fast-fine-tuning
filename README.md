This repo is a pipeline of VITS finetuning for fast speaker adaptation TTS, and any-to-any voice conversion. 
Forked from [here](https://github.com/Plachtaa/VITS-fast-fine-tuning) to be adapted to Spanish.
Ideally all changes should be done adding spanish as an option and not as a replacement, so that it then could be PRd to the main repo.

TODO list:
- [] Add sentences to [](user_voice/user_voice.txt) in spanish. Some valid options could be from the [Commmon Voice Dataset](https://commonvoice.mozilla.org/en/datasets), these are shorter and more accessible, or the [CSS10 Dataset](https://github.com/Kyubyong/css10), far bigger and more complex but those are the sentences the original model was trained on.
- [] Add spanish.py to [](text), although I don't know what could be addeed there, and spanish to cleaners (the original model used multilingual cleaners, we could start on that an improve it later, as long as it does ot break the original model, which has happend to us before). More importantly, it seems [](configs/finetune_speaker.json) and [](configs/modified_finetune_speaker.json) provide one single cleaner cjke that fuses all language cleanings, so maybe that is where we should focus.
- [] Find a valid link for getting the spanish model (or maybe load it on Google Drive or this same repo) from coqui-AI.
- [] Add spanish model with utils.load_model() on [](finetune_speaker.py) and figure out how to set it so Spanish setting uses that.
- [] Add "\[ES\]" to strip in [](user_voice_collect.py) (or maybe use a regex solution?)
- [] I see [](utils.py) has a lastest_checkpoint_path function wich default search value is "G_*.pth", which got me thinking, since we won't use G_trilingual.pth as a base model if we should change not only this behaviour but also the saving process. We should be careful not to break the English & Japanese modes when doing so to be able to do PR later.
- [] Add spanish on the different points of [](VC_inference.py)
- [] [](voice_upload.py) and [](whisper_transcribe.py) seem to be useful for character training. If that's the case we can see what we can provide to add more data to this paradigm too.
- [] Since the original Colab Notebook clones the original repo, using it won't have all these modifications, so create a new notebook to use until we might get a PR and Spanish can be used in the original one.
- [] Since we are at it, create a README_ES.md file.

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
It's recommended to perform fine-tuning on [Google Colab](https://colab.research.google.com/drive/1omMhfYKrAAQ7a6zOCsyqpla-wU-QyfZn?usp=sharing)
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
