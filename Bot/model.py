import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, SimpleRNN, Dense

class ChatbotModel:
    def __init__(self, data_path, model_path=None):
        self.tokenizer = Tokenizer()
        self.max_sequence_len = 100

        # Ensure the model directory exists
        self.model_dir = os.path.dirname(model_path)
        if self.model_dir and not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)

        # Load data first to get total_words
        self._load_data(data_path)

        if model_path and os.path.exists(model_path):
            self.model = self._load_model(model_path)
        else:
            self.model = self._build_model()
            self._train_model()
            self._save_model(model_path)

    def _load_data(self, data_path):
        with open(data_path, 'r', encoding='utf-8') as file:  # Specify utf-8 encoding
            self.text = file.read()
        self.tokenizer.fit_on_texts([self.text])
        self.total_words = len(self.tokenizer.word_index) + 1

        input_sequences = []
        for line in self.text.split('\n'):
            token_list = self.tokenizer.texts_to_sequences([line])[0]
            for i in range(1, len(token_list)):
                n_gram_sequence = token_list[:i+1]
                input_sequences.append(n_gram_sequence)

        self.max_sequence_len = max([len(x) for x in input_sequences])
        input_sequences = np.array(pad_sequences(input_sequences, maxlen=self.max_sequence_len, padding='pre'))
        self.predictors, self.label = input_sequences[:,:-1], input_sequences[:,-1]
        self.label = tf.keras.utils.to_categorical(self.label, num_classes=self.total_words)

    def _build_model(self):
        model = Sequential()
        model.add(Embedding(self.total_words, 100, input_length=self.max_sequence_len-1))
        model.add(SimpleRNN(150))
        model.add(Dense(self.total_words, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        return model

    def _train_model(self):
        self.model.fit(self.predictors, self.label, epochs=100, verbose=1)

    def _save_model(self, model_path):
        if model_path:
            self.model.save(model_path)

    def _load_model(self, model_path):
        return load_model(model_path)

    def generate_text(self, seed_text, next_words):
        for _ in range(next_words):
            token_list = self.tokenizer.texts_to_sequences([seed_text])[0]
            token_list = pad_sequences([token_list], maxlen=self.max_sequence_len-1, padding='pre')
            predicted = np.argmax(self.model.predict(token_list), axis=-1)
            output_word = ""
            for word, index in self.tokenizer.word_index.items():
                if index == predicted:
                    output_word = word
                    break
            seed_text += " " + output_word
        return seed_text
