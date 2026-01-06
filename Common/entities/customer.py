from Common.entities.Enums.gender import Gender

class Customer:
    def __init__(self,id,firstname,lastname,national_code,phon_number,email,birth_date,gender):
        self.customer_id=id
        self.firstname = firstname
        self.lastname = lastname
        self.national_code = national_code
        self.phon_number = phon_number
        self.email = email
        self.birth_date = birth_date
        self.gender = Gender(gender)


    @classmethod
    def create_with_dict(cls,dic_data):
        return cls(
            dic_data.get("customer_id"),
            dic_data.get("First_Name"),
            dic_data.get("Last_Name"),
            dic_data.get("NationalCode"),
            dic_data.get("PhonNumber"),
            dic_data.get("Email"),
            dic_data.get("BirthDate"),
            dic_data.get("Gender"),
        )
