from fastapi import FastAPI
import json, os
from parser import Parser
import sqlite3
from datetime import datetime
from llm import generate_formula_dsl

USE_LLM = os.getenv("USE_LLM", "False").lower() == "true"
outputs = {}

app = FastAPI()
formula_file = "formulas.json"
input_schema_file = "input_schema.json"
formulas = {}
input_schema = {}
_formula_mtime = 0
conn = None
cursor = None

def validate_inputs(inputs, schema):
    validated = {}

    for key, rules in schema.items():
        if rules.get("required") and key not in inputs:
            raise ValueError(f"Missing required input: {key}")
        
        value = inputs.get(key, rules.get("default"))

        if rules.get("type") == "number":
            try:
                value = float(value)
            except (TypeError, ValueError):
                raise ValueError(f"Invalid type for {key}, expected number.")
            if "min" in rules and value < rules["min"]:
                raise ValueError(f"Value for {key} below minimum of {rules['min']}.")
            if "max" in rules and value > rules["max"]:
                raise ValueError(f"Value for {key} above maximum of {rules['max']}.")
        elif rules.get("type") == "string":
            try:
                value = str(value)
            except (TypeError, ValueError):
                raise ValueError(f"Invalid type for {key}, expected string.")
            
        validated[key] = value
    return validated

def load_formula_if_changed():
    global formulas, _formula_mtime
    mtime = os.path.getmtime(formula_file)
    if mtime != _formula_mtime:
        with open(formula_file) as f:
            formulas = json.load(f)
        _formula_mtime = mtime

def load_formula():
    global formulas
    with open(formula_file, 'r') as f:
        formulas = json.load(f)

def load_input_schema():
    global input_schema
    with open(input_schema_file, 'r') as f:
        input_schema = json.load(f)

@app.on_event("startup")
def startup():
    global conn, cursor
    if USE_LLM:
        generate_formula_dsl()
    load_formula()
    load_input_schema()

    
    conn = sqlite3.connect("decision_engine.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT,
        inputs TEXT,
        outputs TEXT
    )
    """)
    conn.commit()

@app.get("/input-schema")
def get_schema():
    return input_schema

def evaluate_formula(inputs, formula, parser):
    load_formula_if_changed()
    
    if isinstance(formula, str):
        return parser.eval_exp(formula, inputs)
    if parser.eval_exp(formula['if'], inputs):
        return evaluate_formula(inputs, formula['then'], parser)
    else: return evaluate_formula(inputs, formula['else'], parser)

@app.post("/evaluate")
def evaluate(inputs : dict):
    parser = Parser()
    validated_inputs = validate_inputs(inputs, input_schema)

    for name, formula in formulas.items():
        outputs[name] = evaluate_formula(validated_inputs, formula, parser)
        validated_inputs[name] = outputs[name]
        print(validated_inputs)
    
    cursor.execute(
        "INSERT INTO evaluations (created_at, inputs, outputs) VALUES (?, ?, ?)",
        (
            datetime.utcnow().isoformat(),
            json.dumps(validated_inputs),
            json.dumps(outputs)
        )
    )
    conn.commit()


    return outputs

@app.get("/evaluations")
def get_evaluations():
    cursor.execute("SELECT * FROM evaluations")
    rows = cursor.fetchall()
    return rows


if __name__ == '__main__':
    input = {"income" : 10000, "age" : 20, "employed" : "MNC", "debt" : 100}
    load_formula()
    load_input_schema()
    print(evaluate(input))





