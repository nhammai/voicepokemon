import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from speech2text import speech2text
import pvporcupine
import pyaudio
import struct
import keyboard
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

    "command": "thunder",
    "amount": "10000"

    "điện 100000 V" then we have

    "command": "thunder",
    "amount": "100000"

    example: "Phóng điện 12000 vôn" then we have:

    "command": "thunder",
    "amount": "12000"
    example: "Phóng điện 20 vôn" then we have:

    "command": "thunder",
    "amount": "20"

    example: "Phóng điện một nghìn hai trăm lẻ một vôn" then we have:

    "command": "thunder",
    "amount": "1201"

    example: "Phóng điện một triệu vôn" then we have:

    "command": "thunder",
    "amount": "1000000"

    example: "Phóng điện một 1000000 vôn" then we have:

    "command": "thunder",
    "amount": "1000000"

    example: "Phóng điện một 2000000 vôn" then we have:

    "command": "thunder",
    "amount": "2000000"
    

    example: "Phóng điện một nghìn hai trăm lẻ một vôn" then we have:

    "command": "thunder",
    "amount": "1201"

    example: "pikachu phóng điện" then we have:

    "command": "thunder",
    "amount": "1000"

    The amount default if I don't say is 1000 

    If it is similar to Quả cầu điện or Quả bóng điện.Remember we must have the  curly bracket because we using json format. I don't write it here but you must write it:
    Example "Pikachu quả bóng điện" then we have
    "command": "electricball"
    "amount": "1000"
    Example: "Quả cầu điện" then we have:
    "command": "electricball"
    "amount": "1000"
    Example: "Pikachu quả cầu điện" then we have:
    "command": "electricball"
    "amount": "1000"
    Example: "Quả banh điện" then we have
    "command": "electricball"
    "amount": "1000"
    Example: "banh điện" then we have:
    "command": "electricball"
    "amount": "1000"

    If it is similar to "Đuôi sắt" or "Đuôi thép". Remember we must have the  curly bracket because we using json format. I don't write it here but you must write it:
    Example: "Pikachu đuôi sắt" then we have
    "command": "irontail"
    "amount": "1000"
    Example: "đuôi sắt" then we have:
    "command": "irontail"
    "amount": "1000"
    Example: "Pikachu đuôi sắt" then we have:
    "command": "irontail"
    "amount": "1000"
    Example: "Đuôi thép" then we have:
    "command": "irontail"
    "amount": "1000"
    "đuôi kim loại" then we have:
    "command": "irontail"
    "amount": "1000"


    Remember we must have the json format and the bracket:

    "command": "nameoftheability"
    "amount": "amountoftheability"

    There's no other text beside this json format with the bracket operator. Never miss the curly bracket operator
    If you can not recognize then we have the default:
    "command": "thunder"
    "amount": "1000"
    Also if you find I say something super silly and not relevant to the ability or command then just set up the default:
    "command": "thunder"
    "amount": "1000"

    Translate it to the command and amount.
    Remember we must have the  curly bracket because we using json format. And don't say any text just say in json format because you're an API.
    You must have the curly brackets. 

    Now the sentence is: {sentence}

"""
prompt = PromptTemplate(
    input_variables=["sentence"],
    template=template,
)



def is_valid_json(json_obj):
    if "command" in json_obj and "amount" in json_obj:
        return True
    return False

def clean_response(response: str):
    # Default JSON to return in case of invalid JSON structure
    default_json = {
        "command": "thunder",
        "amount": "1000"
    }

    # Search for a JSON-like pattern in the response
    match = re.search(r'"\s*command"\s*:\s*".*"\s*,\s*"\s*amount"\s*:\s*".*"', response)
    
    if match:
        # Get the matched text and wrap it with curly braces
        json_str = '{' + match.group(0) + '}'
        
        try:
            # Attempt to parse it as JSON
            json_obj = json.loads(json_str)

            # Validate the JSON structure
            if not is_valid_json(json_obj):
                return json.dumps(default_json, indent=4)
            
            # Re-encode to a pretty-printed JSON string
            pretty_json_str = json.dumps(json_obj, indent=4)
            
            return pretty_json_str
        except json.JSONDecodeError:
            # If JSON decoding fails, return the default JSON
            return json.dumps(default_json, indent=4)
    else:
        # If no JSON-like pattern is found, return the default JSON
        return json.dumps(default_json, indent=4)


chain = LLMChain(llm=llm, prompt=prompt)

def speech2command():
    sentence = speech2text()  # get the text from voice input
    result = chain.run(sentence)
    print(result)
    result = clean_response(result)
    with open("command.json", "w+", encoding="utf-8") as f:  # Use 'w+' mode to open the file for both writing and reading
        f.truncate(0)  # This will make sure the file is completely empty
        f.write(result)



# do wake word to activate 
KEYWORD_PATH = "pika-chu_en_windows_v2_2_0.ppn"
ACCESS_KEY = "pOXDnIw9kRswMpL270PgGOWHxugjHgPau48xLQtUdFNkYcFKEkT0Pg=="

def main():
    porcupine = None
    pa = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=[KEYWORD_PATH],
            sensitivities=[0.5]
        )

        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for 'Pikachu'...")

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Pika Pika")
                keyboard.press('p')
                keyboard.release('p')
                # pyautogui.keyDown('space')  # Press the 'P' key
                speech2command()
                keyboard.press('space')
                keyboard.release('space')
                os.remove("output.wav")

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
            pa.terminate()

if __name__ == "__main__":
    main()
