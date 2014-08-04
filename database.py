# -*- coding: utf-8 -*-
# database.py - Classes for loading data from Coh-Metrix-Port's database.
# Copyright (C) 2014  Andre Luiz Verucci da Cunha
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy import create_engine as _create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

DEFAULT_OPTIONS = {
    'dialect': 'postgresql',
    'driver': 'psycopg2',
    'username': 'cohmetrix',
    'password': 'cohmetrix',
    'host': 'localhost',
    'port': '5432',
    'database': 'cohmetrix_pt_br',
}


def create_engine(options=DEFAULT_OPTIONS, echo=False):
    connect_string =\
        '{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}'\
        .format(**options)
    return _create_engine(connect_string, echo=echo)


def create_session(engine):
    return sessionmaker(bind=engine)()


class DelafVerb(Base):
    __tablename__ = 'delaf_verbs'

    word = Column(String, primary_key=True)
    lemma = Column(String, primary_key=True)
    tense = Column(String, primary_key=True)
    person = Column(String, primary_key=True)

    def __str__(self):
        return '<DelafVerb: word={0}, lemma={1}, tense={2}, person={3}>'\
            .format(self.word, self.lemma, self.tense, self.person)


class Frequency(Base):
    __tablename__ = 'frequencies'

    id = Column(Integer, primary_key=True)
    word = Column(String)
    freq = Column(Integer)
    freq_perc = Column(Float)
    texts = Column(Integer)
    texts_perc = Column(Float)

    def __str__(self):
        return '<Frequency: word=%s, freq=%s, freq_perc=%s, texts=%s, texts_perc=%s>'\
            % (self.word, str(self.freq), str(self.freq_perc), str(self.texts),
               str(self.texts_perc))


class Hypernym(Base):
    __tablename__ = 'hypernyms_verbs'

    word = Column(String, primary_key=True)
    category = Column(String, primary_key=True)
    grammar_attrs = Column(String)
    hyper_levels = Column(Integer)

    def __str__(self):
        return '<Hypernym: word={0}, cat={1}, attrs={2}, levels={3}>'\
            .format(self.word, self.category, self.grammar_attrs,
                    self.hyper_levels)


class Helper(object):

    def __init__(self, session):
        """@todo: Docstring for __init__.

        :session: @todo
        :returns: @todo

        """
        self._session = session

    def get_frequency(self, word):
        return self._session.query(Frequency).filter_by(word=word).first()

    def get_hypernyms(self, verb):
        """@todo: Docstring for get_hypernyms.

        :verb: @todo
        :returns: @todo

        """
        return self._session.query(Hypernym).filter_by(word=verb).first()

    def get_verb(self, verb):
        """@todo: Docstring for get_verb.

        :verb: @todo
        :returns: @todo

        """
        return self._session.query(DelafVerb).filter_by(word=verb).first()

if __name__ == '__main__':
    engine = create_engine()
    session = create_session(engine)
    helper = Helper(session)

    print(helper.get_frequency('abacaxi'))
    print(helper.get_frequency('maçã'))
    print(helper.get_hypernyms('dar'))
    print(helper.get_hypernyms('abalançar'))
    print(helper.get_verb('apareceu'))
    print(helper.get_verb('abraçarão'))
