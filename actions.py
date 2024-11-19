
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk.events import SessionStarted, ActionExecuted, EventType




class ActionGreetUser(Action):
    def name(self) -> Text:
        return "action_greet_user"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello! How can I assist you today?")
        return []

class ActionSavePatientDetails(Action):

    def name(self) -> Text:
        return "action_save_patient_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Extracting patient details
        name = tracker.get_slot("patient_name")
        insurance = tracker.get_slot("insurance_type")
        preferred_time = tracker.get_slot("preferred_time")

        # Save details to a database
        connection = sqlite3.connect('patients.db')
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS patients 
                          (name TEXT, insurance TEXT, preferred_time TEXT)''')
        cursor.execute("INSERT INTO patients (name, insurance, preferred_time) VALUES (?, ?, ?)",
                       (name, insurance, preferred_time))
        connection.commit()
        connection.close()

        dispatcher.utter_message(text="Your details have been saved. Thank you!")
        
        return []


class ActionClarifyPatientName(Action):
    def name(self) -> str:
        return "action_clarify_patient_name"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        dispatcher.utter_message(text="I didn't quite get the patient's full name. Could you please provide the first and last name?")
        return []




class ActionCustomFallback(Action):
    def name(self) -> str:
        return "action_custom_fallback"

    async def run(self, dispatcher, tracker, domain):
        # Check if patient name slots have been set
        patient_first_name = tracker.get_slot("patient_first_name")
        patient_last_name = tracker.get_slot("patient_last_name")

        if patient_first_name and patient_last_name:
            # If patient name entities are present, proceed without fallback
            dispatcher.utter_message(text=f"Got it, you're looking for services for {patient_first_name} {patient_last_name}.")
            return []
        else:
            # Default fallback response
            dispatcher.utter_message(text="I didn’t quite catch that. Could you please provide the patient's full name?")
            return [UserUtteranceReverted()]


class ActionAskContactDetails(Action):
    def name(self):
        return "action_ask_contact_details"

    def run(self, dispatcher, tracker, domain):
        # Custom logic to ask for contact details
        dispatcher.utter_message(text="Could you please provide a contact number or email?")
        return []



class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[EventType]:
        # Trigger the built-in session start event
        events = [SessionStarted()]
        
        # Send a greeting message at the start of each session
        dispatcher.utter_message(template="utter_greet")
        
        # Log the start of the session
        events.append(ActionExecuted("action_listen"))

        return events


class ValidateInsuranceCompany(Action):

    def name(self) -> Text:
        return "action_validate_insurance_company"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        in_network_companies = [
            "Premera", "Regence", "Kaiser", "Cigna", 
            "United Healthcare", "Aetna", "Blue Cross Blue Shield", "BCBS",
            "Blue Shield", "United", "Evergreen", "Group Health"
        ]
        out_of_network_companies = ["Apple Health", "DSHS", "Medicare", "Tricare", "Humana", "Ambetter", "Providence", "CHPW"]

        insurance = tracker.get_slot("insurance_company")

        if insurance in in_network_companies:
            dispatcher.utter_message(text=f"We are out-of-network with {insurance} but we can still bill them on your behalf. This means that you pay at the time of service, and your insurance reimburses you after.") 
 We're out-of-network with all private insurance companies, but we can bill them for you on your behalf. 
            return [SlotSet("insurance_company", insurance)]
        elif insurance in out_of_network_companies:
            dispatcher.utter_message(text=f"Unfortunately, we do not work with {insurance}. You will have to contact them to find a provider that is in their network.")
            return [SlotSet("insurance_company", None)]
        else:
            dispatcher.utter_message(text="I'm sorry, I didn't recognize that insurance company. Could you please repeat it?")
            return [SlotSet("insurance_company", None)]


