
from typing import List
import json
from difflib import get_close_matches
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama

# 加载症状 -> 科室映射
with open("../../data/symptom_to_department.json", "r", encoding="utf-8") as f:
    SYMPTOM_TO_DEPARTMENT = json.load(f)

# 初始化 LLM
# llm = ChatOpenAI(temperature=0.3, model_name="gpt-3.5-turbo")

# 改用本地大模型
# 初始化本地 Ollama 模型
llm = ChatOllama(
    model="qwen2:7b",
    temperature=0.3,
)

# 提取关键词的 Prompt
SYMPTOM_EXTRACTION_PROMPT = PromptTemplate.from_template("""
你是一位中文医院的问诊助手，擅长从自然语言中提取具体的疾病相关症状。请从以下患者描述中提取2~5字的中文【症状关键词】：

如果找不到任何症状，就返回空列表 `[]`。

用户描述：
"{user_input}"

请以 Python 列表形式返回，如：["头疼", "发烧"]
""")

# 标准化症状的 Prompt
SYMPTOM_STANDARDIZE_PROMPT = PromptTemplate.from_template("""
你是医院智能问诊系统，请将以下症状归一化为明确的、常见的疾病相关症状（控制在2-5个字）。
例如：“疼痛”应该归为“头痛”、“背痛”、“肚子疼”等具体部位。

如果无法确定部位，就返回“疼痛”。

仅返回关键词，不要解释：
"{symptom}"
""")


def extract_symptoms(user_input: str) -> List[str]:
    prompt = SYMPTOM_EXTRACTION_PROMPT.format(user_input=user_input)
    response = llm.predict(prompt)
    try:
        symptoms = eval(response.strip())
        if isinstance(symptoms, list):
            return symptoms
    except Exception:
        pass
    return []


def standardize_symptom(symptom: str) -> str:
    prompt = SYMPTOM_STANDARDIZE_PROMPT.format(symptom=symptom)
    response = llm.predict(prompt).strip()
    return response


def map_symptoms_to_departments(symptoms: List[str]) -> List[str]:
    departments = []
    for symptom in symptoms:
        # 先标准化
        std_symptom = standardize_symptom(symptom)
        # 精确匹配
        if std_symptom in SYMPTOM_TO_DEPARTMENT:
            departments.extend(SYMPTOM_TO_DEPARTMENT[std_symptom])
        else:
            # 模糊匹配（可选）
            matches = get_close_matches(std_symptom, SYMPTOM_TO_DEPARTMENT.keys(), n=1, cutoff=0.75)
            if matches:
                departments.extend(SYMPTOM_TO_DEPARTMENT[matches[0]])

    return list(set(departments))  # 去重
