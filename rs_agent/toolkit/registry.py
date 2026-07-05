"""Tool registry for RS-Agent."""

from __future__ import annotations

from langchain.tools import Tool

from rs_agent.toolkit.stubs import STUB_TOOLS, _stub

# Mapping from task type to expected first tool (for planning evaluation)
TASK_TO_TOOL: dict[str, str] = {
    "Super_Resolution": "super_resolution_2x",
    "Denoising": "denoising",
    "Captioning": "caption",
    "Optical_Detection": "optical_detection",
    "Optical_Plane_Type": "optical_plane_type",
    "Scene_Classification": "scene",
    "SAR_Detection": "sar_detection",
    "SAR_Plane_Type": "sar_plane_type",
    "Knowledge_Search": "knowledge_search",
    "Building_Damage_Detection": "building_damage_detection",
    "Building_Extraction": "building_extraction",
    "Road_Extraction": "road_extraction",
    "Horizontal_Object_Detection": "horizontal_object_detection",
    "Rotated_Object_Detection": "rotated_object_detection",
    "Semantic_Segmentation": "semantic_segmentation",
    "Land_Use_Classification": "land_use_classification",
    "Image_Dehazing": "image_dehazing",
    "Cloud_Removal": "cloud_removal",
}

TASK_TO_TOOL_RSCHATGPT: dict[str, str] = {
    "Object_Counting": "count_text",
    "Object_Detection": "detection",
    "Landuse_Segmentation": "landuse_Segmentation",
    "Instance_Segmentation": "Instance_Segmentation",
    "Edge_Detection": "EdgeDetection",
    "Image_Caption": "Caption",
    "Scene_Classification": "Scene",
}

RSCHATGPT_STUB_TOOLS: list[Tool] = [
    Tool(
        name="count_text",
        func=_stub("Counted 3 objects."),
        description="Count objects in an image. Input: target name and image path.",
    ),
    Tool(
        name="detection",
        func=_stub("Detection complete."),
        description="Detect bounding boxes. Input: target name and image path.",
    ),
    Tool(
        name="landuse_Segmentation",
        func=_stub("Landuse segmentation complete."),
        description="Apply land use segmentation. Input: landuse type and image path.",
    ),
    Tool(
        name="Instance_Segmentation",
        func=_stub("Instance segmentation complete."),
        description="Apply instance segmentation. Input: target name and image path.",
    ),
    Tool(
        name="EdgeDetection",
        func=_stub("Edge detection complete."),
        description="Detect edges in an image. Input: image path.",
    ),
    Tool(
        name="Caption",
        func=_stub("The image shows an airport with several planes."),
        description="Caption an image. Input: image path.",
    ),
    Tool(
        name="Scene",
        func=_stub("The scene is airport."),
        description="Classify scene type. Input: image path.",
    ),
]


def get_stub_tools(toolkit: str = "rsagent") -> list[Tool]:
    """Return stub tools for planning evaluation."""
    if toolkit == "rschatgpt":
        return list(RSCHATGPT_STUB_TOOLS)
    return list(STUB_TOOLS)
