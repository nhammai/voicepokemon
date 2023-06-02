import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import re

# Do text to command with open ai api
os.environ["OPENAI_API_KEY"] = ""

llm = OpenAI(temperature=0.9)
template = """
    act as if you're a super API intergrate with amazing nlp model. I want to use you to translate my command and you provide me a json syntax and say nothing but provide me the json.
    I want to analyse the sentence 

    If it similar to " Phóng điện x V" with Phóng điện is the skill the pokenmon attach 

    x is the amount of V to attack. 

    Now I just need to translate the sentence I type to become the standard command to add it to my game. Remember we must have the  curly bracket because we using json format. I don't write it here but you must write it:

    example: "Phóng điện 10000 vôn" then we have 

    "Command": "thunder",
    "amount": "10000"

    "điện 100000 V" then we have

    "Command": "thunder",
    "amount": "100000"

    example: "Phóng điện 12000 vôn" then we have:

    "Command": "thunder",
    "amount": "12000"
    example: "Phóng điện 20 vôn" then we have:

    "Command": "thunder",
    "amount": "20"

    example: "Phóng điện một nghìn hai trăm lẻ một vôn" then we have:

    "Command": "thunder",
    "amount": "1201"

    example: "Phóng điện một triệu vôn" then we have:

    "Command": "thunder",
    "amount": "1000000"

    example: "Phóng điện một 1000000 vôn" then we have:

    "Command": "thunder",
    "amount": "1000000"

    example: "Phóng điện một 2000000 vôn" then we have:

    "Command": "thunder",
    "amount": "2000000"
    

    example: "Phóng điện một nghìn hai trăm lẻ một vôn" then we have:

    "Command": "thunder",
    "amount": "1201"

    example: "pikachu phóng điện" then we have:

    "Command": "thunder",
    "amount": "1000"

    The amount default if I don't say is 1000 

    If it is similar to Quả cầu điện or Quả bóng điện.Remember we must have the  curly bracket because we using json format. I don't write it here but you must write it:
    Example "Pikachu quả bóng điện" then we have
    "Command": "electricball"
    "Amount": "1000"
    Example: "Quả cầu điện" then we have:
    "Command": "electricball"
    "Amount": "1000"
    Example: "Pikachu quả cầu điện" then we have:
    "Command": "electricball"
    "Amount": "1000"
    Example: "Quả banh điện" then we have
    "Command": "electricball"
    "Amount": "1000"
    Example: "banh điện" then we have:
    "Command": "electricball"
    "Amount": "1000"

    If it is similar to "Đuôi sắt" or "Đuôi thép". Remember we must have the  curly bracket because we using json format. I don't write it here but you must write it:
    Example: "Pikachu đuôi sắt" then we have
    "Command": "irontail"
    "Amount": "1000"
    Example: "đuôi sắt" then we have:
    "Command": "irontail"
    "Amount": "1000"
    Example: "Pikachu đuôi sắt" then we have:
    "Command": "irontail"
    "Amount": "1000"
    Example: "Đuôi thép" then we have:
    "Command": "irontail"
    "Amount": "1000"
    "đuôi kim loại" then we have:
    "Command": "irontail"
    "Amount": "1000"


    Remember we must have the json format and the bracket:

    "Command": "nameoftheability"
    "Amount": "amountoftheability"

    There's no other text beside this json format with the bracket operator. Never miss the curly bracket operator
    If you can not recognize then we have the default:
    "Command": "thunder"
    "Amount": "1000"
    Also if you find I say something super silly and not relevant to the ability or command then just set up the default:
    "Command": "thunder"
    "Amount": "1000"

    Translate it to the command and amount.
    Remember we must have the  curly bracket because we using json format. And don't say any text just say in json format because you're an API.
    You must have the curly brackets. 

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
        # Find the start of json content
        start = response.find('"Command"')

        # Find the end of json content by matching the pattern
        # Updated regex pattern to match 'amount' case-insensitively
        pattern = r'"[Aa]mount": "\d+"'
        match = re.search(pattern, response)

        if not match:
            return response  # Return original response if no match found

        end = match.end()

        # Extract json content
        json_content = '{' + response[start:end] + '}'

        # Load as python dictionary
        data = json.loads(json_content)

        # Convert back to json formatted string
        clean_json = json.dumps(data, indent=4)

        return clean_json




chain = LLMChain(llm=llm, prompt=prompt)



def main():
   sentence = "pikachu quả bóng điện 20000 vôn"
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
