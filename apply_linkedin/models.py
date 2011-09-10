from datetime import date
from apply_linkedin.utils import parse_meta, parse_date


class ResultSet(list):
    """A list like object that holds results from a Linkedin API calls."""

class Model(object):

    def __getstate__(self):
        # pickle
        pickle = dict(self.__dict__)
        return pickle
    
    def __getattr__(self, name):
        #invoken when refering to attribute that it is not valid or it was not present at json response
        return None 

    @classmethod
    def parse(cls, json):
        """Parse a JSON object into a model instance."""
        raise NotImplementedError
    
    @classmethod
    def parse_list(cls, json):
        results = ResultSet()
        results.total = json.get('_total')
        for obj in json.get('values', []):
            results.append(cls.parse(obj))
        return results
    
    
class Location(Model):
    
    @classmethod
    def parse(cls, json):
        location = cls()
        for k, v in json.items():
            if k == 'country':
                setattr(location, k, v.get('code'))
            else:
                setattr(location, k, v)
        return location


class Company(Model):
    
    @classmethod
    def parse(cls, json):
        company = cls()
        for k, v in json.items():
            setattr(company, k, v)
        return company
            
    
class Job(Model):
    
    @classmethod
    def parse(cls, json):
        job = cls()
        for k, v in json.items():
            if k == 'company':
                setattr(job, k, Company.parse(v))
            elif k == 'position':
                setattr(job, k, Position.parse(v))
            else:
                setattr(job, k, v)
        return job
            

class PositionResultSet(ResultSet):
    
    _cached_current_position = None
    _cached_first_position = None
    
    @property
    def current_position(self):
        """iterate over all position looking for what is current
        """
        if not self._cached_current_position:
            for position in self:
                if position.isCurrent:
                    self._cached_current_position = position
        return self._cached_current_position
    
    @property
    def first_position(self):
        if not self._cached_first_position:
            max_start_date = date.today()
            for position in self:
                if position.startDate and position.startDate < max_start_date:
                    max_start_date = position.startDate
                    self._cached_first_position = position
        return self._cached_first_position
     
            
class Position(Model):
    
    @classmethod
    def parse(cls, json):
        position = cls()
        for k, v in json.items():
            if k == 'company':
                setattr(position, k, Company.parse(v))
            elif k in ['startDate', 'endDate']:
                setattr(position, k, parse_date(v))
            else:
                setattr(position, k, v)
        return position

    @classmethod
    def parse_list(cls, json):
        results = PositionResultSet()
        results.total = json.get('_total')
        for obj in json.get('values', []):
            results.append(cls.parse(obj))
        return results


class Education(Model):
    
    @classmethod
    def parse(cls, json):
        education = cls()
        for k, v in json.items():
            if k in ['startDate', 'endDate']:
                setattr(education, k, parse_date(v))
            else:
                setattr(education, k, v)
        return education


class Skill(Model):
    
    @classmethod
    def parse(cls, json):
        skill = cls()
        for k, v in json.items():
            if k == 'skill':
                setattr(skill, 'name', v.get('name'))
            else:
                setattr(skill, k, v)
        return skill
    
    
class PhoneNumber(Model):
    
    @classmethod
    def parse(cls, json):
        phone_number = cls()
        for k, v in json.items():
            setattr(phone_number, k, v)
        return phone_number
        
        
class Language(Model):
    
    @classmethod
    def parse(cls, json):
        language = cls()
        for k, v in json.items():
            if k == 'language':
                setattr(language, 'name', v.get('name', ''))
            else:
                setattr(language, k, v)  
        return language
    
    
class RecommendationType(Model):
    
    @classmethod
    def parse(cls, json):
        recommendation_type = cls()
        for k, v in json.items():
            setattr(recommendation_type, k, v)
        return recommendation_type    

    
class Recommender(Model):    

    @classmethod
    def parse(cls, json):
        recommender = cls()
        for k, v in json.items():
            setattr(recommender, k, v)
        return recommender   
             
    
class Recommendation(Model):
    
    @classmethod
    def parse(cls, json):
        recommendation = cls()
        for k, v in json.items():
            if k == 'recommendationType':
                setattr(recommendation, k, RecommendationType.parse(v))
            elif k == 'recommender':  
                setattr(recommendation, k, Recommender.parse(v))
            else:
                setattr(recommendation, k, v)
        return recommendation
                

class Person(Model):
    
    @classmethod
    def parse(cls, json):
        person = cls()
        for k, v in json.items():
            if k == 'positions':
                setattr(person, k, Position.parse_list(v))
            elif k == 'educations':
                setattr(person, k, Education.parse_list(v))
            elif k == 'skills':
                setattr(person, k, v)
            elif k == 'phoneNumbers':
                setattr(person, k, PhoneNumber.parse_list(v))
            elif k == 'languages':
                setattr(person, k, Language.parse_list(v))
            elif k == 'location':
                setattr(person, k, Location.parse(v))
            elif k == 'recommendationsReceived':
                setattr(person, k, Recommendation.parse_list(v))
            else:
                setattr(person, k, v)
        return person
    
class Application(Model):
    
    @classmethod
    def parse(cls, json):
        application = cls()
        for k, v in json.items():
            if k == 'meta':
                setattr(application, k, parse_meta(v))
            elif k == 'job':
                setattr(application, k, Job.parse(v))
            elif k == 'person':
                setattr(application, k, Person.parse(v))
            else:
                setattr(application, k, v)
        return application
