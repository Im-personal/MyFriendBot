import tensorflow as tf
from tensorflow import keras
from keras.layers import Input, Embedding, LSTM, Dense
import numpy as np
from chatParser import json_chat_parser  # мой модуль, не удалять!

# Загрузка диалога из файла JSON
dialogue = json_chat_parser(r"C:\Users\Ilia-\Downloads\Telegram Desktop\ChatExport_2023-03-02 (1)\result.json")
dialogue = dialogue.get_chat_array()

print(len(dialogue))
# Предварительная обработка данных
questions = []
answers = []
for i in range(len(dialogue)):
    if i % 2 == 0:  # четные элементы - вопросы
        questions.append(dialogue[i].replace(':', '').lower())
    else:  # нечетные элементы - ответы
        answers.append(dialogue[i].lower())

if len(answers) > len(questions):
    answers.pop()
if len(answers) < len(questions):
    questions.pop()

# Создание словаря слов
tokenizer = keras.preprocessing.text.Tokenizer(filters='')
tokenizer.fit_on_texts(questions + answers)

# Преобразование входных данных в последовательности чисел
question_sequences = tokenizer.texts_to_sequences(questions)
answer_sequences = tokenizer.texts_to_sequences(answers)

# Создание обучающих данных (входные последовательности и соответствующие выходные последовательности)
# Создание обучающих данных (входные последовательности и соответствующие выходные последовательности)
X = []
y = []
for i in range(len(question_sequences)):
    for j in range(1, len(answer_sequences[i])):
        X.append(question_sequences[i])
        y.append(answer_sequences[i][j])

# Добавление заполнителя до одинаковой длины входных и выходных последовательностей
max_len = max(len(x) for x in X)
if isinstance(y[0], int):  # если y содержит только одно число
    y = [y]  # добавляем его в список в качестве элемента
X = keras.preprocessing.sequence.pad_sequences(X, padding='post', maxlen=max_len)
y = keras.preprocessing.sequence.pad_sequences(y, padding='post', maxlen=max_len)


# Создание модели
vocab_size = len(tokenizer.word_index) + 1
embedding_dim = 256
lstm_units = 512

inputs = Input(shape=(max_len,))
x = Embedding(vocab_size, embedding_dim)(inputs)
x, state_h, state_c = LSTM(lstm_units, return_sequences=True, return_state=True)(x)
output = Dense(vocab_size, activation='softmax')(x)

model = keras.Model(inputs=inputs, outputs=output)

# Компиляция и обучение модели
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
model.fit(X, y, batch_size=64, epochs=10)

# Сохранение модели
model.save('Artembot')

# Загрузка модели
model = keras.models.load_model('Artembot')

# Общение с моделью
while True:
    x = input(">> ")
    x_seq = tokenizer.texts_to_sequences([x.lower()])
    x_seq = keras.preprocessing.sequence.pad_sequences(x_seq, padding='post', maxlen=X.shape[1])
    result = np.argmax(model.predict(x_seq), axis=-1)
    result = tokenizer.sequences_to_texts([result])[0]
    print(result)
