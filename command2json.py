import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json


# Do text to command with open ai api
os.environ["OPENAI_API_KEY"] = ""

llm = OpenAI(temperature=0.9)
template = """
    act as if you're a super API intergrate with amazing nlp model. I want to use you to translate my command and you provide me a json syntax and say nothing but provide me the json.
    I want to analyse the sentence 

    If it similar to " Phóng điện x V" with Phóng điện is the skill the pokenmon attach 

    x is the amount of V to attack. 

    Now I just need to translate the sentence I type to become the standard command to add it to my game

    example: "Phóng điện 10000 vôn" then we have 

    "Command": "electric discharge",
    "amount": "10000"

    "điện 100000 V" then we have

    "Command": "electric discharge",
    "amount": "100000"


    example: "pikachu phóng điện" then you print 

    "Command": "electric discharge",
    "amount": "1000"

    The amount default if I don't say is 1000 

    Translate it to the command and amount
    
    

    Now the sentence is: {sentence}

"""
prompt = PromptTemplate(
    input_variables=["sentence"],
    template=template,
)

def clean_response(response: str):
    try:
        # This assumes that the JSON object always starts with '{' and ends with '}'
        start_index = response.index('{')
        end_index = response.rindex('}') + 1
        json_str = response[start_index:end_index]
        # Parse the string with a JSON decoder
        json_obj = json.loads(json_str)
        # Re-encode to get cleaned version
        clean_json_str = json.dumps(json_obj, indent=4)
        return clean_json_str
    except ValueError:
        print("The response does not contain a valid JSON object")
        return response




chain = LLMChain(llm=llm, prompt=prompt)



def main():
   sentence = "Kích điện 30000 vôn"
   result = chain.run(sentence)
   print(result)

    # Clean the result
   result = clean_response(result)

   print(result)
   with open("command.json", "w+", encoding="utf-8") as f:  # Use 'w+' mode to open the file for both writing and reading
        f.truncate(0)  # This will make sure the file is completely empty
        f.write(result)

if __name__ == "__main__":
    main()
