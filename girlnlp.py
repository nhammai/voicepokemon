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
template_areyouready = """
    act as if you're an super NLP model that you can understand everything about vietnamese language. Because we will talk with vietnamese here.
    You will analyze the sentence I provide to you. And the output is only "yes" or "no" and nothing else. Just "yes" or "no" never maybe. You can do it.
    It like classify text. yes or no. To the question: "Bạn đã sẵn sàng để chinh phục thế giới Pokemon chưa nhỉ?". It mean: "Are you ready to conquer the Pokemon world?". 
    Here are some examples to the answer is yes:
    "Có mình đã sẵn sàng" ,
    "Mình đã sẵn sàng",
    "Mình rất muốn",
    "Có,mình rất muốn",
    "Mình sẵn sàng rồi",
    "Ngại gì vết bẩn",
    "Sẵn sàng",
    "Ok",
    "bắt đầu nào",
    "Chơi liền",
    "Chiến thôi nào",
    "Nhào dô",
    "Được rồi",
    "Tất nhiên! Tôi không thể chờ đợi để trở thành một huấn luyện viên Pokemon thực thụ!",
    "Đúng rồi! Tôi đã sẵn sàng từ lâu để bước vào cuộc phiêu lưu trong thế giới Pokemon!",
    "Chắc chắn! Chinh phục thế giới Pokemon là một trong những ước mơ lớn nhất của tôi!",
    "Đương nhiên! Tôi đã chuẩn bị tâm lý và kỹ năng để chiến đấu với những Pokemon mạnh mẽ!",
    "Tôi đã đặt cả trái tim vào việc này. Hãy chuẩn bị cho một cuộc hành trình Pokemon đầy thú vị!"
    Here are some examples to the answer is no:
    "Chưa mình chưa sẵn sàng",
    "Không sẵn sàng",
    "Mình không",
    "Mình chưa chắc nữa",
    "Mình không rõ",
    "Mình thấy rất đáng sợ",
    "Không, cảm ơn. Thế giới Pokemon không phù hợp với sở thích và mục tiêu của tôi.",
    "Tôi không quan tâm đến Pokemon lắm. Có lẽ tìm một thế giới khác phù hợp hơn với tôi.",
    "Xin lỗi, tôi không có hứng thú với việc chinh phục thế giới Pokemon. Chúc may mắn với những người khác!",
    "Tôi đã từng thử, nhưng không phù hợp với tôi. Tôi tìm kiếm một trò chơi khác để khám phá.",
    "Thật tiếc, nhưng tôi không có kế hoạch chinh phục thế giới Pokemon. Hy vọng bạn tìm được những người bạn tuyệt vời để tham gia cùng!"


    If you not sure then the answer is yes.
    remember only return yes or no and response in lowercase and without anyspace.
    Now the sentence is: {sentence}

"""

template_knowmore = """
    act as if you're an super NLP model that you can understand everything about vietnamese language. Because we will talk with vietnamese here.
    You will analyze the sentence I provide to you. And the output is only "yes" or "no" and nothing else. Just "yes" or "no" never maybe. You can do it.
    It like classify text. yes or no. To the question: "Bạn có cần mình giới thiệu một tí về cách thức chơi không nhỉ?". It mean: "Do you need a little introduction on how to play?". 
    Here are some examples to the answer is yes:
    "Có mình cần bạn giới thiệu" ,
    "Chắc chắn rồi mình rất cần",
    "Mình cần",
    "Cần",
    "Rất cần",
    "Được rồi",
    "Rất sẵn lòng",
    "Ok",
    "ok",
    "bạn nói đi",
    "cần mình cần",
    "có",
    "tất nhiên rồi",
    "Ok sao cũng được",
    "giới thiệu",
    "Vâng ạ",
    "vâng rất sẵn lòng",
    "vâng rất muốn nghe",
    "Mình rất muốn nghe",
    "Chắc chắn! Hãy giới thiệu cho tôi một ít về cách thức chơi để tôi có thể bắt đầu một cách hiệu quả.",
    "Vâng, tôi rất quan tâm đến cách thức chơi. Xin hãy chỉ dẫn tôi để tôi có thể làm quen với trò chơi.",
    "Cần một ít hướng dẫn để tôi có thể bắt đầu một cách đúng đắn. Xin hãy giúp tôi hiểu về cách thức chơi."

    Here are some examples to the answer is no:
    "Không",
    "Mình không cần cho lắm",
    "Mình không cần",
    "Chắc là không đâu",
    "Nói lẹ lẹ đi",
    "Mình rất muốn chơi bây giờ không cần thiết giới thiệu dài dòng",
    "Không cần, cảm ơn. Tôi đã tự tìm hiểu và có kiến thức về cách thức chơi rồi.",
    "Tôi đã có kinh nghiệm với trò chơi này nên không cần giới thiệu lại cách thức chơi.",
    "Xin lỗi, nhưng tôi đã biết cách chơi rồi. Tôi muốn khám phá những điều mới hơn."


    If you not sure then the answer is yes.
    remember only return yes or no and response in lowercase and without anyspace.
    Now the sentence is: {sentence}

"""


prompt = PromptTemplate(
    input_variables=["sentence"],
    template=template_knowmore,
)


chain = LLMChain(llm=llm, prompt=prompt)



import re

def process_result(result):
    # Convert the result to lowercase and remove spaces
    processed_result = result.lower().replace(" ", "")

    # Remove special characters using regular expression
    processed_result = re.sub(r'[^\w\s]', '', processed_result)

    return processed_result


# sentence = "chơi liền"
# result = chain.run(sentence)
# print(result)

# processed_result = process_result(result)

# print(processed_result)

def speech2command():
    sentence = speech2text()  # get the text from voice input
    result = chain.run(sentence)
    print(result)
    processed_result = process_result(result)
    print(processed_result)
    return processed_result
    

