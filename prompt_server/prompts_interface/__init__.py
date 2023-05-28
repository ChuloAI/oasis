from guidance_prompt import GuidancePrompt

"""Used only for type annotation purposes."""
class PromptModuleInterface:
    doc_string_guidance_prompt: GuidancePrompt
    ADD_TYPE_HINTS: GuidancePrompt
    CUSTOM_PROMPT: GuidancePrompt
    FIX_SYNTAX_ERROR: GuidancePrompt