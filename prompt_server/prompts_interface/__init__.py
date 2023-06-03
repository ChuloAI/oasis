from andromeda_chain import AndromedaPrompt

"""Used only for type annotation purposes."""
class PromptModuleInterface:
    function_doc_string_guidance_prompt: AndromedaPrompt
    doc_string_guidance_prompt: AndromedaPrompt
    ADD_TYPE_HINTS: AndromedaPrompt
    CUSTOM_PROMPT: AndromedaPrompt
    FIX_SYNTAX_ERROR: AndromedaPrompt