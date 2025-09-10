from string import Template


## ======= System prompt to prcoess the job posting

system_prompt = Template("\n".join([
    'Vous êtes un assistant qui extrait des informations d’emploi structurées à partir de texte brut.',
    'Extrayez :',
    '- Titre du poste',
    '- Nom de l\'entreprise',
    '- Compétences (sous forme de liste)',
    '- E-mail du recruteur (si présent)',
    'Retournez uniquement du JSON valide dans ce format :',
    '{',
    "\"title\": \"...\",",
    "\"company\": \"...\",",
    "\"skills\": [\"...\", \"...\", \"...\"],",
    "\"recruiter_email\": \"...\"",
    '}',
]))