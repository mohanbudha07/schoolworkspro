from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    classroom = relationship("ClassRoom", back_populates="students")
    quizzes = relationship("Quiz", back_populates="teacher")
    attempts = relationship("Attempt", back_populates="student")


class ClassRoom(Base):
    __tablename__ = "classes"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    students = relationship("User", back_populates="classroom")
    subjects = relationship("Subject", back_populates="classroom")


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"))
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    classroom = relationship("ClassRoom", back_populates="subjects")
    topics = relationship("Topic", back_populates="subject")
    quizzes = relationship("Quiz", back_populates="subject")


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    subject = relationship("Subject", back_populates="topics")
    questions = relationship("Question", back_populates="topic")


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    difficulty = Column(Integer, default=2)
    qtype = Column(String, default="mcq")
    prompt = Column(Text, nullable=False)
    options_json = Column(Text, nullable=True)
    answer = Column(String, nullable=False)
    explanation = Column(Text, nullable=True)
    generated = Column(Boolean, default=False)
    topic = relationship("Topic", back_populates="questions")


class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    teacher_id = Column(Integer, ForeignKey("users.id"))
    due_date = Column(DateTime, nullable=True)
    published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    subject = relationship("Subject", back_populates="quizzes")
    teacher = relationship("User", back_populates="quizzes")
    items = relationship("QuizItem", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("Attempt", back_populates="quiz")


class QuizItem(Base):
    __tablename__ = "quiz_items"
    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    quiz = relationship("Quiz", back_populates="items")
    question = relationship("Question")


class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=True)
    kind = Column(String, default="quiz")
    answers_json = Column(Text)
    score = Column(Float, default=0)
    max_score = Column(Float, default=0)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    student = relationship("User", back_populates="attempts")
    quiz = relationship("Quiz", back_populates="attempts")
    item_results = relationship("AttemptItem", back_populates="attempt", cascade="all, delete-orphan")


class AttemptItem(Base):
    __tablename__ = "attempt_items"
    id = Column(Integer, primary_key=True)
    attempt_id = Column(Integer, ForeignKey("attempts.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    given_answer = Column(String)
    correct = Column(Boolean, default=False)
    difficulty = Column(Integer, default=2)
    attempt = relationship("Attempt", back_populates="item_results")


class Mastery(Base):
    __tablename__ = "mastery"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    score = Column(Float, default=0.4)
    attempts_count = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint("user_id", "topic_id", name="uq_user_topic"),)
