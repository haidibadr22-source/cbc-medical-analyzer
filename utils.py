# utils.py

import fitz  # PyMuPDF
import json
import os
import re
import tempfile
from typing import Dict, Any


# ==========================================================
# Read PDF
# ==========================================================

def read_pdf(pdf_path: str) -> str:
    """
    Read all text from a PDF file.

    Parameters
    ----------
    pdf_path : str
        Path to PDF file.

    Returns
    -------
    str
        Extracted text.
    """

    document = fitz.open(pdf_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text.strip()


# ==========================================================
# Clean LLM JSON
# ==========================================================

def clean_json_response(response: str) -> Dict[str, Any]:
    """
    Clean JSON returned by the LLM.

    Removes:

    ```json
    ...
    ```

    and converts it to a Python dictionary.
    """

    if not response:
        raise ValueError("LLM returned an empty response.")

    response = response.strip()

    # Remove markdown code fences
    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    # Extract only the JSON object
    match = re.search(r"\{.*\}", response, re.DOTALL)

    if not match:
        raise ValueError("No JSON object found in the LLM response.")

    return json.loads(match.group())


# ==========================================================
# Save JSON
# ==========================================================

def save_json(data: Dict[str, Any], filename: str) -> str:
    """
    Save dictionary as JSON.

    Returns the saved file path.
    """

    os.makedirs("outputs", exist_ok=True)

    path = os.path.join("outputs", filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )

    return path


# ==========================================================
# Temporary JSON
# ==========================================================

def save_temp_json(data: Dict[str, Any]) -> str:
    """
    Save JSON into a temporary file.

    Useful for returning downloadable files.
    """

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".json",
        mode="w",
        encoding="utf-8"
    )

    json.dump(
        data,
        temp,
        indent=4,
        ensure_ascii=False
    )

    temp.close()

    return temp.name


# ==========================================================
# Read JSON
# ==========================================================

def read_json(path: str) -> Dict[str, Any]:
    """
    Read a JSON file.
    """

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ==========================================================
# Delete File
# ==========================================================

def delete_file(path: str):
    """
    Delete a file if it exists.
    """

    if os.path.exists(path):
        os.remove(path)
