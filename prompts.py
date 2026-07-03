# prompts.py

PARSER_PROMPT = """
You are an expert hematology assistant.

Your task is to extract ALL information from the following CBC report.

Requirements:

1. Return ONLY valid JSON.
2. Do NOT explain anything.
3. Do NOT wrap the JSON inside markdown.
4. Preserve numeric values exactly.
5. Preserve units.
6. If a value is missing, use null.

Report:

{report}
"""


VALIDATOR_PROMPT = """
You are an expert laboratory validator.

Compare the ORIGINAL CBC report with the extracted JSON.

Report:

{report}

Extracted JSON:

{json_data}

Verify:

- Missing values
- Incorrect values
- Missing tests
- Incorrect units
- Hallucinated information

Return a concise validation report.
"""


SUMMARY_PROMPT = """
You are an experienced hematologist.

Based ONLY on the CBC report below, provide a concise medical summary.

Report:

{report}

Extracted JSON:

{json_data}

Requirements:

- Mention abnormal findings.
- Mention possible clinical significance.
- Keep it under 200 words.
- Do not invent information.
"""
