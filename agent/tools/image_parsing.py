"""Image parsing and editing tools using Gemini vision."""

from typing import Optional, Dict, Any, Union
from pathlib import Path
import google.generativeai as genai
from PIL import Image
import io
import json

from config import config


def setup_gemini():
    """Configure Gemini API."""
    genai.configure(api_key=config.GOOGLE_API_KEY)


def parse_graph_from_image(image_input: Union[str, Path, bytes, Image.Image]) -> Dict[str, Any]:
    """Extract graph structure from an image using Gemini vision.
    
    Args:
        image_input: Image as file path, bytes, or PIL Image
        
    Returns:
        Dictionary containing:
            - adjacency_list: Extracted graph structure
            - description: Text description of the graph
            - confidence: Confidence level of the extraction
            
    Raises:
        ValueError: If image parsing fails
    """
    setup_gemini()
    
    # Load image
    if isinstance(image_input, (str, Path)):
        image = Image.open(image_input)
    elif isinstance(image_input, bytes):
        image = Image.open(io.BytesIO(image_input))
    elif isinstance(image_input, Image.Image):
        image = image_input
    else:
        raise ValueError(f"Unsupported image input type: {type(image_input)}")
    
    # Create model
    model = genai.GenerativeModel(config.GEMINI_VISION_MODEL)
    
    # Prompt for graph extraction
    prompt = """Analyze this graph image and extract its structure.

Please provide:
1. A list of all nodes (vertices) you can identify
2. A list of all edges (connections) between nodes
3. A brief description of the graph structure

Format your response as JSON with the following structure:
{
    "nodes": ["A", "B", "C", ...],
    "edges": [["A", "B"], ["B", "C"], ...],
    "description": "Brief description of the graph",
    "properties": {
        "appears_to_be": "type of graph (e.g., tree, cycle, complete, etc.)",
        "num_nodes": <count>,
        "num_edges": <count>
    }
}

Be as accurate as possible in identifying nodes and edges. If node labels are not clearly visible, use generic labels like "Node1", "Node2", etc.
"""
    
    try:
        response = model.generate_content([prompt, image])
        
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Try to find JSON in the response
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            json_text = response_text[json_start:json_end].strip()
        elif "{" in response_text:
            # Find the JSON object
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            json_text = response_text[json_start:json_end]
        else:
            raise ValueError("Could not find JSON in Gemini response")
        
        parsed_data = json.loads(json_text)
        
        # Convert to adjacency list format
        adjacency_list = {}
        nodes = parsed_data.get("nodes", [])
        edges = parsed_data.get("edges", [])
        
        # Initialize all nodes
        for node in nodes:
            adjacency_list[str(node)] = []
        
        # Add edges
        for edge in edges:
            if len(edge) >= 2:
                node1, node2 = str(edge[0]), str(edge[1])
                if node1 in adjacency_list:
                    adjacency_list[node1].append(node2)
                if node2 in adjacency_list:
                    adjacency_list[node2].append(node1)
        
        return {
            "adjacency_list": adjacency_list,
            "description": parsed_data.get("description", "Graph extracted from image"),
            "properties": parsed_data.get("properties", {}),
            "confidence": "high" if len(nodes) > 0 else "low",
        }
        
    except Exception as e:
        raise ValueError(f"Failed to parse graph from image: {str(e)}")


def annotate_graph_image(
    image_input: Union[str, Path, Image.Image],
    annotation_request: str,
    save_path: Optional[Path] = None
) -> Dict[str, Any]:
    """Use Gemini to describe how to annotate a graph image.
    
    Note: This provides textual instructions for annotation. Actual image 
    editing would require additional image manipulation libraries.
    
    Args:
        image_input: Original graph image
        annotation_request: Description of what to annotate or highlight
        save_path: Optional path to save annotated image
        
    Returns:
        Dictionary with annotation instructions and description
    """
    setup_gemini()
    
    # Load image
    if isinstance(image_input, (str, Path)):
        image = Image.open(image_input)
    elif isinstance(image_input, Image.Image):
        image = image_input
    else:
        raise ValueError(f"Unsupported image input type: {type(image_input)}")
    
    # Create model
    model = genai.GenerativeModel(config.GEMINI_VISION_MODEL)
    
    prompt = f"""Analyze this graph image and provide instructions for the following annotation request:

Request: {annotation_request}

Please provide:
1. Which specific nodes or edges should be highlighted
2. What colors or visual indicators should be used
3. Any labels or text that should be added
4. A description of the annotated result

Format as JSON:
{{
    "elements_to_highlight": {{
        "nodes": ["list", "of", "nodes"],
        "edges": [["node1", "node2"], ...],
    }},
    "visual_instructions": {{
        "node_color": "color for highlighted nodes",
        "edge_color": "color for highlighted edges",
        "labels": {{"node_id": "label text"}},
    }},
    "description": "Description of what the annotation shows"
}}
"""
    
    try:
        response = model.generate_content([prompt, image])
        response_text = response.text.strip()
        
        # Extract JSON
        if "```json" in response_text:
            json_start = response_text.find("```json") + 7
            json_end = response_text.find("```", json_start)
            json_text = response_text[json_start:json_end].strip()
        elif "{" in response_text:
            json_start = response_text.find("{")
            json_end = response_text.rfind("}") + 1
            json_text = response_text[json_start:json_end]
        else:
            # Return raw text if JSON parsing fails
            return {
                "raw_instructions": response_text,
                "description": annotation_request,
            }
        
        parsed_instructions = json.loads(json_text)
        return parsed_instructions
        
    except Exception as e:
        return {
            "error": str(e),
            "description": f"Failed to generate annotation instructions: {annotation_request}",
        }


def describe_graph_image(image_input: Union[str, Path, Image.Image]) -> str:
    """Get a natural language description of a graph image.
    
    Args:
        image_input: Graph image to describe
        
    Returns:
        Text description of the graph
    """
    setup_gemini()
    
    # Load image
    if isinstance(image_input, (str, Path)):
        image = Image.open(image_input)
    elif isinstance(image_input, Image.Image):
        image = image_input
    else:
        raise ValueError(f"Unsupported image input type: {type(image_input)}")
    
    model = genai.GenerativeModel(config.GEMINI_VISION_MODEL)
    
    prompt = """Describe this graph in detail. Include:
- The number of nodes and edges you can see
- The overall structure (tree, cycle, complete graph, etc.)
- Any patterns or special properties you notice
- Whether it appears to be a specific type of graph (bipartite, planar, regular, etc.)
- Any colorings or labelings present

Provide a clear, concise description suitable for someone who cannot see the image."""
    
    try:
        response = model.generate_content([prompt, image])
        return response.text.strip()
    except Exception as e:
        return f"Failed to describe image: {str(e)}"
