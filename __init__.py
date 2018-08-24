# TODO: Add an appropriate license to your skill before publishing.  See
# the LICENSE file for more information.

# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG
import json
import requests


# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

# TODO: Change "Template" to a unique name for your skill
class TemplateSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(TemplateSkill, self).__init__(name="TemplateSkill")
        
        # Initialize working variables used within the skill.
        self.count = 0

    '''def initialize(self):
        # Creating GreetingsIntent requiring Greetings vocab
        patients = IntentBuilder("ReadPatientIntent").require("Patient").require.("name").build()
        self.register_intent(patients,self.handle_patient_read)'''
        # Associating a callback with the Intent



    @intent_handler(IntentBuilder("").require("Patient").require("firstname").require("lastname"))
    def handle_total_patient(self,message):
        firstname = message.data['firstname']
        lastname = message.data['lastname']
        url = 'http://hapi.fhir.org/baseDstu3/Patient?phonetic='+firstname+'&'+'phonetic='+lastname+'&_pretty=true'
        response = requests.get(url)
        json_data = json.loads(response.text)
        total = json_data['total']
        
        self.speak_dialog("TotalPatient",data={"total" : total})


    @intent_handler(IntentBuilder("").require("PatientFilter").require("firstname").require("lastname").require("birthyear"))
    def handle_total_patient(self,message):
        firstname = message.data['firstname']
        lastname = message.data['lastname']
        birthyear = message.data['birthyear']
        url = 'http://hapi.fhir.org/baseDstu3/Patient?phonetic='+firstname+'&'+'phonetic='+lastname+'&_pretty=true'
        response = requests.get(url)
        json_data = json.loads(response.text)
        f = 0
        
        for x in range(len(json_data['entry'])):
            keys = json_data['entry'][x]['resource'].keys()
            if "birthDate" in keys:
                year = json_data['entry'][x]['resource']['birthDate'].split('-')[0]
                if(year == birthyear):
                    f = 1
                    gender = json_data['entry'][x]['resource']['gender']
                    break
        if(f==1):
            self.speak_dialog("PatintDetail",data={"gender" : gender})
        else:
            self.speak_dialog("PatintNotFound")





        

    

    





		# Sending a command to mycroft, speak Greetings Dialog


    # The "handle_xxxx_intent" function is triggered by Mycroft when the
    # skill's intent is matched.  The intent is defined by the IntentBuilder()
    # pieces, and is triggered when the user's utterance matches the pattern
    # defined by the keywords.  In this case, the match occurs when one word
    # is found from each of the files:
    #    vocab/en-us/Hello.voc
    #    vocab/en-us/World.voc
    # In this example that means it would match on utterances like:
    #   'Hello world'
    #   'Howdy you great big world'
    #   'Greetings planet earth'
    '''@intent_handler(IntentBuilder("").require("Hello").require("World"))
    def handle_hello_world_intent(self, message):
        # In this case, respond by simply speaking a canned response.
        # Mycroft will randomly speak one of the lines from the file
        #    dialogs/en-us/hello.world.dialog
        self.speak_dialog("hello.world")

    @intent_handler(IntentBuilder("").require("Count").require("Dir"))
    def handle_count_intent(self, message):
        if message.data["Dir"] == "up":
            self.count += 1
        else:  # assume "down"
            self.count -= 1
        self.speak_dialog("count.is.now", data={"count": self.count})'''

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return TemplateSkill()
