from tianji.knowledges.script.demo import model_center

if __name__ == "__main__":
    model = model_center()
    question = "如何给长辈敬酒？"
    chat_history = []
    _, response = model.qa_chain_self_answer(question, chat_history)
    print(response)