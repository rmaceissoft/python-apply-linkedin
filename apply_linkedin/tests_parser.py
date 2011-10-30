import unittest
from datetime import date
import sys
sys.path.append('../') 

from apply_linkedin.parser import parse_application
from apply_linkedin.models import Application

def application_fixture():
    
    return """
        {
           "coverLetter":"To whom it may concern, I am very interested in this open position at your company.  I believe my skills and work experience make me an ideal candidate for this role.  I look forward to speaking with you soon about this position.  Thank you for your consideration.Best regards, Applicant name",
           "person":{
            "headline":"Vice President Marketing",
            "skills":{
             "values":[
              {
                 "id":14,
                 "skill":{
                  "name":"C++"
                 }
              },
              {
                 "id":15,
                 "skill":{
                  "name":"Java"
                 }
              }
             ],
             "_total":2
            },
            "lastName":"Hitchcock",
            "honors":"Mad Scientist of the Year, 1995 Marketing Bogusness Award, 2003",
            "location":{
             "postalCode":"94043",
             "name":"San Francisco Bay Area",
             "country":{
              "code":"us"
             }
            },
            "emailAddress":"alfred@linkedin.com",
            "id":"1",
            "publicProfileUrl":"http://www.linkedin.com/in/adamnash",
            "positions":{
             "values":[
              {
                 "summary":"Responsible for mergers and acquisitions at the company.",
                 "id":11,
                 "startDate":{
                  "month":1,
                  "year":1998
                 },
                 "title":"Vice President Mergers and Acquisitions",
                 "company":{
                  "id":1004,
                  "ticker":"PFE",
                  "name":"Pfizer",
                  "industry":"Pharmaceuticals",
                  "type":"Public Company"
                 },
                 "isCurrent":true
              },
              {
                 "summary":"Responsible for the overall marketing strategy.",
                 "id":1,
                 "startDate":{
                  "month":5,
                  "year":1997
                 },
                 "title":"Vice President Marketing",
                 "company":{
                  "id":1003,
                  "ticker":"DNA",
                  "name":"Genentech",
                  "industry":"Biotechnology",
                  "type":"Public Company",
                  "size":"5001-10,000 employees"
                 },
                 "isCurrent":true
              },
              {
                 "summary":"Responsible for the European marketing strategy. Successfully launched 5 products in 12 countries.",
                 "id":2,
                 "startDate":{
                  "month":2,
                  "year":1992
                 },
                 "title":"Director of Marketing - Europe",
                 "company":{
                  "id":1003,
                  "ticker":"DNA",
                  "name":"Genentech",
                  "industry":"Biotechnology",
                  "type":"Public Company",
                  "size":"5001-10,000 employees"
                 },
                 "endDate":{
                  "month":5,
                  "year":1997
                 },
                 "isCurrent":false
              }
             ],
             "_total":3
            },
            "languages":{
             "values":[
              {
                 "id":11,
                 "language":{
                  "name":"English"
                 }
              },
              {
                 "id":12,
                 "language":{
                  "name":"Russian"
                 }
              },
              {
                 "id":13,
                 "language":{
                  "name":"Spanish"
                 }
              }
             ],
             "_total":3
            },
            "publications":{
             "values":[
              {
                 "id":3,
                 "title":"Object-oriented analysis and design with applications, third edition, Third edition",
                 "date":{
                  "month":4,
                  "year":2007,
                  "day":6
                 }
              }
             ],
             "_total":1
            },
            "certifications":{
             "values":[
              {
                 "id":7,
                 "name":"CFA I"
              }
             ],
             "_total":1
            },
            "recommendationsReceived":{
             "values":[
              {
                 "id":1,
                 "recommendationType":{
                  "code":"colleague"
                 },
                 "recommender":{
                  "id":"2",
                  "lastName":"Willis",
                  "firstName":"Bruce"
                 },
                 "recommendationText":"Alfred did an amazing job there..."
              }
             ],
             "_total":1
            },
            "educations":{
             "values":[
              {
                 "id":101,
                 "startDate":{
                  "month":2,
                  "year":2008
                 },
                 "fieldOfStudy":"Mathematics",
                 "degree":"Ph.D.",
                 "schoolName":"University of Oregon",
                 "endDate":{
                  "month":5,
                  "year":2014
                 },
                 "activities":"Bird Dog Club, Beta Gamma Gamma"
              },
              {
                 "id":2,
                 "startDate":{
                  "year":1995
                 },
                 "fieldOfStudy":"Physics",
                 "degree":"Ph.D.",
                 "schoolName":"Stanford",
                 "endDate":{
                  "year":1998
                 },
                 "activities":"Quack Scientist Club, Gamma Gamma Gamma"
              },
              {
                 "id":1,
                 "startDate":{
                  "year":1993
                 },
                 "degree":"BSc",
                 "schoolName":"Stratfield University, Scotland",
                 "endDate":{
                  "year":1995
                 },
                 "activities":"Nerd Club"
              }
             ],
             "_total":3
            },
            "firstName":"Alfred",
            "patents":{
             "values":[
              {
                 "id":1,
                 "title":"System and Method for Data Entry into a Computing Device",
                 "date":{
                  "month":1,
                  "year":1999,
                  "day":1
                 }
              }
             ],
             "_total":1
            }
           },
           "questions":{
             "_total":2,
             "values":[
              {
               "answer":"",
               "question":"Do you have top secret clearance?"
              },
              {
               "answer":"true",
               "question":"Have you passed the Series 7 Exam?"
              }
             ]
           },
           "job":{
            "position":{
             "title":"CEO for manufacturing and supply sector"
            },
            "id":"1100",
            "company":{
             "name":"Nokia"
            }
           },
           "meta":"Apply with LinkedIn"
        }    
    """


class TestParserSuccess(unittest.TestCase):

    def test_init(self):
        json_application = application_fixture()
        self.assertRaises(Exception, parse_application(json_application))
        

class TestParser(unittest.TestCase):

    def setUp(self):
        self.application = parse_application(application_fixture())
                
    def test_parse_date_type(self):
        
        for position in self.application.person.positions:
            if position.startDate:
                self.assertTrue(isinstance(position.startDate, date))
            if position.endDate:
                self.assertTrue(isinstance(position.endDate, date))

        for education in self.application.person.educations:
            if education.startDate:
                self.assertTrue(isinstance(education.startDate, date))
                self.assertTrue(isinstance(education.endDate, date))
    
    
if __name__ == '__main__':
    unittest.main()
