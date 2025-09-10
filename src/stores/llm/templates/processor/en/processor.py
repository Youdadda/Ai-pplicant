from string import Template


## ======= System prompt to prcoess the job posting

system_prompt = Template("\n".join([
    'You are an assistant that extracts structured job information from raw text.',
    'Extract:',
    '- Job Title',
    '- Company Name',
    '- Skills (as a list)',
    '- Recruiter Email (if present)',
    'Return only valid JSON in this format:',
    '{',
    "\"title\": \"...\",",
    "\"company\": \"...\",",
  "\"skills\": [\"...\", \"...\", \"...\"],",
    "\"recruiter_email\": \"...\"",
    '}',

]))

footer_prompt = Template("\n".join([
    "Following the instructions you were provided with above, extaract the demanded informations from the following document: .",
    "## Document:",
    "$document",
    "",
    "## Answer:",
]))