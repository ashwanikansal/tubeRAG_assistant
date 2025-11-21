from langchain_core.prompts import PromptTemplate

def get_default_prompt() -> PromptTemplate:
    """
    Prompt that restricts answers to transcript context.
    """
    print("Generating prompt...")
    return PromptTemplate(
        template="""
            You are a helpful assistant.
            Answer ONLY from the provided transcript context.
            If the context is insufficient, just say you don't know.

            Context:
            {context}

            Question: {question}
            """.strip(),
        input_variables=["context", "question"],
    )
