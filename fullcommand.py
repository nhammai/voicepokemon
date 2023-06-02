import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

os.environ["OPENAI_API_KEY"] = "" # now we use the testfull prompt api to this

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

        "Analyse it to the command and amount\n\n"
        "Now the sentence is: {sentence}\n\n"
    ),
)

chain = LLMChain(llm=llm, prompt=prompt)

sentence = "Kích hoạt đuôi sắt"
result = chain.run(sentence)
print(result)