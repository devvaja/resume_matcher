# #
# import re
# import spacy
#
# # Load the English NLP model
# nlp = spacy.load("en_core_web_sm")
#
# class ParseResume:
#     def __init__(self, resume: str):
#         self.resume_data = resume
#         self.emails = self.extract_emails(self.resume_data)
#         self.phones = self.extract_phone_numbers(self.resume_data)
#         self.skills = self.extract_skills(self.resume_data)
#
#     def extract_emails(self, text):
#         email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
#         return re.findall(email_pattern, text)
#
#     def extract_phone_numbers(self, text):
#         phone_pattern = r"\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}"
#         return re.findall(phone_pattern, text)
#
#     def extract_skills(self, text):
#         skills = []
#         doc = nlp(text)
#         for token in doc:
#             if token.pos_ in ["NOUN", "PROPN"]:
#                 skills.append(token.text)
#         return list(set(skills))
#
#     def annotate_text(self):
#         annotated_text = self.resume_data
#         # Highlight emails
#         for email in self.emails:
#             annotated_text = annotated_text.replace(
#                 email, f'<span class="highlight-email">{email}</span>'
#             )
#         # Highlight phone numbers
#         for phone in self.phones:
#             annotated_text = annotated_text.replace(
#                 phone, f'<span class="highlight-phone">{phone}</span>'
#             )
#         # Highlight skills
#         for skill in self.skills:
#             annotated_text = annotated_text.replace(
#                 skill, f'<span class="highlight-skill">{skill}</span>'
#             )
#         return annotated_text
#
#     def get_JSON(self):
#         # Ensure the annotated text is being generated properly
#         annotated_text = self.annotate_text()  # Ensure the annotated text is generated here
#         return {
#             "resume_data": self.resume_data,
#             "annotated_text": annotated_text,
#             "emails": self.emails,
#             "phones": self.phones,
#             "skills": self.skills,
#         }
#
#
import json
import re
from .utils import TextCleaner, generate_unique_id,DataExtractor,KeytermExtractor



class ParseResume:
    def __init__(self, resume: str):
        self.resume_data = resume
        self.clean_data = TextCleaner.clean_text(self.resume_data)
        self.entities = DataExtractor(self.clean_data).extract_entities()
        self.name = DataExtractor(self.clean_data[:30]).extract_names()
        self.experience = DataExtractor(self.clean_data).extract_experience()
        self.emails = DataExtractor(self.resume_data).extract_emails()
        self.phones = DataExtractor(self.resume_data).extract_phone_numbers()
        self.years = DataExtractor(self.clean_data).extract_position_year()
        self.key_words = DataExtractor(self.clean_data).extract_particular_words()
        self.pos_frequencies = KeytermExtractor(self.clean_data).count_frequency()
        self.keyterms = KeytermExtractor(self.clean_data).get_keyterms_based_on_sgrank()
        self.bi_grams = KeytermExtractor(self.clean_data).bi_gramchunker()
        self.tri_grams = KeytermExtractor(self.clean_data).tri_gramchunker()

    def get_JSON(self) -> dict:
        return {
            "unique_id": generate_unique_id(),
            "resume_data": self.resume_data,
            "clean_data": self.clean_data,
            "entities": self.entities,
            "extracted_keywords": self.key_words,
            "keyterms": self.keyterms,
            "name": self.name,
            "experience": self.experience,
            "emails": self.emails,
            "phones": self.phones,
            "years": self.years,
            "bi_grams": str(self.bi_grams),
            "tri_grams": str(self.tri_grams),
            "pos_frequencies": self.pos_frequencies,
        }

from .utils import generate_unique_id,DataExtractor,TextCleaner, CountFrequency,KeytermExtractor


