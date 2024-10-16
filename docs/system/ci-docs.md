# CI Pipeline 说明

本项目的持续集成（CI）管道主要通过 GitHub Actions 实现，旨在自动化构建、测试和部署过程，以确保代码的质量和稳定性。

具体的 CI 配置文件位于 `.github/workflows/check.yml`，该文件定义了各个工作流程和步骤，包括代码检查、测试执行和构建过程等。通过这些自动化流程，开发者可以更高效地管理项目，及时发现并修复潜在问题，从而提升开发效率和代码质量。

## prompt 管理说明

目前实现

1.prompt检查，

2.prompt格式从markdown到json的转换，

3.json格式prompt的合并

### job:check (prompt 检查)

- step:Run check.py (.ci/check.py)

  - 功能：

    检查test/prompt里markdown格式的 prompt文件是否符合 test/prompt/08-None-prompt编写规则模板.md 中描述的格式

  - 输入：

    无输入

  - 输出：

    文档格式正确则会输出 "文档路径：格式正确"

    文档格式错误则输出 "文档路径： 不符合规则模板：\<不符合规则的原因>"

    例：

    > test/rompt/08-None-prompt编写规则模板.md: 格式正确

    > test/prompt/gpt_prompt/01-Etiquette/01-Etiquette-职场与同学聚会敬酒.md 不符合规则模板: Prompt部分未识别

    > test/prompt/gpt_prompt/02-Hospitality/02-Hospitality-家宴如何排座次.md 不符合规则模板: 不存在以## 开头的汉字标题

### job:prompt_to_json (转为json格式，并合并)

- step: gpt_prompt to json&&yiyan_prompt to json (.ci/prompt_to_json_for_CI.py)

  - 功能：

    获取 folder_path 中的markdown 格式的 prompt文件，然后转为对应的json格式

  - 输入：

    - folder_path

      markdown格式的prompt文件所在目录的路径（folder_path路径中一定要带prompt目录，标准markdown文件格式请参考test/prompt/08-None-prompt编写规则模板.md）

      例：

      > test/prompt/gpt_prompt

    - output_path

      写入json文件的目录路径

      例：

      > tianji/prompt（这里只需要到prompt所在目录即可，脚本会识别并拼接prompt目录的下级目录）

  - 输出：

    - 文档使用的heading（也就是文档内最大标题的格式），处理的文档名与所属分类，并输出json文件

      例：

      > 此文档的heading使用的是 ##
      > 处理文档为 01-Etiquette-职场与同学聚会敬酒.md 该文档属于第1大类
      >
      > \[
      > {
      > "id": ,
      > "name": "",
      > "system_prompt": "",
      > "example": \[
      > {
      > "input": "",
      > "output": "！"
      > },
      > {
      > "input": "",
      > "output": ""
      > }
      > \]
      > },
      >
      > ......
      >
      > (这里需要注意markdown文件名格式，格式为“大类id-类名-具体场景”)
      >
      > 输出的json格式意义为：
      >
      > ```txt
      > id： prompt所属大类
      > name:子标题
      > test_system:prompt内容
      > input:用户输入
      > output:对应输出
      > ```

- step：Merge the gpt_prompt &&Merge the yiyan_prompt  (.ci/build_all_gpt_prompt.py && .ci/build_all_yiyan_prompt.py)

  - 功能：

    合并对应目录下json格式的prompt

  - 输入：

    - gpt_folder_path(yiyan_floder_path)

      gpt_prompt所在的目录路径，会合并所有该路径下的json

    - gpt_output_json_path(yiyan_output_json_path)

      要输出所有合并的json的文件路径

  - 输出：

    合并后的json文件

​
