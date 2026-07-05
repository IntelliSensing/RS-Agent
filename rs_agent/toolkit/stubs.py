"""Stub tool implementations for task planning evaluation."""

from __future__ import annotations

from langchain.tools import Tool


def _stub(message: str):
    def _fn(*_args, **_kwargs) -> str:
        return message

    return _fn


STUB_TOOLS: list[Tool] = [
    Tool(
        name="super_resolution_2x",
        func=_stub("The image has been super-resolutioned."),
        description=(
            "Useful for super-resolution processing on an image. "
            "Input should be the image path."
        ),
    ),
    Tool(
        name="denoising",
        func=_stub("The image has been denoised."),
        description=(
            "Useful for denoise processing on an image. "
            "Input should be the image path."
        ),
    ),
    Tool(
        name="caption",
        func=_stub("The image shows a busy airport."),
        description=(
            "Useful when you want to know what is inside the photo. "
            "Input should be the image path."
        ),
    ),
    Tool(
        name="optical_detection",
        func=_stub("The detection on this optical image has done."),
        description=(
            "Useful for detecting and counting targets in optical images. "
            "Input should be the image path."
        ),
    ),
    Tool(
        name="optical_plane_type",
        func=_stub("The plane type in this optical image is Boeing 747."),
        description=(
            "Useful for determining the plane type in an optical image. "
            "Input should be the image path."
        ),
    ),
    Tool(
        name="scene",
        func=_stub("The scene of this image is airport."),
        description=(
            "Useful for answering which scene the picture shows. "
            "Input should be the image path."
        ),
    ),
    Tool(
        name="sar_detection",
        func=_stub("The detection on this SAR image has done."),
        description=(
            "Useful for detecting and counting targets in SAR images. "
            "Input should be the image path."
        ),
    ),
    Tool(
        name="sar_plane_type",
        func=_stub("The plane type in this SAR image is Boeing 747."),
        description=(
            "Useful for determining the plane type in a SAR image. "
            "Input should be the image path."
        ),
    ),
    Tool(
        name="knowledge_search",
        func=_stub("Sorry, I have no idea about this question."),
        description=(
            "Useful for information about a specific plane or aircraft. "
            "Input should be an English query."
        ),
    ),
    Tool(
        name="building_damage_detection",
        func=_stub("The building damage detection on this image has done."),
        description=(
            "Useful for assessing building damage after a disaster. "
            "Input should be the image path."
        ),
    ),
    Tool(
        name="building_extraction",
        func=_stub("The buildings in this image have been extracted."),
        description=(
            "Useful for extracting buildings from the image. "
            "Input should be the image path."
        ),
    ),
    Tool(
        name="road_extraction",
        func=_stub("The roads in this image have been extracted."),
        description=(
            "Useful for extracting roads from the image. "
            "Input should be the image path."
        ),
    ),
    Tool(
        name="horizontal_object_detection",
        func=_stub("The horizontal object detection on this image has done."),
        description=(
            "Useful for detecting objects with horizontally aligned bounding boxes. "
            "Input should be the image path."
        ),
    ),
    Tool(
        name="rotated_object_detection",
        func=_stub("The rotated object detection on this image has done."),
        description=(
            "Useful for rotated object detection in an image. "
            "Input should be the image path."
        ),
    ),
    Tool(
        name="semantic_segmentation",
        func=_stub("The semantic segmentation on this image has done."),
        description=(
            "Useful for semantic segmentation or pixel-wise classification. "
            "Input should be the image path."
        ),
    ),
    Tool(
        name="land_use_classification",
        func=_stub("The land use classification on this image has done."),
        description=(
            "Useful for land cover or land use classification. "
            "Input should be the image path."
        ),
    ),
    Tool(
        name="image_dehazing",
        func=_stub("The haze in this image has been removed."),
        description=(
            "Useful for image dehazing. Input should be the image path."
        ),
    ),
    Tool(
        name="cloud_removal",
        func=_stub("The cloud in this image has been removed."),
        description=(
            "Useful for cloud removal. Input should be the image path."
        ),
    ),
]
