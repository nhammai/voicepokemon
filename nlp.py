import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

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

sentence = open("rawtext.txt", "r", encoding="utf-8").read().strip()
result = chain.run(sentence)

with open("command.txt", "w", encoding="utf-8") as f:  # Use 'w' mode to overwrite the file
    f.write(result)