

# RS-Agent: Automating Remote Sensing Tasks through Intelligent Agent

[Wenjia Xu](https://xuwenjia.bupt.edu.cn/)†*, [Zijian Yu](#)†, [Boyang Mu](#), [Jiuniu Wang](#), [Zhiwei Wei](#)* and [Mugen Peng](https://teacher.bupt.edu.cn/pengmugen/zh_CN/index.htm)  
† Equal Contribution   * Corresponding Author

**State Key Laboratory of Networking and Switching Technology, Beijing University of Posts and Telecommunications**  
**School of Geographic Sciences, Hunan Normal University**  
**Aerospace Information Research Institute, Chinese Academy of Sciences**

[Website](https://intellisensing.github.io/RS-Agent/) | [Paper](https://doi.org/10.1007/s11432-026-5026-5) | [Video](https://github.com/user-attachments/assets/ca5a3494-a6dd-43ae-835e-f222caf2dd9d)





[Introduction](#introduction) | [Core Components](#core-components) | [Supported Function](#supported-function) | [Results](#results) | [Getting Started](#getting-started) | [Notes](#notes) | [Models](#models) | [Toolkit](#toolkit) | [Citation](#citation)

[https://github.com/user-attachments/assets/ca5a3494-a6dd-43ae-835e-f222caf2dd9d](https://github.com/user-attachments/assets/ca5a3494-a6dd-43ae-835e-f222caf2dd9d)

## Introduction

Recent advancements in Large Language Models (LLMs) and Multi-modal Large Language Models (MLLMs) have led to impressive performance in remote sensing tasks. However, these models are limited to basic vision and language tasks and lack specialized expertise for complex remote sensing applications. To address these, we propose **RS-Agent**, an intelligent agent for remote sensing. RS-Agent is powered by an LLM as its "Central Controller," enabling it to understand and respond to various problems. It integrates high-performance remote sensing image processing tools, allowing multi-tool, multi-turn conversations for complex tasks. Additionally, RS-Agent utilizes a knowledge graph-enhanced Retrieval-Augmented Generation (RAG) framework to access domain-specific knowledge, ensuring accurate responses to expert-level queries. Experimental results show RS-Agent achieves over 95% task planning accuracy and demonstrates strong domain-specific knowledge retrieval, excelling across various tasks.



## Core Components

1. **Central Controller**: Serves as the decision-making core of the agent. It interprets user queries, plans task execution, manages dialogue history, and synthesizes final responses.
2. **Toolkit**: A collection of state-of-the-art remote sensing tools for various applications. These tools are invoked based on the Central Controller's planning.
3. **Solution Space**: Stores predefined expert-level task solutions. It guides the Controller in selecting appropriate tools and execution strategies by retrieving relevant task-specific instructions via **Task-Aware Retrieval**.
4. **Knowledge Space**: Provides domain-specific information via a curated knowledge database. It supports expert-level reasoning by retrieving relevant content via **DualRAG**.



## Supported Function


| Tool                          | Function                                       | Example Input                                |
| ----------------------------- | ---------------------------------------------- | -------------------------------------------- |
| `cloud_removal`               | Cloud removal from satellite images            | Remove the clouds in this image.             |
| `image_dehazing`              | Haze removal from images                       | Dehaze this foggy image.                     |
| `super_resolution_2x`         | Image super-resolution (2×)                    | Enhance the resolution of this image.        |
| `denoising`                   | Image denoising                                | Remove noise from this image.                |
| `caption`                     | Geo-specific VQA and captioning                | What is in this remote sensing image?        |
| `optical_detection`           | Optical image target detection                 | Detect objects in this optical image.        |
| `optical_plane_type`          | Aircraft type recognition in optical images    | What type of aircraft is in this image?      |
| `scene`                       | Scene classification                           | What is the scene category of this image?    |
| `sar_detection`               | Target detection in SAR images                 | Find the objects in this SAR image.          |
| `sar_plane_type`              | Aircraft type recognition in SAR images        | Identify the aircraft in this SAR image.     |
| `knowledge_search`            | Aircraft info retrieval via Knowledge Database | Who manufactures Boeing 747?                 |
| `building_damage_detection`   | Building damage assessment                     | Which buildings are damaged?                 |
| `building_extraction`         | Building extraction from images                | Extract all buildings from the image.        |
| `road_extraction`             | Road extraction from images                    | Extract roads from the scene.                |
| `horizontal_object_detection` | Horizontal bounding box detection              | Detect objects using horizontal boxes.       |
| `rotated_object_detection`    | Rotated object detection                       | Detect objects using rotated boxes.          |
| `semantic_segmentation`       | Pixel-wise semantic segmentation               | Segment the different regions in this image. |
| `land_use_classification`     | Land use categorization                        | What are the land use types in this image?   |




## Results



### Quantitative Results

To evaluate RS-Agent's adaptability, we evaluate its task planning accuracy when paired with different closed-source (GPT series) and open-source LLMs.


| Task                             | ChatGPT (3.5-turbo-1106) | ChatGPT (3.5-turbo) | ChatGPT (4o-mini) | LLaMa 3.1 (8B) | LLaMa 3.1 (70B) | Qwen2.5 (14B) | Qwen2.5 (32B) | Qwen2.5 (72B) | DeepSeek-r1 (70B) |
| -------------------------------- | ------------------------ | ------------------- | ----------------- | -------------- | --------------- | ------------- | ------------- | ------------- | ----------------- |
|                                  | (87.71t/s)               | (65.03t/s)          | (58.87t/s)        | (100.78t/s)    | (17.71t/s)      | (69.61t/s)    | (36.77t/s)    | (16.24t/s)    | (18.25t/s)        |
| **Cloud Removal**                | 95.00%                   | 95.00%              | 100%              | 100%           | 100%            | 100%          | 95.00%        | 100%          | 100%              |
| **Image Dehazing**               | 30.00%                   | 95.00%              | 100%              | 100%           | 100%            | 100%          | 100%          | 100%          | 75.00%            |
| **Super Resolution**             | 100%                     | 100%                | 100%              | 0.00%          | 100%            | 100%          | 100%          | 100%          | 95.00%            |
| **Denoising**                    | 90.00%                   | 100%                | 100%              | 100%           | 100%            | 100%          | 100%          | 100%          | 90.00%            |
| **Image Captioning**             | 55.00%                   | 45.00%              | 90.00%            | 15.00%         | 60.00%          | 70.00%        | 80.00%        | 80.00%        | 10.00%            |
| **Object Detection**             | 75.00%                   | 60.00%              | 95.00%            | 30.00%         | 90.00%          | 90.00%        | 85.00%        | 100%          | 85.00%            |
| **Optical Plane Classification** | 100%                     | 100%                | 100%              | 100%           | 100%            | 100%          | 100%          | 100%          | 95.00%            |
| **Scene Classification**         | 20.00%                   | 90.00%              | 100%              | 80.00%         | 90.00%          | 90.00%        | 100%          | 100%          | 50.00%            |
| **SAR Detection**                | 30.00%                   | 100%                | 100%              | 75.00%         | 95.00%          | 100%          | 100%          | 100%          | 100%              |
| **SAR Plane Classification**     | 100%                     | 100%                | 100%              | 100%           | 100%            | 100%          | 100%          | 100%          | 90.00%            |
| **Knowledge Search**             | 100%                     | 100%                | 100%              | 100%           | 80.00%          | 100%          | 100%          | 100%          | 10.00%            |
| **Building Damage Detection**    | 100%                     | 100%                | 100%              | 100%           | 100%            | 95.00%        | 100%          | 100%          | 100%              |
| **Building Extraction**          | 10.00%                   | 70.00%              | 100%              | 55.00%         | 100%            | 100%          | 100%          | 100%          | 100%              |
| **Road Extraction**              | 15.00%                   | 55.00%              | 100%              | 65.00%         | 100%            | 100%          | 100%          | 100%          | 100%              |
| **Horizontal Detection**         | 20.00%                   | 55.00%              | 100%              | 95.00%         | 100%            | 100%          | 100%          | 100%          | 100%              |
| **Rotated Detection**            | 15.00%                   | 35.00%              | 100%              | 85.00%         | 90.00%          | 100%          | 100%          | 100%          | 100%              |
| **Semantic Segmentation**        | 60.00%                   | 100%                | 100%              | 80.00%         | 100%            | 100%          | 100%          | 100%          | 80.00%            |
| **Land Use Classification**      | 15.00%                   | 100%                | 100%              | 75.00%         | 100%            | 100%          | 100%          | 95.00%        | 95.00%            |
| **Average Accuracy**             | 57.22%                   | 82.50%              | 99.17%            | 75.28%         | 94.72%          | 96.94%        | 97.78%        | 98.61%        | 81.94%            |




### Qualitative Results



## Getting Started



### 1. Environment

```bash
git clone https://github.com/IntelliSensing/RS-Agent.git
cd RS-Agent
python -m venv .venv && source .venv/bin/activate   # optional
pip install -r requirements.txt
pip install -e .                                    # install rs_agent package
export PYTHONPATH=.
```



### 2. Configuration

```bash
cp .env.example .env
```

Edit `.env`:

```bash
OPENAI_API_KEY=your-key-here
OPENAI_API_BASE=https://api.openai.com/v1

# Embedding model: HuggingFace id or local path
EMBEDDING_MODEL=moka-ai/m3e-base
EMBEDDING_DEVICE=cpu
```



### 3. Build Solution Index (optional, pre-built indices included)

Pre-built FAISS indices are shipped under `data/indices/`. Rebuild if you change solution templates or the embedding model:

```bash
# RS-Agent (18 tools)
python scripts/build_solution_index.py

# RS-ChatGPT baseline (7 tools)
python scripts/build_solution_index.py \
  --source data/solutions/guidance_rschatgpt.txt \
  --output data/indices/solution_db_rschatgpt
```



### 4. Run Demo

```bash
python examples/demo.py \
    --question "Can you upscale this image to a higher resolution?"
```

By default this uses `examples/sample.png`. Override with `--image /path/to/your/image.png`.

## Notes

Before running the code, please keep the following in mind:

- **API Key required**: `examples/demo.py` and `benchmarks/planning/run_eval.py` call an LLM backend. Copy `.env.example` to `.env` and set `OPENAI_API_KEY` (and `OPENAI_API_BASE` if needed).
- **Network on first run**: Solution Space retrieval downloads `moka-ai/m3e-base` from HuggingFace, and the agent pulls the LangChain hub prompt — both require internet access.
- **Stub tools by default**: Tools in `rs_agent/toolkit/stubs.py` return placeholder outputs for **task planning evaluation** only. For real remote sensing inference, install the upstream models listed in the [Toolkit](#toolkit) section.
- **LangChain version**: Use `langchain>=0.3,<0.4` as pinned in `requirements.txt`. Newer LangChain releases may break imports such as `from langchain.tools import Tool`.
- **DualRAG reproduction**: Full Knowledge Space experiments need Ollama or an OpenAI-compatible API, plus a built index over the `mix` corpus. Follow `dualrag/reproduce/Step_1.py`–`Step_3.py` (see [dualrag/DUALRAG.md](dualrag/DUALRAG.md)).



## Models



### Agent Backbone (LLM)


| Component          | Default Model          | Notes                                        |
| ------------------ | ---------------------- | -------------------------------------------- |
| Central Controller | `gpt-4o-mini`          | Any OpenAI-compatible API supported          |
| Paper default      | `Qwen2.5-32B-Instruct` | Also validated with ChatGPT, LLaMA, DeepSeek |


Configure via `configs/default.yaml` or `.env`.

### Retrieval Models


| Component                 | Model          | Source                                                      |
| ------------------------- | -------------- | ----------------------------------------------------------- |
| Solution Space embedding  | `m3e-base`     | [moka-ai/m3e-base](https://huggingface.co/moka-ai/m3e-base) |
| Solution Space index      | FAISS          | Built from `data/solutions/guidance.txt`                    |
| Knowledge Space (DualRAG) | LightRAG + LLM | See `dualrag/DUALRAG.md`                                    |




## Toolkit

RS-Agent orchestrates specialized remote sensing tools via standardized APIs. Install the upstream repository and model weights for each tool before enabling real inference.

### Low-Level Processing


| RS-Agent Tool         | Task             | Upstream Repository                                           | Backbone Model |
| --------------------- | ---------------- | ------------------------------------------------------------- | -------------- |
| `denoising`           | Image denoising  | [JingyunLiang/SwinIR](https://github.com/JingyunLiang/SwinIR) | SwinIR         |
| `super_resolution_2x` | Super-resolution | [xinntao/Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) | Real-ESRGAN    |
| `image_dehazing`      | Image dehazing   | [WeiChen0/DACLIP-uir](https://github.com/WeiChen0/DACLIP-uir) | DACLIP         |
| `cloud_removal`       | Cloud removal    | Project-specific setup                                        | —              |




### Optical Analysis


| RS-Agent Tool                 | Task                        | Upstream Repository                                                   | Backbone Model                   |
| ----------------------------- | --------------------------- | --------------------------------------------------------------------- | -------------------------------- |
| `caption`                     | Captioning / VQA            | [mbzuai-oryx/GeoChat](https://github.com/mbzuai-oryx/GeoChat)         | GeoChat-7B                       |
| `optical_detection`           | Object detection & counting | [ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) | YOLOv8x-OBB (DOTA)               |
| `optical_plane_type`          | Aircraft type (optical)     | Custom classifier                                                     | ResNet-based, fine-tuned         |
| `scene`                       | Scene classification        | ViT (DINO-style)                                                      | ViT-B/16, fine-tuned on RSSDIVCS |
| `horizontal_object_detection` | Horizontal bbox detection   | [open-mmlab/mmdetection](https://github.com/open-mmlab/mmdetection)   | MMDetection                      |
| `rotated_object_detection`    | Rotated bbox detection      | [open-mmlab/mmrotate](https://github.com/open-mmlab/mmrotate)         | MMRotate                         |




### SAR Analysis


| RS-Agent Tool    | Task                 | Upstream Repository            | Backbone Model                  |
| ---------------- | -------------------- | ------------------------------ | ------------------------------- |
| `sar_detection`  | SAR object detection | DiffDet4SAR (Detectron2-based) | DiffDet                         |
| `sar_plane_type` | Aircraft type (SAR)  | Custom SAR classifier          | Fine-tuned on SAR aircraft data |




### Segmentation & Extraction


| RS-Agent Tool               | Task                       | Upstream Repository                                                                                  | Backbone Model     |
| --------------------------- | -------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------ |
| `semantic_segmentation`     | Semantic segmentation      | [open-mmlab/mmsegmentation](https://github.com/open-mmlab/mmsegmentation)                            | MMSegmentation     |
| `land_use_classification`   | Land use / land cover      | GeoSeg-based service                                                                                 | Segmentation model |
| `building_extraction`       | Building extraction        | [chrxianyu/RSBuilding](https://github.com/chrxianyu/RSBuilding)                                      | —                  |
| `road_extraction`           | Road extraction            | Project-specific setup                                                                               | —                  |
| `building_damage_detection` | Building damage assessment | [luuuyi/changeos](https://github.com/luuuyi/changeos) / [open-cd](https://github.com/likyoo/open-cd) | Change detection   |




### Knowledge


| RS-Agent Tool      | Task                | Upstream Repository                                                              | Backbone Model |
| ------------------ | ------------------- | -------------------------------------------------------------------------------- | -------------- |
| `knowledge_search` | Domain knowledge QA | [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG) (DualRAG fork in `dualrag/`) | LightRAG + LLM |




### RS-ChatGPT Baseline

For comparison with [Remote-Sensing-ChatGPT](https://github.com/HaonanGuo/Remote-Sensing-ChatGPT):


| Tool                       | Method         | Repository                                                                                |
| -------------------------- | -------------- | ----------------------------------------------------------------------------------------- |
| `Caption`                  | BLIP           | [salesforce/BLIP](https://github.com/salesforce/BLIP)                                     |
| `Scene`                    | ResNet         | AID-pretrained ResNet                                                                     |
| `detection` / `count_text` | YOLOv5-OBB     | [hukaixuan19970627/yolov5_obb](https://github.com/hukaixuan19970627/yolov5_obb)           |
| `Instance_Segmentation`    | Swin + UperNet | [open-mmlab/mmsegmentation](https://github.com/open-mmlab/mmsegmentation)                 |
| `landuse_Segmentation`     | HRNet          | [HRNet/HRNet-Semantic-Segmentation](https://github.com/HRNet/HRNet-Semantic-Segmentation) |
| `EdgeDetection`            | Canny          | OpenCV                                                                                    |




## Repository Structure

```
RS-Agent/
├── rs_agent/              # Core framework (Controller, Solution Space, Toolkit)
├── dualrag/               # DualRAG (modified LightRAG fork)
├── benchmarks/            # Evaluation scripts
├── data/                  # Solution DB and FAISS indices
├── configs/               # YAML configuration
├── scripts/               # Utility scripts
├── examples/              # Usage demos
└── images/                # Figures and logos
```



## DualRAG

The Knowledge Space uses DualRAG, implemented as a modified LightRAG fork. See [dualrag/DUALRAG.md](dualrag/DUALRAG.md) for installation and usage.

## Contributions

1. We present RS-Agent, a novel architecture designed to interpret user queries and orchestrate diverse tools for accurate and efficient remote sensing task execution.
2. We propose **Task-Aware Retrieval**, which retrieves expert-level task solutions to emulate professional remote sensing analysts.
3. We propose **DualRAG**, a retrieval augmented generation method with weighted keyword-aware dual-path retrieval.
4. Extensive experiments demonstrate RS-Agent consistently surpasses previous SOTA MLLMs across remote sensing applications.



## Citation

```bibtex
@article{rsagent,
  author = "Xu Wenjia,Yu Zijian,Mu Boyang,Wang Jiuniu,Wei Zhiwei,Peng MuGen",
  title = "RS-Agent: Automating Remote Sensing Tasks through Intelligent Agent",
  journal = "SCIENCE CHINA Information Sciences",
  year = "2026",
  pages = "-",
  url = "http://www.sciengine.com/publisher/Science China Press/journal/SCIENCE CHINA Information Sciences///10.1007/s11432-026-5026-5",
  doi = "https://doi.org/10.1007/s11432-026-5026-5"
}
```



## Acknowledgments

We are thankful to the amazing open-sourced LLMs and the tools used in our RS-Agent for releasing their models and code as open-source contributions.

## License

Apache-2.0 License. See [LICENSE](LICENSE) for details. DualRAG fork inherits LightRAG's MIT license (see `dualrag/LICENSE`).