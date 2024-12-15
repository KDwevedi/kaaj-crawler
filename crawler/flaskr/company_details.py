# Define a data structure to store the extracted details
class CompanyDetails:
    def __init__(self):
        self.entity_name = ""
        self.corporation_type = ""
        self.filing_information = {}
        self.principal_address = ""
        self.mailing_address = ""
        self.registered_agent = {}
        self.officers_directors = []

    def __repr__(self):
        return str(self.__dict__)
    
    def to_dict(self):
        return {
            "entity_name": self.entity_name,
            "corporation_type": self.corporation_type,
            "filing_information": self.filing_information,
            "principal_address": self.principal_address,
            "mailing_address": self.mailing_address,
            "registered_agent": self.registered_agent,
            "officers_directors": self.officers_directors,
        }
