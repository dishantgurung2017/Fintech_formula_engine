import json
import yaml
from transformers import pipeline, AutoTokenizer


def extract_json(text: str) -> str:
    brace_count = 0
    start = None

    for i, ch in enumerate(text):
        if ch == "{":
            if brace_count == 0:
                start = i
            brace_count += 1
        elif ch == "}":
            brace_count -= 1
            if brace_count == 0 and start is not None:
                return text[start:i+1]

    raise ValueError("No valid JSON object found")

def load_llm(model_id="google/gemma-3-4b-it"):
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    generator = pipeline(
        "text-generation",
        model=model_id,
        tokenizer=tokenizer,
        max_new_tokens=400,
        temperature=0.0,
        do_sample=False
    )
    return generator

def generate_json_from_prompt(generator, prompt_path, dsl_text):
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = yaml.safe_load(f)["prompt"]

    prompt = prompt_template.format(input_text=dsl_text)

    output = generator(prompt)[0]["generated_text"]
    output = output.replace(prompt, "").strip()

    json_text = extract_json(output)
    return json.loads(json_text)

def generate_formula_dsl():
    with open("DSL.txt", "r", encoding="utf-8") as f:
        dsl_text = f.read()

    with open("input.txt", "r", encoding="utf-8") as f:
        input_text = f.read()

    generator = load_llm()

    input_schema = generate_json_from_prompt(
        generator,
        prompt_path="prompt_input_schema.yaml",
        dsl_text=input_text
    )

    rules = generate_json_from_prompt(
        generator,
        prompt_path="prompt_rules.yaml",
        dsl_text=dsl_text
    )

    with open("formulas.json", "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=4)

    with open("input_schema.json", "w", encoding="utf-8") as f:
        json.dump(input_schema, f, indent=4)


if __name__ == "__main__":
    generate_formula_dsl()
