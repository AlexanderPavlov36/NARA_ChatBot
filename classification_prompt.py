classification_prompt = """
Classify the type of user request. Reply with only one word:
- "question": if this is a question that needs an answer;
- "show_records": if the user is directly asking to display, list, show, etc.
archival materials/documents/full texts/records/sources.

If the request does NOT explicitly ask to display, list, show, etc., classify as
"question".

Examples:

Request: Why is the sky blue?
Output: question

Request: Show me documents about politics.
Output: show_records

Request: List the sources.
Output: show_records

Request: Give me all related documents.
Output: show_records

Request: Who was president in 1952?
Output: question
"""