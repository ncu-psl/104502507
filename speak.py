import speech_recognition

options = [
    '宣告矩陣',
    '轉置矩陣',
    '行列式',
    '反矩陣',
    '微分',
    '積分',
    '極值',
    '畫圖',
    '繪圖',
]

functions = [
    'self.matrix_row_col()',
    'self.matrixtranspose()',
    'self.matrixdeterminate()',
    'self.matrixinverse()',
    'self.differentation()',
    'self.integration()',
    'self.limit_gui()',
    'self.plot()',
    'self.plot()',
]

def speak():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)

    # msg = r.recognize_bing(audio, 'b141844071b7403ab26ea67e8f590a3f', language='zh-TW')
    msg = r.recognize_google(audio, language='zh-TW')
    print(msg)

    for i in range(len(options)):
        if options[i] in msg:
            return i
    return -1

# speak()