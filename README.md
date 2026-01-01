Start formula engine using:-
Wihout LLM(Write rules directly on formulas.json):
``` uvicorn formula_engine:app --port 8000 ```
With LLM(natural language to JSON, GPU RECOMMENDED):
``` USE_LLM=True uvicorn formula_engine:app --port 8000 ```

Non-engineers (risk team, finance analysts, product managers) can write the rules for calculating metrics in DSL.txt and variables that need to be given by the user in input.txt.(REFERENCE IS PROVIDED).
<h1>Note:</h1>  Rules cannot be changed in DSL.txt after formula_engine is started. Instead formulas.json can be modified.

<h1>Steps to follow:-</h1>
<img width="1872" height="540" alt="Screenshot 2026-01-01 161000" src="https://github.com/user-attachments/assets/2f88fe1d-afbc-4766-aa9a-ac7173178f0d" />
This is the interface that will appear once we enter the url.
<img width="1334" height="647" alt="Screenshot 2026-01-01 161202" src="https://github.com/user-attachments/assets/cbcf9d38-415d-442a-839e-e739edb7a026" />
Click on get end-point to get the input schema that should be followed by the user while entering the inputs.This image shows how input_schema looks like.
<img width="1808" height="922" alt="Screenshot 2026-01-01 161613" src="https://github.com/user-attachments/assets/2b9fee7c-6745-48d8-bbfb-cc539b629884" />
Enter the inputs in the manner shown above. Then click execute.
<img width="1646" height="189" alt="Screenshot 2026-01-01 162207" src="https://github.com/user-attachments/assets/470002ae-8327-484c-b436-7927c5ae47c4" />
This is how the output looks like.
<h1>Architecture Overview</h1>

<img width="388" height="432" alt="Screenshot 2026-01-01 163918" src="https://github.com/user-attachments/assets/5f719d3e-2769-4b9e-a844-5c6157bd235b" />
