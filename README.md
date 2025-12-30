Start formula engine using:-
Wihout LLM(Write rules directly on formulas.json):
``` uvicorn formula_engine:app --port 8000 ```
With LLM(natural language to JSON, GPU RECOMMENDED):
```USE_LLM=True python -m uvicorn formula_engine:app --port 8000``

Non-engineers (risk team, finance analysts, product managers) can write the rules for calculating metrics in DSL.txt and variables that need to be given by the user in input.txt.(REFERENCE IS PROVIDED).
