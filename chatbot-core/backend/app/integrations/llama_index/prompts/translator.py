from llama_index.core.prompts import PromptTemplate


TRANSLATOR_PROMPT_TMPL = PromptTemplate(
    template="""\
Translate the following documents from {source_language} to {target_language}:
'''
{document}
'''
"""
)
