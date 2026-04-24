# Large Language Models (LLMs) & Generative AI (GenAI)


!!! info
    Please refer to the University's **[AI Governance Policy](https://www.otago.ac.nz/administration/policies/policy-collection/ai-governance-policy)** and related **[AI Tools Guidance](https://www.otago.ac.nz/__data/assets/pdf_file/0027/631836/AI-Tool-Guidance-V3.1-1st-Dec-25.pdf)** document for general advice on responsible use of AI across the University.

This is a fast-moving field; We are currently trialling a number of different tools and deployment models for on-premises LLM/genAI.

We have a few models hosted entirely on-campus without dependencies on external cloud services, available for select trial usecases via an OpenAI-compatible API or 'ChatGPT-style' user interface.

Running these models locally within the campus environment necessitates significant resources that are currently **limited** due to our present hardware capabilities. Therefore usage should focus on scenarios where **on-campus processing** is absolutely necessary (e.g. sensitive data).

Email {{ support_email }} to discuss how we can help you support your particular usecase.

## Models


### Model list

The selection of available models may change, depending on specific demand, usecases and on available hardware resources.

Currently eResearch Solutions makes the following models available on-campus:


Name | Parameters | Precision | License | Usecases
---|---|---|---|---
DeepSeek-R1-Distill-Qwen-32B (DeepSeek, Alibaba Cloud) | 32B | bf16 | open source; MIT, Apache 2.0 | tasks requiring efficient reasoning, such as mathematical problem-solving, logical reasoning, and coding tasks; text-only
DeepSeek-R1-Distill-Qwen-32B (DeepSeek, Alibaba Cloud) | 32B | bf16 | open source; MIT, Apache 2.0 | tasks requiring efficient reasoning, such as mathematical problem-solving, logical reasoning, and coding tasks; text-only
Gemma3-12B-it (Google) | 12B | bf16 | custom; restrictions on use and training | question answering, summarisation; multi-modal input
bge-m3 (BAAI) | 1.5B | fp16 | open source; MIT | embeddings (e.g. in RAG pipelines)



## Model features to consider


### Parameters


More parameters allow the model to capture more complex patterns in the data at training, potentially improving accuracy, but at the cost of increased resource use and speed; It's a trade-off between complexity and performance.

### Quantisation

Quantisation is a model compression technique that reduces the precision of weights and activations, making LLMs more efficient. While quantised models can run on less powerful hardware, they may **sacrifice some accuracy** compared to their full-precision counterparts. However, advancements in quantisation techniques are helping to minimise this accuracy loss, making quantised models increasingly viable for various applications.

### License

*Truly Open, Open-Weights, or Restricted-Weights Open Access?* All models labeled "open" are not equal. Some follow **open-source principles** by offering the full stack — code, weights, training methodology, documentation under an open-source license. Others only publish the trained model weights, often under **restrictive** conditions that limit their usage or redistribution; These are commonly referred to as "open-weight" models.

### Distillation

Distilled LLM models are smaller, more efficient versions of large language models that retain much of the original model's performance while requiring less computational power and resources. This process, known as model distillation, involves **transferring knowledge from a larger model (the "teacher") to a smaller model (the "student")** to optimize it for specific tasks.
Distilled models are optimized for single-GPU setups and can deliver decent performance compared to the full model with much lower resource requirements.

### Chain-of-Thought

Chain-of-thought (CoT) is a technique that enhances a model's "reasoning" abilities by guiding them to articulate a series of intermediate steps before arriving at a final answer (i.e. seemingly "thinking" about a problem before providing a final answer).
This method helps break down complex problems into manageable parts, often improving accuracy and clarity in responses, and also allows the user the opportunity to study the "reasoning" behaviour of the model.

Most models can be prompted to employ CoT reasoning (e.g. by adding "Let's think step by step." to your prompt), but some 'reasoning'/'thinking' models are particularly well-trained for this and will apply Auto-CoT automatically.

Note that this is a **simulated reasoning-like process** that quickly breaks down once confronted with out-of-domain logical problems that don't match the specific logical patterns found in the model's training data. (See 'Limitations' below)


### LLM limitations and considerations

Large language models (LLMs) have gained significant attention due to their impressive capabilities. However there is also a lot of confusion and marketing hype surrounding LLMs and GenAI. 

These models excel in generating text that is contextually relevant by estimating the probability of different words or phrases occurring in a given context, allowing it to create coherent and contextually relevant responses.

However, it is crucial **not to anthropomorphise** LLMs' abilities. LLMs do not possess human-like reasoning or thinking capabilities. The [transformer architecture](https://en.wikipedia.org/wiki/Transformer_(deep_learning)) underlying these models allows them to **generate plausible text based on probabilistic pattern matching** but **does not enable genuine reasoning, introspection, intention or causal understanding**.

Prompting an LLM model is essentially guiding a statistical text generator to produce outputs based on your prompts.

The effectiveness of LLMs lies in their ability to generate the most plausible response to an input, showcasing strong performance on various tasks and emergent abilities. Nonetheless, it is essential to recognise and set realistic expectations for what LLMs can and cannot do, understanding their limitations.

Other considerations

* **LLMs may confidently produce plausible-sounding but factually incorrect or nonsensical responses**
* **Bias** can be a problem and should be considered in training and deployment
* LLMs are **expensive** to train and run, and consume lots of resources
