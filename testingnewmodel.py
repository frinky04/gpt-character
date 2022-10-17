import banana_dev as banana

api_key="b641be26-bb2b-463b-bcd6-ef203ee23069"
model_key="gptj"



while True:
    prompt = input("Input >>> ")
    model_inputs = { "text": prompt, "length": 50, "temperature": 0.9, "topK": 50, "topP": 0.9}
    output = banana.run(api_key, model_key, model_inputs)
    output = output["modelOutputs"][0]["output"].strip()
    print(output)