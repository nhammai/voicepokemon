import pyaudio
import os
import time
import pyaudio
import wave
import pygame
import speech_recognition as sr


def playSound(filename):
    pygame.init()

    # Load the audio file
    
    pygame.mixer.music.load(filename)

    # Play the audio file
    pygame.mixer.music.play()

    # Wait for the audio to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)



# Initialize recognizer
recognizer = sr.Recognizer()




def speech2text():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 3
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')
    playSound("sounds/listening.mp3")

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()


    playSound("sounds/done.mp3")

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Load the audio file
    with sr.AudioFile('dien.wav') as source:
        audio = recognizer.record(source)

    # Transcribe the audio using Google Web Speech API
    try:
        result = recognizer.recognize_google(audio, language='vi-VN')
        print("Transcript: ", result)

    except sr.UnknownValueError:
        print("Google Web Speech API could not understand the audio")
    except sr.RequestError as e:
        print(f"Error: {e}")


    

    return result

    
# k = speech2text()


