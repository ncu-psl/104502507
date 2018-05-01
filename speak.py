import speech_recognition

options = ['創建矩陣', '轉置', '行列式', '反矩陣', ]
functions = ['self.matrix_row_col()', 'self.dotranspose()', 'self.matrixdeterminate()', 'self.matrixinverse()']

def speak():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)

    msg = r.recognize_google(audio, language='zh-TW')
    print(msg)

    for i in range(len(options)):
        if options[i] in msg:
            return i
        else:
            return -1