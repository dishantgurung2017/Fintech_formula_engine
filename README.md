# How to Start the Formula Engine
## Without LLM (Rules written directly in formulas.json)
Use this mode when formulas are already defined in JSON.
```bash
uvicorn formula_engine:app --port 8000 

## With LLM (Natural Language → JSON)
Recommended when non-engineers want to define rules using plain English.
GPU is recommended for this mode.
With LLM(natural language to JSON, GPU RECOMMENDED):
```bash
USE_LLM=True uvicorn formula_engine:app --port 8000

<h1>Designed for Non-Engineers</h1>
<h2>DSL.txt</h2>
Used by risk teams, finance analysts, or product managers to write rules in natural language.
<h2>input.txt</h2>
Lists the variables that users must provide (reference format provided).

The LLM automatically converts these rules into structured JSON formulas used by the engine.
  
<h1>Important Notes</h1>  
Rules in DSL.txt cannot be changed after the engine starts
formulas.json can be modified at runtime
This ensures deterministic execution and avoids inconsistent rule evaluation

<h1>How to Use the API (Step-by-Step)</h1>
<h2>Step 1️ – Open the API Interface</h2>
Once the server starts, open your browser and go to:```http://localhost:8000/docs```
This opens the Swagger UI.
<img width="1872" height="540" alt="Screenshot 2026-01-01 161000" src="https://github.com/user-attachments/assets/2f88fe1d-afbc-4766-aa9a-ac7173178f0d" />

<h2>Step 2️ – Get the Input Schema</h2>
Click on the GET /input-schema endpoint.
This endpoint returns the exact structure the user must follow while providing inputs.
<img width="1334" height="647" alt="Screenshot 2026-01-01 161202" src="https://github.com/user-attachments/assets/cbcf9d38-415d-442a-839e-e739edb7a026" />

<h2>Step 3️ – Submit Inputs</h2>
Click on the POST /evaluate endpoint and enter inputs exactly as per the schema.
Then click Execute.
<img width="1808" height="922" alt="Screenshot 2026-01-01 161613" src="https://github.com/user-attachments/assets/2b9fee7c-6745-48d8-bbfb-cc539b629884" />

<h2>Step 4️ – View Results</h2>
The engine evaluates all configured formulas and returns the calculated metrics.
<img width="1646" height="189" alt="Screenshot 2026-01-01 162207" src="https://github.com/user-attachments/assets/470002ae-8327-484c-b436-7927c5ae47c4" />

<h1>Architecture Overview</h1>

<img width="388" height="432" alt="Screenshot 2026-01-01 163918" src="https://github.com/user-attachments/assets/5f719d3e-2769-4b9e-a844-5c6157bd235b" />
