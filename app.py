from prefect import flow, get_run_logger
from scrape_sign import get_horoscope_by_month
from generate_dev_response import rewrite_horoscope_as_dev
from user_input import get_user_input, UserInformation


@flow()
def get_dev_horoscope():
    logger = get_run_logger()
    logger.info("Prompting user for information")  
    user_input = get_user_input()
    user_info = UserInformation(user_input)
    logger.info(f"Fetching monthly horoscope")
    og_horoscope = get_horoscope_by_month(user_info.horoscope_number)
    logger.info(f"Rewriting horoscope")
    dev_horoscope = rewrite_horoscope_as_dev(og_horoscope, user_input.job_title)
    print(dev_horoscope)
    


if __name__ == "__main__":
    get_dev_horoscope()