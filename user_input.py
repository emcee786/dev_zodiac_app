
from pydantic import computed_field, ValidationError, BaseModel
from typing import Literal
from prefect import flow, pause_flow_run
from prefect.input import RunInput

ZODIAC_SIGNS = {
    "Aries": 1,
    "Taurus": 2,
    "Gemini": 3,
    "Cancer": 4,
    "Leo": 5,
    "Virgo": 6,
    "Libra": 7,
    "Scorpio": 8,
    "Sagittarius": 9,
    "Capricorn": 10,
    "Aquarius": 11,
    "Pisces": 12
}

class UserInput(RunInput):
    horoscope: Literal[
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces"]
    
    job_title: str

class UserInformation(BaseModel):
    horoscope: str
    job_title: str
    horoscope_number: int
    

    def __init__(self, user_input: UserInput):
        # Calculate the horoscope number before initializing
        horoscope_number = self.get_horoscope_number(user_input.horoscope)
        
        # Use Pydantic's BaseModel initialization
        super().__init__(
            horoscope=user_input.horoscope,
            job_title=user_input.job_title,
            horoscope_number=horoscope_number
        )

    @staticmethod
    def get_horoscope_number(horoscope: str) -> int:
        ZODIAC_SIGNS = {
            "Aries": 1, "Taurus": 2, "Gemini": 3, "Cancer": 4,
            "Leo": 5, "Virgo": 6, "Libra": 7, "Scorpio": 8,
            "Sagittarius": 9, "Capricorn": 10, "Aquarius": 11, "Pisces": 12
        }
        return ZODIAC_SIGNS[horoscope]
    
@flow(log_prints=True)
def get_user_input() -> UserInput:
    user_input = None

    while user_input is None:
        try:
            user_input = pause_flow_run(wait_for_input=UserInput)
            print(f"User_info: {user_input}")
        except ValidationError:
            print("Invalid info. Please try again.")
        return user_input

if __name__ == "__main__":
    get_user_input()