class ParseDocumentToJson:
    def __init__(self, doc: str, doc_type: str):
        self.years = None
        self.phones = None
        self.emails = None
        self.experience = None
        self.name = None
        self.doc_data = doc
        self.doc_type = doc_type
        self.clean_data = TextCleaner.clean_text(self.doc_data)
        self.entities = DataExtractor(self.clean_data).extract_entities()
        self.key_words = DataExtractor(self.clean_data).extract_particular_words()
        self.pos_frequencies = CountFrequency(self.clean_data).count_frequency()
        self.keyterms = KeytermExtractor(self.clean_data).get_keyterms_based_on_sgrank()
        self.bi_grams = KeytermExtractor(self.clean_data).bi_gramchunker()
        self.tri_grams = KeytermExtractor(self.clean_data).tri_gramchunker()
        if self.doc_type == "resume":
            self.get_additional_data()

    def get_additional_data(self):
        self.name = DataExtractor(self.clean_data[:30]).extract_names()
        self.experience = DataExtractor(self.clean_data).extract_experience()
        self.emails = DataExtractor(self.doc_data).extract_emails()
        self.phones = DataExtractor(self.doc_data).extract_phone_numbers()
        self.years = DataExtractor(self.clean_data).extract_position_year()

    def get_JSON(self) -> dict:
        doc_dictionary = {
            "unique_id": generate_unique_id(),
            "doc_data": self.doc_data,
            "clean_data": self.clean_data,
            "entities": self.entities,
            "extracted_keywords": self.key_words,
            "keyterms": self.keyterms,
            "bi_grams": str(self.bi_grams),
            "tri_grams": str(self.tri_grams),
            "pos_frequencies": self.pos_frequencies,
        }
        if self.doc_type == "resume":
            doc_dictionary.update(
                {
                    "name": self.name,
                    "experience": self.experience,
                    "emails": self.emails,
                    "phones": self.phones,
                    "years": self.years,
                }
            )
        return doc_dictionary




SAVE_DIRECTORY = "../../Data/Processed/JobDescription"


class ParseJobDesc:

    def __init__(self, job_desc: str):
        self.job_desc_data = job_desc
        self.clean_data = TextCleaner.clean_text(self.job_desc_data)
        self.entities = DataExtractor(self.clean_data).extract_entities()
        self.key_words = DataExtractor(self.clean_data).extract_particular_words()
        self.pos_frequencies = CountFrequency(self.clean_data).count_frequency()
        self.keyterms = KeytermExtractor(self.clean_data).get_keyterms_based_on_sgrank()
        self.bi_grams = KeytermExtractor(self.clean_data).bi_gramchunker()
        self.tri_grams = KeytermExtractor(self.clean_data).tri_gramchunker()

    def get_JSON(self) -> dict:
        """
        Returns a dictionary of job description data.
        """
        job_desc_dictionary = {
            "unique_id": generate_unique_id(),
            "job_desc_data": self.job_desc_data,
            "clean_data": self.clean_data,
            "entities": self.entities,
            "extracted_keywords": self.key_words,
            "keyterms": self.keyterms,
            "bi_grams": str(self.bi_grams),
            "tri_grams": str(self.tri_grams),
            "pos_frequencies": self.pos_frequencies,
        }

        return job_desc_dictionary







SAVE_DIRECTORY = "../../Data/Processed/Resumes"


class ParseResume:

    def __init__(self, resume: str):
        self.resume_data = resume
        self.clean_data = TextCleaner.clean_text(self.resume_data)
        self.entities = DataExtractor(self.clean_data).extract_entities()
        self.name = DataExtractor(self.clean_data[:30]).extract_names()
        self.experience = DataExtractor(self.clean_data).extract_experience()
        self.emails = DataExtractor(self.resume_data).extract_emails()
        self.phones = DataExtractor(self.resume_data).extract_phone_numbers()
        self.years = DataExtractor(self.clean_data).extract_position_year()
        self.key_words = DataExtractor(self.clean_data).extract_particular_words()
        self.pos_frequencies = CountFrequency(self.clean_data).count_frequency()
        self.keyterms = KeytermExtractor(self.clean_data).get_keyterms_based_on_sgrank()
        self.bi_grams = KeytermExtractor(self.clean_data).bi_gramchunker()
        self.tri_grams = KeytermExtractor(self.clean_data).tri_gramchunker()

    def get_JSON(self) -> dict:
        """
        Returns a dictionary of resume data.
        """
        resume_dictionary = {
            "unique_id": generate_unique_id(),
            "resume_data": self.resume_data,
            "clean_data": self.clean_data,
            "entities": self.entities,
            "extracted_keywords": self.key_words,
            "keyterms": self.keyterms,
            "name": self.name,
            "experience": self.experience,
            "emails": self.emails,
            "phones": self.phones,
            "years": self.years,
            "bi_grams": str(self.bi_grams),
            "tri_grams": str(self.tri_grams),
            "pos_frequencies": self.pos_frequencies,
        }

        return resume_dictionary







