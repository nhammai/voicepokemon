import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from speech2text import speech2text
import pvporcupine
import pyaudio
import struct
import pyautogui  # Import pyautogui
import keyboard

# Do text to command with open ai api
os.environ["OPENAI_API_KEY"] = ""

llm = OpenAI(temperature=0.9)
prompt = PromptTemplate(
    input_variables=["sentence"],
    template=(
        "Act as if you're an super NLP api"
        "I'm about creating a pokemon game so with voice command and I want it to understand my sentence.\n\n"
        "I want to analyse the sentence\n\n"
        "If it is similar to \"Phóng điện x V\" with Phóng điện as the skill the Pokémon uses and x as the amount of V to attack.\n\n"
        "Now I just need to translate the sentence I type to become the standard command to add it to my game\n\n"
        "Example: \"Phóng điện 10000 vôn\" then you print\n\n"
        "Command: thunder\n\n"
        "Amount: 10000\n\n"
        "Example: \"Phóng điện 1 triệu vôn\" then you print\n\n"
        "Command: thunder\n\n"
        "Amount: 1000000\n\n"
        "Example: \"Phóng điện 20 vôn\" then you print\n\n"
        "Command: thunder\n\n"
        "Amount: 20\n\n"
        "Example: \"Phóng điện một triệu hai trăm vôn\" then you print\n\n"
        "Command: thunder\n\n"
        "Amount: 1200000\n\n"
        "\"điện 100000 V\" then you print\n\n"
        "Command: thunder\n\n"
        "Amount: 100000\n\n"
        "Example: \"pikachu phóng điện\" then you print\n\n"
        "Command: thunder\n\n"
        "Amount: 1000\n\n"
        "The amount default if I don't say is 1000\n\n"
        "If it is similar to \"Quả cầu điện\" or \"Quả bóng điện\" \n\n"
        "Now I just need to translate the sentence I type to become the standard command to add it to my game\n\n"
        "Example: \"Pikachu quả bóng điện\" then you print\n\n"
        "Command: electricball\n\n"
        "Amount: 0\n\n"
        "Example: \"Quả cầu điện\" then you print\n\n"
        "Command: electricball\n\n"
        "Amount: 0\n\n"
        "Example: \"Pikachu quả cầu điện \" then you print\n\n"
        "Command: electricball\n\n"
        "Amount: 0\n\n"
        "Example: \"Quả banh điện\" then you print\n\n"
        "Command: electricball\n\n"
        "Amount: 0\n\n"
        "\"banh điện\" then you print\n\n"
        "Command: electricball\n\n"
        "Amount: 0\n\n"
        "If it is similar to \"Đuôi sắt\" or \"Đuôi thép\" \n\n"
        "Now I just need to translate the sentence I type to become the standard command to add it to my game\n\n"
        "Example: \"Pikachu đuôi sắt\" then you print\n\n"
        "Command: irontail\n\n"
        "Amount: 0\n\n"
        "Example: \"đuôi sắt\" then you print\n\n"
        "Command: irontail\n\n"
        "Amount: 0\n\n"
        "Example: \"Pikachu đuôi sắt \" then you print\n\n"
        "Command: irontail\n\n"
        "Amount: 0\n\n"
        "Example: \"Đuôi thép\" then you print\n\n"
        "Command: irontail\n\n"
        "Amount: 0\n\n"
        "\"đuôi kim loại\" then you print\n\n"
        "Command: irontail\n\n"
        "Amount: 0\n\n"
        "Remember there is only the format"
        "Command: nameoftheability"
        "Amount: amountoftheability"
        "There's no other text beside this format"
        "If you can not recognize then we have the default:"
        "Command: thunder\n\n"
        "Amount: 1000\n\n"
        "Also if you find I say something super silly and not relevant to the ability or command then just set up the default:"
        "Command: thunder\n\n"
        "Amount: 1000\n\n"
        "You will never leave the command and amount empty or silly operator like this:"
        "Command: -"
        "Amount: -"
        "At least if you don't know what to do you have to setup to the default value like this:"
        "Command: thunder\n\n"
        "Amount: 1000\n\n"
        "Never say things like this:"
        "In this case, we set up the default:Command: thunder"

        "Amount: 1000"
        "Because you will break my code"
        "Just shut up. Say nothing but:"
        "Command: nameoftheability"
        "Amount: amountoftheability"
        "And remember you don't say anything to me beside:"
        "Command: nameoftheability"
        "Amount: amountoftheability"
        "And remember you don't understand then we have the default:"
        "Command: thunder\n\n"
        "Amount: 1000\n\n"
        "You're an API you're not a chatbot so you don't say:"
        "Since this sentence does not match the format for command and amount, you will set up to the default:"
        "Command: thunder"

        "Amount: 1000"
        "You only say: "
        "Command: thunder"

        "Amount: 1000"

        "Analyse it to the command and amount\n\n"
        "The sentence is: {sentence}\n\n"
    ),
)

# check_prompt = PromptTemplate(
#     input_variables=["sentence"],
#     template=(
#         "Act as if you're an API. Your job will check the "
#     ),
# )





chain = LLMChain(llm=llm, prompt=prompt)

def speech2command():
    sentence = speech2text()  # get the text from voice input
    result = chain.run(sentence)

    with open("command.txt", "w+", encoding="utf-8") as f:  # Use 'w+' mode to open the file for both writing and reading
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

        print("Listening for 'Pika chu'...")

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
