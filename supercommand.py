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
os.environ["OPENAI_API_KEY"] = "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"

llm = OpenAI(temperature=0.9)
prompt = PromptTemplate(
    input_variables=["sentence"],
    template=(
        "I'm about creating a pokemon game so with voice command and I want it to understand my sentence.\n\n"
        "I want to analyse the sentence\n\n"
        "If it is similar to \"Phóng điện x V\" with Phóng điện as the skill the Pokémon uses and x as the amount of V to attack.\n\n"
        "Now I just need to translate the sentence I type to become the standard command to add it to my game\n\n"
        "Example: \"Phóng điện 10000 vôn\" then you print\n\n"
        "Command: thunder\n\n"
        "Amount: 10000\n\n"
        "\"điện 100000 V\" then you print\n\n"
        "Command: thunder\n\n"
        "Amount: 100000\n\n"
        "Example: \"pikachu phóng điện\" then you print\n\n"
        "Command: thunder\n\n"
        "Amount: 1000\n\n"
        "The amount default if I don't say is 1000\n\n"
        "Analyse it to the command and amount\n\n"
        "Now the sentence is: {sentence}\n\n"
    ),
)

chain = LLMChain(llm=llm, prompt=prompt)

def speech2command():
    sentence = speech2text() # get the text from voice input
    result = chain.run(sentence)

    with open("command.txt", "w", encoding="utf-8") as f:  # Use 'w' mode to overwrite the file
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
