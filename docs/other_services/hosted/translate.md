# Translation

*For audio/video speech-to-text translation, see* [Audio/Video Speech-to-Text Transcription & Translation](stt.md)

## LibreTranslate

We have an exprimental on-campus deployment of [LibreTranslate](https://github.com/LibreTranslate/LibreTranslate), a free & open source machine translation web user interface and API;

[https://translate.rtis-k8s-charlie.uod.otago.ac.nz](https://translate.rtis-k8s-charlie.uod.otago.ac.nz)

Depending on the language, quality can vary but output is generally poor compared to some of the larger ML models/LLM-based translation.

### Supported languages

Arabic, Azerbaijani, Catalan, Chinese, Czech, Danish, Dutch, English, Esperanto, Finnish, French, German, Greek, Hebrew, Hindi, Hungarian, Indonesian, Irish, Italian, Japanese, Korean, Malay, Persian, Polish, Portuguese, Russian, Slovak, Spanish, Swedish, Turkish, Ukrainian, [and more](https://www.argosopentech.com/argospm/index/).

## LLMs

Many generic LLM models perform quite well when tasked with translating from one language to another (depending on source and target language, and the respective model's training).

e.g. with the prompt: *"Translate this into English: ....."*

See [Large Language Models (LLMs) & Generative AI (GenAI)](llm.md)

For translations of longer texts and documents, this will require splitting the full document into smaller chunks that fit within the model's context window, either manually or by using purpose-built tools that can interact with the OpenAI-compatible endpoint. (e.g. [TranslateBook with LLM (TBL)](https://github.com/hydropix/TranslateBookWithLLM)).
