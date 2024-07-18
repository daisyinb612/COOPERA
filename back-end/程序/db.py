from langchain_community.document_loaders import PyPDFLoader,TextLoader,UnstructuredWordDocumentLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.vectorstores import Chroma
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from llama_index.core.schema import NodeWithScore, QueryBundle, TextNode
import os
from index import FileIndex
class DB(object):
    def __init__(self) -> None:
        self.embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
        self.reranker = FlagEmbeddingReranker(
            top_n=3,
            model="BAAI/bge-reranker-large",
            use_fp16=False
        )
        self.fileindex = FileIndex()

    def do_split(self,file,chunk_size=100,chunk_overlap=30):
        if file.endswith(".txt"):
           loader = TextLoader(file, encoding='utf-8')
        elif file.endswith(".pdf"):
           loader = PyPDFLoader(file)
        elif file.endswith(".docx"):
            loader = UnstructuredWordDocumentLoader(file)
        else:
            loader = None
        if loader:
            pages = loader.load_and_split()
            text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len
            )
            text = text_splitter.split_documents(pages)
            print("切分完毕")
            print(text)
            return text
        else:
            print("file type error")
            return None

    def creat_db_empty(self,savepath) -> None:
        vectorstore = Chroma(embedding_function=self.embeddings,persist_directory=savepath)
        print("已创建空向量数据库")

    def creat_db(self,savepath,source) -> None:
        files = [os.path.join(source, file) for file in os.listdir(source)]
        for file in files:
            print(file)
            text = self.do_split(file)
            vectorstore = Chroma.from_documents(
                documents=text,
                embedding=self.embeddings,
                persist_directory=savepath,
            )
            print("成功转换为向量数据库数据的条目数："+str(vectorstore._collection.count()))

    def add_file(self,filepath,savepath) -> None:
        vectorstore = Chroma(embedding_function=self.embeddings,persist_directory=savepath)
        text = self.do_split(filepath)
        result = vectorstore.add_documents(documents=text)
        print(result)
        print("成功添加")
        self.fileindex.add_file(filename=os.path.basename(filepath),file_list=result)
    
    def delete_file_from_db(self,savepath,filename):
        vectorstore = Chroma(embedding_function=self.embeddings,persist_directory=savepath)
        list = self.fileindex.get_list(filename)
        vectorstore.delete(list)
        print(list)
        print("成功删除")

    def search_from_db(self,savepath,question) -> str:
        vectorstore = Chroma(embedding_function=self.embeddings,persist_directory=savepath)
        search_result = vectorstore.similarity_search(question, k=3)
        reranker_text = []
        for i in range(3):
            reranker_text.append(search_result[i].page_content)
        nodes = [NodeWithScore(node=TextNode(text=doc)) for doc in reranker_text]
        query_bundle = QueryBundle(query_str=question)
        ranked_nodes = self.reranker._postprocess_nodes(nodes, query_bundle)
        for node in ranked_nodes:
            print(node.node.get_content(), "-> Score:", node.score)
        #print(ranked_nodes)
        def get_score(item):
            return item.score
        ranked_nodes.sort(key=get_score, reverse=True)
        #print(ranked_nodes)
        print("最高相关的语料为："+ranked_nodes[0].node.get_content())
        return ranked_nodes[0].node.get_content()

    def get_world_setting(self,filepath="./剧本信息/世界观设定/1.txt"):
        with open(filepath,"r",encoding="utf-8") as f:
            data = f.read()
            print(data)
            f.close()
            return "###世界观设定###："+data
'''    
d = DB()
#d.creat_db(source="./剧本信息/世界观设定",savepath="./向量数据库/已完成的语料")
#d.search_from_db(savepath="./向量数据库/已完成的语料",question="地球遭受了名为什么的灾难")
#d.delete_file_from_db(savepath="./向量数据库/已完成的语料")
d.creat_db_empty(savepath="./向量数据库/已完成的语料")
d.add_file(filepath="./剧本信息/世界观设定/1.txt",savepath="./向量数据库/已完成的语料")'''