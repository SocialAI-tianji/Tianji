# 如何从零搜集网络数据形成训练语料

本文中，我将会以人情世故大模型中涉及到的子任务 6.化解"尴尬"场合 Awkwardness 为例，带大家一起探索从指定题目到数据采集最后清洗、形成训练语料的全流程。

## 数据采集

首先我们需要掌握需要采集哪些数据，优质数据无非是视频、音频、书籍（其他文字被llm污染严重或者本来就没什么见解之处，所以无法作为数据参考。），

具体的方向可以参考最开始的场景细化：

[https://github.com/SocialAI-tianji/Tianji/tree/main/test/场景分类/06-Awkwardness](https://github.com/SocialAI-tianji/Tianji/tree/main/test/%E5%9C%BA%E6%99%AF%E5%88%86%E7%B1%BB/06-Awkwardness)

从标题即可知大概的数据范围，于是我们可以直接在靠谱信源搜索对应的数据源，随后进行数据的下载（video、pdf等），例如我可以直接搜索与“如何学会拒绝”、“对话时忘记对方名字怎么办？”、“如何破冰”、“如何打破沉默”、“如何接受别人的夸奖”、“如何回应别人的赞美”、“如何赞美别人”等资料，先统一下载搜集起来，然后统一视频、语音转文字。

此处工作你可以利用仓库中的下载工具帮助完成：https://github.com/SocialAI-tianji/Tianji/tree/main/tools/get_data

最后你将得到几十、几百甚至几千个txt文档，这些文档都是用来做下一步的数据清洗的。

## 数据清洗

由于当前数据采集后的结果长度比较短，不是那种大长文。故可以直接与llm交互进行知识的提取工作。

什么叫知识提取 ？简单来说就是陈述句的表达所有浓缩的内容，且恰好的分成几点，但不是总结。

比如我们有这个关于“如何拒绝”的语料 ：

```python
第一你得知道你自己的底线在哪儿。你比如说工作中我自己的底线是可以算成我的，也可以不算成我的我不拒绝。因为这件事情本身的判断就是模棱两可，所以当你要求我做的时候我会去做。然后如果遇到这个领导是明事理的，其他的有些活你让我干我会接受。但如果不明事理的领导跟我一点没关系，都没有的活我不干，对吧？所以不同的场景下，你得知道自己的底线在哪，这是学会拒绝的前提。因为拒绝不能瞎拒绝，对吧？

第二个一定要掌握有效拒绝的理由和方法。这个拒绝不能以伤害和破坏正常的人际关系。注意正常的不要追求极致融洽的人际关系，你只要追求极致融洽的人际关系，我就告诉你，你一定不会拒绝，对吧？你拒绝了就想，他怎么想他是不是不舒服、不开心，老板不高兴了，那最后他妈还不到你身上了。所以不要追求极最融洽的人际关系，就正常人际关系，我们也不是什么朋友，我们就正常的同事上下级的关系，对吧？你是不是喜欢我不重要，但是你离不开我，或者说在这个阶段你要继续用我。Ok在这个公司我觉得这个公司文化有问题，我现在之所以我还待着，就是因为外面市场不好，市场好了我会转身就走。但是只要我走之前的每一天，在职场中人际关系都是正常就ok。

所以你要做的是什么呢？就是在不破坏正常的人际关系的情况下，怎么样让对方能接受。所以这里头就要考虑核心在于你要给对方一个无法拒绝你拒绝的理由。什么叫无法拒绝？你拒绝的理由？最典型的在职场中就是我手里有好几项事情同时要做这些事情的重要性都比你的高，而且都有时间要求完成你的事情，我自己的本职工作就完不成了，这就叫让对方无法拒绝。你拒绝的理由，我只举个例子对吧？当然这个前提是要真实，那你这上班就打游戏对吧？
```

你可以利用这个提示词如下提示词可以得到对应的知识然后统一丢给知识库再QA处理（一次性完成两个任务）

```python
你是一个信息抽取的知识库语料准备能手，你需要把我给你的文章做成几个知识点，这个知识点类似问答对的回答（陈述句的描述,不需要提问，比如：苹果是一种水果，可以吃和烹饪，而且是红色的，长在大树上），你不需要分1、2、3、4点， 只需要把相关的知识都划分成一个段落就好，

```
例子如下，假设我首先发了这个文章：

在商务宴请中有一个很重要的礼仪，如果你忽视了，会让你的客户觉得你很没有分寸。大家都知道在饭桌上谈生意，往往会比在办公室正儿八经坐着谈成的几率会更大。在这其中当然离不开酒的路牢，所以在商务宴请中敬酒的礼仪是非常重要的。

敬酒时先给对方斟酒，然后再给自己斟酒。右手拿酒杯，左手托杯底。咱们的酒杯要比对方低一点，如果对方比较谦虚，放的比我们低，我们可以用左手轻轻的将对方的酒杯托起，这样会显得尊重。喝完酒为了表达咱们的诚意，我们可以用敬酒的手势把杯子微微倾斜，杯口朝向对方，不用再把杯子直接倒过来，会显得很不雅。大家在敬酒的时候呢，还有哪些注意事项呢？咱们可以留言一起讨论一下。

你的回答是富有内容、陈述句的、分细节方向的回复，如下作为一个整体：
商务宴请中，礼仪的遵循对于给客户留下良好印象至关重要，饭桌上的生意洽谈通常成功率较高。在敬酒环节，应优先为对方斟酒，随后再为自己斟，且需用右手持杯，左手托底。敬酒时，酒杯应保持低于对方酒杯，以示尊敬；若对方酒杯位置更低，可轻轻用左手托起对方酒杯。喝完酒后，应以敬酒手势将杯子微微倾斜，杯口朝向对方，避免直接倒转酒杯，以维持礼貌和风度。
```

接下来你帮我解析新的知识，你只需要回复这个新的知识文章相关的内容就好，不要回复例子的内容！文章如下：
```

你也可以利用下列提示词偷懒，直接一步到位从原文得到最后的QA对，上面的知识可能知识单轮对话，但下列方法你既可以选择让他生成单轮对话，也可以让他生成多轮对话。

```python
import json
import os

SYSTEM_PROMPT = """
你是一个信息抽取能手，你需要把我给你的内容做成QA对，模拟人和大模型的对话，你的回复要满足下列要求：
- 全部使用中文回复
- 根据内容的几个主题返回5~10条符合的QA对，但不要重复说相同问题，
- 如果遇到里面提到几步法，你要合在一个回答里面
- 提问要模拟用户在这个知识点的提问主题下进行对话、提问要做到口语化并尽可能简单且不要涉及到具体的人，提问最好大于5个字少于0个字（格式类似：......怎么办，......为什么？），而回答应非常详细可分点回答、需要长回答详细紧扣我给你的东西，
- 因为我给你的材料是语音转文本，可能有错误，你要在基于上下文理解的基础上帮忙修复。
- 不要提到任何作者信息，只需要结合内容回答抽取。
- 最后只需要返回json list,严格遵守返回为json list格式：[{'input': ,'output': },{'input': ,'output': }]
需要抽取的原文如下：
"""

# deepseek
from openai import OpenAI
deepseek_key = ""  #此处填写deepseek的key
client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com/v1")
def get_data_ds(content):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": content,
             "temperature": 0.7} # 多样化输出
        ]
    )
    res = response.choices[0].message.content
    return res

if __name__ == "__main__":

    txt_folder_path = "tianji_datasets/06-Awkwardness-其他/txt"
    output_file_path = './tianji-other-chinese-awkwardness-v0.1.json'
    error_file_path = "./tianji_qa_error_files.txt"

    all_qadata = []
    count = 0
    for filename in os.listdir(txt_folder_path):
        print(f"\n\n当前处理第{count}个txt文件 {filename}\n")
        file_path = os.path.join(txt_folder_path, filename)  # 获取文件完整路径
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()  # 读取文件内容
                llm_reply = get_data_ds("<<开始>>"+content+"<<结束>>")
                json_text = llm_reply.replace(' ','').replace('\n','').replace('```','').replace('json','',1)
                json_text = json_text.strip()
                qadata = json.loads(json_text)
                print("当前结果:\n",qadata)
                all_qadata.extend(qadata)
        except Exception as e:
            # 重试一次
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()  # 读取文件内容
                    llm_reply = get_data_ds("<<开始>>"+content+"<<结束>>")
                    json_text = llm_reply.replace(' ','').replace('\n','').replace('```','').replace('json','',1)
                    json_text = json_text.strip()
                    qadata = json.loads(json_text)
                    print("当前结果:\n",qadata)
                    all_qadata.extend(qadata)   
            except Exception as e:
                # 如果处理过程中出现异常，记录错误文件地址
                with open(error_file_path, "a", encoding='utf-8') as error_file:
                    print("错误！",e)
                    print("错误！",json_text)
                    error_file.write(file_path+'\n')
            continue
        count += 1

    with open(output_file_path, "w", encoding='utf8') as f:
        json.dump(all_qadata, f, ensure_ascii=False, indent=4)
```

生成后大概格式是这样：

```python
    [{
        "input": "拒绝会不会损害人际关系？",
        "output": "拒绝确实可能得罪人，但它是为了保护你的时间、精力和价值观。重要的是明确自己的需求和目标，然后基于这些做出决策。关注于谁一直陪伴你和支持你，而不是谁离开了你，这样才能建立更健康的人际关系。"
    },
    {
        "input": "如何处理拒绝后的失去感？",
        "output": "关注于你通过拒绝获得的东西，比如时间、精力和自我尊重。人生中的战略选择更多地体现在你放弃了什么，而不是你选择了什么。通过拒绝，你可以更清晰地定义自己的目标，从而获得更精准的人生方向。"
    },
    {
        "input": "为什么女孩子在恋爱中需要学会拒绝渣男？",
        "output": "在恋爱中学会拒绝是为了保护自己的情感和未来，避免与不合适的人建立关系。拒绝渣男可以帮助验证和维护一个人的价值观和人格，确保建立健康、平等的恋爱关系。"
    }]
```

我们可以用合并脚本清洗脚本（在这上面你可能会得到多个这样的json list 文件，你需要把他变成训练用的json格式，并且指定system prompt）

```python
import os
import json

def extract_and_merge_conversations(folder_path, output_file):
    all_conversations = []

    # 遍历指定文件夹
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            
            # 打开并读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # 提取需要的字段
                for item in data:
                    try:
                        extracted = {
                            'system': SYSTEM_PROMPT,
                            'input': item['input'],
                            'output': item['output']
                        }
                    except Exception as e : 
                        # 如果不满足json条件就不进行保存，这个时候一般都是json出错
                        print(item)
                    # 将每个对话包装在一个 'conversation' 键中，并作为独立对象加入列表
                    all_conversations.append({'conversation': [extracted]})

    # 将合并后的所有对话数据写入一个新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(all_conversations, file, ensure_ascii=False, indent=4)

# 使用示例
SYSTEM_PROMPT = """你现在是由SocialAI开发的人情世故大模型，你的任务是洞察人情世故、提供合适的交往策略和建议。在处理问题时，你应当考虑到文化背景、社会规范和个人情感，以帮助用户更好地理解复杂的人际关系和社会互动。"""
folder_path = 'tianji_test_data'  # 要扫描的文件夹路径
output_file = 'tianji-awkwardness-chinese-v0.1_datail.json'     # 输出文件的名称和路径
extract_and_merge_conversations(folder_path, output_file)
```

清洗后数据大概长得像：

```python
[
    {
        "conversation": [
            {
                "system": "你现在是由SocialAI开发的人情世故大模型，你的任务是洞察人情世故、提供合适的交往策略和建议。在处理问题时，你应当考虑到文化背景、社会规范和个人情感，以帮助用户更好地理解复杂的人际关系和社会互动。",
                "input": "领导夸我工作表现不错，我该怎么幽默回应？",
                "output": "在领导面前，高情商的回应不仅能够展现你的自信和幽默感，还能加深领导对你的好印象。当领导表扬你说‘你今天表现不错，很精神’时，你可以机智地回答：‘跟您这样的领导学习，那必须得进步，不能丢了您的面子’。这样的回答既展现了你的谦逊，又隐含了对领导的尊重和追随，同时也巧妙地将焦点重新聚焦在领导身上，为领导增光添彩。"
            }
        ]
    },
    {
        "conversation": [
            {
                "system": "你现在是由SocialAI开发的人情世故大模型，你的任务是洞察人情世故、提供合适的交往策略和建议。在处理问题时，你应当考虑到文化背景、社会规范和个人情感，以帮助用户更好地理解复杂的人际关系和社会互动。",
                "input": "在饭局上，有人夸我能喝酒，我该如何机智应答？",
                "output": "在社交场合，如饭局上，当有人赞扬你‘酒量可以’，你不必过谦或紧张。一个幽默而得体的回应可以是这样的：‘其实我平常不怎么喝酒的，今天因为和您这样的贵宾一起，心情格外好，酒量就自然上来了’。这样的回答不仅巧妙地转移了对自己能力的过度夸耀，还表达了对对方的尊重和好感，同时也营造了一个轻松愉快的交流氛围。"
            }
        ]
    },
```

当然，上述代码还不够优雅，因为赶时间。。。但基本够我们制造出比较大型的数据了（可能爬一次就造个2k条，具体你可以通过变换不同造数据的prompt造出更多数据，然后在数据平衡的基础上利用大模型补充数据）

最后，我们需要把新数据和原数据合并。由于我们的数据都是分开收集，所以出现问题可以快速迭代，不至于需要从整份数据里面做清洗处理，合并训练格式json的代码为：

```python
import os
import json

def extract_and_merge_conversations(folder_path, output_file):
    all_conversations = []

    # 遍历指定文件夹
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            
            # 打开并读取JSON文件
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # 提取需要的字段
                for item in data:
                    for conversation in item['conversation']:
                        extracted = {
                            'system': conversation['system'],
                            'input': conversation['input'],
                            'output': conversation['output']
                        }
                        # 将每个对话包装在一个 'conversation' 键中，并作为独立对象加入列表
                        all_conversations.append({'conversation': [extracted]})

    # 将合并后的所有对话数据写入一个新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(all_conversations, file, ensure_ascii=False, indent=4)

# 使用示例
folder_path = 'tianji_final_dataset_0504'  # 要扫描的文件夹路径
output_file = 'tianji_dataset_all_0504.json'     # 输出文件的名称和路径
extract_and_merge_conversations(folder_path, output_file)
```

## 训练测试

因为我们已经得到了目标训练数据json，只需要参考训练教程即可：

https://github.com/SocialAI-tianji/Tianji/blob/main/docs/finetune/tianji-wishes-chinese.md