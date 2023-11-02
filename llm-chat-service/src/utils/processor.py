
from fastapi import HTTPException
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
        self.reduce_template = """The following is set of summaries:
        {doc_summaries}
        Take these and distill it into a final, consolidated summary of the main themes in more than 150 but less than 350 words. 
        Helpful Answer:"""
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

  
    def processing(username: str, project_name: str, directory_path: str, query: str):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
        documents = []
        for ext in FILE_EXTENSIONS:
            documents += DirectoryLoader(
                directory_path,
                glob=f"**/*.{ext}",
                recursive=True,
                use_multithreading=True,
                loader_cls=TextLoader,
                silent_errors=True,
                loader_kwargs={"autodetect_encoding": True},
                show_progress=False,
            ).load()

        embeddings = OpenAIEmbeddings()
        vectorized_docs = [embeddings.embed(doc) for doc in documents]
        qdrant = Qdrant.from_documents(vectorized_docs, embeddings,url= QDRANT_URL, collection_name=f"{username}-{project_name}")
        top_5_results = qdrant.similarity_search(query, k=5)
       
        content_list = [result['page_content'] for result in top_5_results]

        
        split_docs = text_splitter.split_documents(content_list)
        map_result = self.map_chain.run(split_docs)
        
        doc_summaries_dict = {'doc_summaries': map_result}
        
       
        summary = self.reduce_chain.run(doc_summaries_dict)

        return summary
    
    
    