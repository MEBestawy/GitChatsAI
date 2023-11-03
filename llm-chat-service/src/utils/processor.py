
from fastapi import HTTPException
from qdrant_client import QdrantClient
from config import FILE_EXTENSIONS, QDRANT_URL
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.qdrant import Qdrant
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import ReduceDocumentsChain, MapReduceDocumentsChain
from langchain.text_splitter import RecursiveCharacterTextSplitter



class gitProcessor:

    def __init__(self):
       
        self.llm = ChatOpenAI(temperature=0)
        self.map_template = """The following is a set of documents
          {docs}
            Based on this list of docs, please identify the main themes 
            Helpful Answer:"""
        self.map_prompt = PromptTemplate.from_template(self.map_template)
        self.map_chain = LLMChain(llm=self.llm, prompt=self.map_prompt)
        self.reduce_template = """
    You are an assistant that specializes in software engineering, tasked with analyzing a code repository. You will be given a question regarding a codebase and you should answer it given the available context documents.
    Any mention of this project/repo/codebase/etc... refers to the {project_name} repo.
    
    Keep your answer under 100 words.
    If you are unsure, then prefix your answer with "I am not sure, "
    QUESTION: {query}

    CONTEXT DOCUMENTS ABOUT PROJECT: {doc_summaries}
    
    ANSWER:"""
        self.reduce_prompt = PromptTemplate.from_template(self.reduce_template)
        self.reduce_chain = LLMChain(llm=self.llm, prompt=self.reduce_prompt)
        self.combine_documents_chain = StuffDocumentsChain(
            llm_chain=self.reduce_chain, document_variable_name="doc_summaries"
        )
        self.reduce_documents_chain = ReduceDocumentsChain(
            combine_documents_chain=self.combine_documents_chain,
            collapse_documents_chain=self.combine_documents_chain,
            token_max=4000,
        )
        self.map_reduce_chain = MapReduceDocumentsChain(
            llm_chain=self.map_chain,
            reduce_documents_chain=self.reduce_documents_chain,
            document_variable_name="docs",
            return_intermediate_steps=False,
        )

  
    def processing(self, collection_name: str, query: str):
        embeddings = OpenAIEmbeddings()
        client = QdrantClient(url=QDRANT_URL)
        qdrant = Qdrant(client, collection_name, embeddings)
        top_5_results = qdrant.similarity_search(query, k=2)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
        split_docs = text_splitter.split_documents(top_5_results)
        map_result = self.map_chain.run(split_docs)
        doc_summaries_dict = {'doc_summaries': map_result}
        summary = self.reduce_chain.run(
            doc_summaries=doc_summaries_dict,
            query=query,
            project_name=collection_name
        )

        return {"message": summary}
    
    
    