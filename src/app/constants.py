from enum import StrEnum


class SystemLanguage(StrEnum):
    KAZAKH = 'kazakh'
    RUSSIAN = 'russian'
    ENGLISH = 'english'


class EnglishLevel(StrEnum):
    BEGINNER = 'beginner'
    ELEMENTARY = 'elementary'
    INTERMEDIATE = 'intermediate'
    UPPER_INTERMEDIATE = 'upper intermediate'
    ADVANCED = 'advanced'


class QuestionType(StrEnum):
    FILL_GAP = "fill_gap"  # Вставить пропущенное слово
    TRANSLATE = "translate"  # Перевод предложения
    MATCH_PAIRS = "match_pairs"  # Соединить слова (кот - cat)


class TrainingType(StrEnum):
    SPEAKING = "speaking"
    WRITING = "writing"
