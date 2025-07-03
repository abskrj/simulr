from ..models.response_models import Example
from typing import List

def get_example_structures() -> List[Example]:
    """Return pre-built example structures"""
    
    return [
        Example(
            id="simple_truss",
            title="Simple Truss Bridge",
            prompt="steel rod stress on truss bridge",
            complexity="simple"
        ),
        Example(
            id="cantilever_beam",
            title="Cantilever Beam",
            prompt="cantilever beam with point load at the end",
            complexity="simple"
        ),
        Example(
            id="simply_supported_beam",
            title="Simply Supported Beam",
            prompt="simply supported steel beam with distributed load",
            complexity="simple"
        ),
        Example(
            id="frame_structure",
            title="Steel Frame Building",
            prompt="steel frame building with wind load analysis",
            complexity="medium"
        ),
        Example(
            id="suspension_bridge",
            title="Suspension Bridge",
            prompt="suspension bridge like golden gate bridge with cable analysis",
            complexity="high"
        ),
        Example(
            id="truss_tower",
            title="Communication Tower",
            prompt="steel truss communication tower with wind loads",
            complexity="medium"
        ),
        Example(
            id="arch_bridge",
            title="Arch Bridge",
            prompt="concrete arch bridge with vehicle loads",
            complexity="medium"
        ),
        Example(
            id="skyscraper",
            title="High-Rise Building",
            prompt="skyscraper structure like burj khalifa with seismic analysis",
            complexity="high"
        )
    ] 