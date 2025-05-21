from app.tools.symptom_tool import extract_symptoms, map_symptoms_to_departments

def symptom_to_department_tool(user_input: str) -> str:
    symptoms = extract_symptoms(user_input)
    if not symptoms:
        return "很抱歉，我无法从您的描述中提取出明确的症状，请尽量描述清楚您身体哪里不适。"

    departments = map_symptoms_to_departments(symptoms)
    if not departments:
        return f"您提到的症状：{', '.join(symptoms)} 暂未能匹配到科室，建议前往医院就诊，由前台协助挂号。"

    return f"根据您的描述（{', '.join(symptoms)}），建议您前往 {', '.join(departments)} 就诊。"
