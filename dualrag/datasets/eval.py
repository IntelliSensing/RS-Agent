import os
import re
import json
from pathlib import Path

from openai import OpenAI

# Configure via environment variables (see .env.example)
api_key = os.environ.get("OPENAI_API_KEY", "")
base_url = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")

def eval_answers(query_file, result1_file, result2_file, output_file_path):
    client = OpenAI(api_key=api_key, base_url=base_url)

    # 读取问题
    with open(query_file, "r") as f:
        data = f.read()
    queries = re.findall(r"- Question \d+: (.+)", data)

    # 读取答案集1
    with open(result1_file, "r") as f:
        answers1 = json.load(f)
    answers1 = [i["result"] for i in answers1]

    # 读取答案集2
    with open(result2_file, "r") as f:
        answers2 = json.load(f)
    answers2 = [i["result"] for i in answers2]

    results = []
    error_log_file = output_file_path.replace('.json', '_error_log.json')

    # 初始化胜率计数
    win_count = {
        "Comprehensiveness": {"Answer 1": 0, "Answer 2": 0},
        "Diversity": {"Answer 1": 0, "Answer 2": 0},
        "Empowerment": {"Answer 1": 0, "Answer 2": 0},
        "Overall Winner": {"Answer 1": 0, "Answer 2": 0}
    }

    for i, (query, answer1, answer2) in enumerate(zip(queries, answers1, answers2)):
        print(f"\nEvaluating Question {i + 1}...")

        sys_prompt = """
        ---Role---
        You are an expert tasked with evaluating two answers to the same question based on three criteria: **Comprehensiveness**, **Diversity**, and **Empowerment**.
        """

        prompt = f"""
        You will evaluate two answers to the same question based on three criteria: **Comprehensiveness**, **Diversity**, and **Empowerment**.

        - **Comprehensiveness**: How much detail does the answer provide to cover all aspects and details of the question?
        - **Diversity**: How varied and rich is the answer in providing different perspectives and insights on the question?
        - **Empowerment**: How well does the answer help the reader understand and make informed judgments about the topic?

        For each criterion, choose the better answer (either Answer 1 or Answer 2) and explain why. Then, select an overall winner based on these three categories.

        Here is the question:
        {query}

        Here are the two answers:

        **Answer 1:**
        {answer1}

        **Answer 2:**
        {answer2}

        Evaluate both answers using the three criteria listed above and provide detailed explanations for each criterion.
        - Your output **MUST** be a valid JSON object.  
        - Do **NOT** include any extra text or commentary.  
        - Pay close attention to **bracket matching** , especially the last bracket.
        - Ensure that the JSON structure is strictly valid and follows this format exactly:  

        {{
            "Comprehensiveness": {{
                "Winner": "[Answer 1 or Answer 2]",
                "Explanation": "[Provide explanation here]"
            }},
            "Diversity": {{
                "Winner": "[Answer 1 or Answer 2]",
                "Explanation": "[Provide explanation here]"
            }},
            "Empowerment": {{
                "Winner": "[Answer 1 or Answer 2]",
                "Explanation": "[Provide explanation here]"
            }},
            "Overall Winner": {{
                "Winner": "[Answer 1 or Answer 2]",
                "Explanation": "[Summarize why this answer is the overall winner based on the three criteria]"
            }}
        }}
        """

        try:
            # 调用接口生成评估结果
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": prompt}
                ]
            )

            # 解析返回结果
            result = response.choices[0].message.content.strip()
            result_json = json.loads(result)

            # 实时显示结果
            print(json.dumps(result_json, indent=4, ensure_ascii=False))

            # 统计胜率
            win_count["Comprehensiveness"][result_json["Comprehensiveness"]["Winner"]] += 1
            win_count["Diversity"][result_json["Diversity"]["Winner"]] += 1
            win_count["Empowerment"][result_json["Empowerment"]["Winner"]] += 1
            win_count["Overall Winner"][result_json["Overall Winner"]["Winner"]] += 1

            # 保存成功结果
            results.append({
                "question": query,
                "answer1": answer1,
                "answer2": answer2,
                "evaluation": result_json
            })

        except json.JSONDecodeError as e:
            print(f"❌ Error decoding JSON for question {i + 1}: {e}")
            print(f"Raw output:\n{result}")

            # 保存解析失败的原始输出
            with open(error_log_file, "a") as error_log:
                json.dump({
                    "question": query,
                    "answer1": answer1,
                    "answer2": answer2,
                    "raw_output": result,
                    "error": str(e)
                }, error_log, indent=4, ensure_ascii=False)
                error_log.write(",\n")

            # 解析失败的结果也存储在最终文件中，便于完整对比
            results.append({
                "question": query,
                "answer1": answer1,
                "answer2": answer2,
                "evaluation": {
                    "error": str(e),
                    "raw_output": result
                }
            })

    # 保存结果到文件
    with open(output_file_path, "w") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print(f"\n✅ Results saved to {output_file_path}")

    # === 输出胜率 ===
    print("\n==== Win Rate Statistics ====")
    for category, counts in win_count.items():
        total = counts["Answer 1"] + counts["Answer 2"]
        win_rate_1 = counts["Answer 1"] / total * 100 if total > 0 else 0
        win_rate_2 = counts["Answer 2"] / total * 100 if total > 0 else 0
        print(f"\n{category}:")
        print(f"  - Answer 1 win rate: {win_rate_1:.2f}% ({counts['Answer 1']}/{total})")
        print(f"  - Answer 2 win rate: {win_rate_2:.2f}% ({counts['Answer 2']}/{total})")

if __name__ == "__main__":
    dualrag_root = Path(__file__).resolve().parents[1]
    datasets_dir = Path(__file__).resolve().parent

    query_file = datasets_dir / "questions" / "mix_questions.txt"
    result1_file = dualrag_root / "mix_local_result.json"
    result2_file = dualrag_root / "mix_result.json"
    output_file_path = dualrag_root / "mix_compare_results.json"

    eval_answers(query_file, result1_file, result2_file, output_file_path)