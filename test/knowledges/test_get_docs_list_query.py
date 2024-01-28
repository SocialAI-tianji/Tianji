import tianji.utils.knowledge_tool as knowledgetool
from dotenv import load_dotenv

load_dotenv()

# KNOWLEDGE_PATH = r"D:\1-wsl\TIANJI\Tianji\tianji\knowledges\04-Wishes\knowledges.txt"
# SAVE_PATH = r"D:\1-wsl\TIANJI\Tianji\temp"

KNOWLEDGE_PATH = r"/Users/fengzetao/Workspace/Github/SocialAI/Tianji/tianji/knowledges/04-Wishes/knowledges.txt"
SAVE_PATH = r"/Users/fengzetao/Workspace/Github/SocialAI/Tianji/temp"

# doclist = knowledgetool.get_docs_list_query_openai(query_str="春节",loader_file_path=KNOWLEDGE_PATH, \
#                                   persist_directory = SAVE_PATH,k_num=5)

doclist = knowledgetool.get_docs_list_query_zhipuai(
    query_str="春节",
    loader_file_path=KNOWLEDGE_PATH,
    persist_directory=SAVE_PATH,
    k_num=5,
)

if doclist is not []:
    print(doclist)
else:
    print("doclist is [] !")
