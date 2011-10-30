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
        instance = cls()
        for k, v in json.items():
            if hasattr(cls, 'extra_values') and k in cls.extra_values:
                func = cls.extra_parsers[k]
                setattr(instance, k, func(v))
            else:
                setattr(instance, k, v)
    
    @classmethod
    def parse_list(cls, json):
        results = ResultSet()
        results.total = json.get('_total')
        for obj in json.get('values', []):
            results.append(cls.parse(obj))
        return results
    
    
class Location(Model):
    
    extra_parsers = {
        'country' : lambda v : v.get('code')
    }
    

class Company(Model):
    pass
    
        
class Job(Model):
    
    extra_parsers = {
        'company' : lambda v : Company.parse(v),
        'position' : lambda v : Position.parse(v)
    }
    
    
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

    extra_parsers = {
        'company' : lambda v : Company.parse(v),
        'startDate' : lambda v : parse_date(v),
        'endDate' : lambda v : parse_date(v),
    }
        
    @classmethod
    def parse_list(cls, json):
        results = PositionResultSet()
        results.total = json.get('_total')
        for obj in json.get('values', []):
            results.append(cls.parse(obj))
        return results


class Education(Model):
    
    extra_parsers = {
        'startDate' : lambda v : parse_date(v),
        'endDate' : lambda v : parse_date(v),
    }
    

class Skill(Model):

    extra_parsers = {
        'skill' : lambda v : v.get('name'),
    }
    
    
class PhoneNumber(Model):
    pass
    
        
class Language(Model):
    
    extra_parsers = {
        'language' : lambda v : v.get('name'),
    }

  
class RecommendationType(Model):
    pass

    
class Recommender(Model):
    pass    

             
class Recommendation(Model):
    
    extra_parsers = {
        'recommendationType' : lambda v : RecommendationType.parse(v),
        'recommender' : lambda v : Recommender.parse(v),
    }

class Person(Model):
    
    extra_parsers = {
        'positions' : lambda v : Position.parse_list(v),
        'educations' : lambda v : Education.parse_list(v),
        'skills' : lambda v : Skill.parse_list(v),
        'phoneNumbers' : lambda v : PhoneNumber.parse_list(v),
        'languages' : lambda v : Language.parse_list(v),
        'location' : lambda v : Location.parse(v),
        'recommendationsReceived' : lambda v : Recommendation.parse_list(v),
    }

    
class Application(Model):
    
    extra_parsers = {
        'meta' : lambda v : parse_meta(v),
        'job' : lambda v : Job.parse(v),
        'person' : lambda v : Person.parse(v)
    }