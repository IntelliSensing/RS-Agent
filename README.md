<h1 align="center"> RS-Agent: An LLM-driven Remote Sensing Intelligent Agent </h1> 

<p align="center">
  <a href="http://wenjia.ruantang.top/">Wenjia Xu</a><sup>*</sup>, 
  <a href="https://scholar.google.com/citations?user=iZ3TxmoAAAAJ">Zijian Yu</a><sup>*</sup>, 
  <a href="https://sites.google.com/site/">Boyang Mu</a>, 
  <a href="https://trentonwei.github.io/">Zhiwei Wei</a>, 
  <a href="https://sites.google.com/site/">Yuanben Zhang</a>, 
  <a href="https://jiuniu.ruantang.top/">Jiuniu Wang</a> and 
  <a href="https://scholar.google.com/citations?user=85mAZVcAAAAJ&hl">Mugen Peng</a>
  <br><sup>*</sup> Equal Contribution
</p>

<figure>
<div align="center">
<img src=images/Agent-logo.png width="15%">
</figure>


<p align="center">
  <a href="https://intellisensing.github.io/RS-Agent/">
    <img src="https://img.shields.io/badge/Project-Website-87CEEB" alt="Website">
  </a>
  <a href="https://arxiv.org/abs/2406.07089">
    <img src="https://img.shields.io/badge/arXiv-Paper-red.svg" alt="Paper">
  </a>
  <a href="https://youtu.be/KOKtkkKpNDk">
    <img src="https://img.shields.io/badge/Video-Presentation-F9D371" alt="Video">
  </a>
</p>


<p align="center">
  <a href="#introduction">Introduction</a> |
  <a href="#core components">Core Components</a> |
  <a href="#Supported Function">Supported Function</a> |
  <a href="#Qualitative Results">Qualitative Results</a> |
  <a href="#Contributions">Contributions</a> | 
  <a href="#acknowledgments">Acknowledgements</a> 
</p>

    
## <a id="introduction"></a>Introduction

Recent advancements in Large Language Models (LLMs) and Multi-modal Large Language Models (MLLMs) have led to impressive performance in remote sensing tasks. However, these models are limited to basic vision and language tasks and lack specialized expertise for complex remote sensing applications. To address these, we propose **RS-Agent**, an intelligent agent for remote sensing. RS-Agent is powered by an LLM as its "Central Controller," enabling it to understand and respond to various problems. It integrates high-performance remote sensing image processing tools, allowing multi-tool, multi-turn conversations for complex tasks. Additionally, RS-Agent utilizes a knowledge graph-enhanced Retrieval-Augmented Generation (RAG) framework to access domain-specific knowledge, ensuring accurate responses to expert-level queries. Experimental results show RS-Agent achieves over 95% task planning accuracy and demonstrates strong domain-specific knowledge retrieval, excelling across various tasks.

<figure>
<div align="center">
<img src=images/teaser_figure.png width="50%">
</div>
</figure>

## <a id="core components"></a>Core Components

1. **Central Controller**: Serves as the decision-making core of the agent. It interprets user queries, plans task execution, manages dialogue history, and synthesizes final responses.

2. **Toolkit**: A collection of state-of-the-art remote sensing tools for various applications. These tools are invoked based on the Central Controller’s planning.
   
3. **Solution Space**: Stores predefined expert-level task solutions. It guides the Controller in selecting appropriate tools and execution strategies by retrieving relevant task-specific instructions.
   
4. **Knowledge Space**: Provides domain-specific information via a curated knowledge database. It supports expert-level reasoning by retrieving relevant content.
<figure>
<div align="center">
<img src=images/method.png width="100%">
</figure>

## <a id="Supported Function"></a>Supported Function

| Tool                                  | Function                                            | Example Input                                        |
|:-------------------------------------:|:---------------------------------------------------:|:-----------------------------------------------------:|
| cloud_removal      | Cloud removal from satellite images                 | Remove the clouds in this image.                     |
| image_dehazing | Haze removal from images                            | Dehaze this foggy image.                             |
| super_resolution    | Image super-resolution (2×)                         | Enhance the resolution of this image.                |
| denoising      | Image denoising                                    | Remove noise from this image.                        |
| caption     | Geo-specific VQA and captioning                     | What is in this remote sensing image?                |
| optical_detection  | Optical image target detection                      | Detect objects in this optical image.                |
| optical_plane_type                    | Aircraft type recognition in optical images         | What type of aircraft is in this image?             |
| scene                                 | Scene classification                                | What is the scene category of this image?           |
| sar_detection| Target detection in SAR images                      | Find the objects in this SAR image.                  |
| sar_plane_type                        | Aircraft type recognition in SAR images             | Identify the aircraft in this SAR image.            |
| knowledge_search                      | Aircraft info retrieval via Knowledge Database      | Who manufactures Boeing 747?                         |
| building_damage_detection | Building damage assessment                    | Which buildings are damaged?                         |
| building_extraction| Building extraction from images                     | Extract all buildings from the image.                |
| road_extraction | Road extraction from images                         | Extract roads from the scene.                        |
| horizontal_object_detection | Horizontal bounding box detection              | Detect objects using horizontal boxes.               |
| rotated_object_detection  | Rotated object detection                         | Detect objects using rotated boxes.                  |
| semantic_segmentation | Pixel-wise semantic segmentation                    | Segment the different regions in this image.         |
| land_use_classification | Land use categorization                         | What are the land use types in this image?           |

## <a id="Qualitative Results"></a>Qualitative Results
<figure>
<div align="center">
<img src=images/qualititive_result.png width="100%">
</div>
</figure>

## <a id="Contributions"></a>🏆 Contributions

1. We present RS-Agent, a novel architecture designed to interpret user queries and orchestrate diverse tools for accurate and efficient remote sensing task execution. Its four core components—Central Controller, Toolkits, Solution Space, and Knowledge Space—work in concert, seamlessly interacting and complementing one another to enable robust, adaptive performance across a wide range of applications.

2. To enhance the agent’s task planning accuracy, we propose an innovative Task-Aware Retrieval method. By retrieving and understanding expert-level task solutions, RS-Agent is able to emulate the decision-making and tool selection processes of professional remote sensing analysts.

3. To strengthen RS-Agent’s domain-specific knowledge, we propose DualRAG, a retrieval augmented generation method that assigns weights to extracted keywords and performs dual path retrieval, thereby enhancing the accuracy and relevance of knowledge retrieval.

4. Extensive experiments demonstrate that RS-Agent consistently surpasses previous SOTA Multimodal Large Language Models across a range of remote sensing applications, and significantly boosts the task planning accuracy. These results establish RS-Agent as a major step forward in adapting AI agents to the remote sensing field, and, for the first time, present a comprehensive and modular architecture tailored for remote sensing applications.



## <a id="acknowledgments"></a>Acknowledgments

We thank the developers of the datasets and tools used in our experiments.

---
