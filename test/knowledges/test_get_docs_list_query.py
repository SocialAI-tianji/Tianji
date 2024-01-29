import tianji.utils.knowledge_tool as knowledgetool
from tianji.knowledges.config import KNOWLEDGE_PATH, EMBEDDING_PATH
from dotenv import load_dotenv

load_dotenv()

# KNOWLEDGE_PATH = r"D:\1-wsl\TIANJI\Tianji\tianji\knowledges\04-Wishes\knowledges.txt"
# SAVE_PATH = r"D:\1-wsl\TIANJI\Tianji\temp"

# doclist = knowledgetool.get_docs_list_query_openai(query_str="春节",loader_file_path=KNOWLEDGE_PATH, \
#                                   persist_directory = SAVE_PATH,k_num=5)

doclist = knowledgetool.get_docs_list_query_openai(
    query_str="春节",
    loader_file_path=KNOWLEDGE_PATH.WISHES.path(),
    persist_directory=EMBEDDING_PATH.WISHES.path(filename="openai"),
    k_num=5,
)

if doclist is not []:
    print(doclist)
else:
    print("doclist is [] !")
