# Option 2: return a string (we use a raw LLM call for illustration)

from llama_index.llms import OpenAI
from llama_index.prompts import PromptTemplate
from llama_index.query_engine import CustomQueryEngine
from llama_index.retrievers import BaseRetriever
from llama_index.response_synthesizers import (
    get_response_synthesizer,
    BaseSynthesizer,
)
from utils.llm_utils.mdm_rules import mdm_rules

qa_prompt = PromptTemplate(
    "Analyze the patient information provided below:\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Consider the following Medical Decision Making (MDM) Rules:\n"
    "---------------------\n"
    f"{mdm_rules}\n"
    "---------------------\n"
    "Now, answer the query:\n"
    "Query:"
    "Answer: "
)


class RAGStringQueryEngine(CustomQueryEngine):
    """RAG String Query Engine."""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer
    llm: OpenAI
    qa_prompt: PromptTemplate

    def custom_query(self, query_str: str):
        nodes = self.retriever.retrieve(query_str)
        

        context_str = "\n\n".join([n.node.get_content() for n in nodes])
        response = self.llm.complete(
            qa_prompt.format(context_str=context_str, query_str=query_str)
        )

        return str(response)