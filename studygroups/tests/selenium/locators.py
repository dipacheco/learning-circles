from selenium.webdriver.common.by import By

class LearningCircleCreationPageLocators(object):
    FIRST_COURSE_BUTTON = (By.CSS_SELECTOR, ".result-item .primary-cta button:first-of-type")
    REMOVE_COURSE_SELECTION_LINK = (By.LINK_TEXT, "Remove selection")
    NEXT_TAB_BUTTON = (By.CSS_SELECTOR, ".action-bar button.next-tab")
    CITY_SELECT = (By.CSS_SELECTOR, ".city-select .Select-input input")
    CITY_SELECT_INPUT = (By.CSS_SELECTOR, ".city-select .Select-input input")
    CITY_SELECT_OPTION = (By.CSS_SELECTOR, ".Select-menu-outer .Select-option")
    TAB_1 = (By.CSS_SELECTOR, "#react-tabs-0")
    TAB_1_TITLE = (By.CSS_SELECTOR, "#react-tabs-1 h4")
    TAB_2 = (By.CSS_SELECTOR, "#react-tabs-2")
    TAB_2_TITLE = (By.CSS_SELECTOR, "#react-tabs-3 h4")
    TAB_3 = (By.CSS_SELECTOR, "#react-tabs-4")
    TAB_3_TITLE = (By.CSS_SELECTOR, "#react-tabs-5 h4")
    TAB_4 = (By.CSS_SELECTOR, "#react-tabs-6")
    TAB_4_TITLE = (By.CSS_SELECTOR, "#react-tabs-7 h4")
    TAB_5 = (By.CSS_SELECTOR, "#react-tabs-8")
    TAB_5_TITLE = (By.CSS_SELECTOR, "#react-tabs-9 h4")
    VENUE_NAME_FIELD = (By.ID, "id_venue_name")
    VENUE_DETAILS_FIELD = (By.ID, "id_venue_details")
    VENUE_ADDRESS_FIELD = (By.ID, "id_venue_address")
    START_DATE_FIELD = (By.ID, "id_start_date")
    WEEKS_FIELD = (By.ID, "id_weeks")
    MEETING_TIME_FIELD = (By.NAME, "meeting_time")
    MEETING_TIME_INPUT = (By.CSS_SELECTOR, ".rc-time-picker-panel-input")
    DURATION_FIELD = (By.ID, "id_duration")
    DESCRIPTION_FIELD = (By.ID, "id_description")
    SIGNUP_QUESTION_FIELD = (By.ID, "id_signup_question")
    VENUE_WEBSITE_FIELD = (By.ID, "id_venue_website")
    FACILITATOR_GOAL_FIELD = (By.ID, "id_facilitator_goal")
    FACILITATOR_CONCERNS_FIELD = (By.ID, "id_facilitator_concerns")
    SUCCESS_ALERT = (By.CSS_SELECTOR, ".alert.alert-success")
    DANGER_ALERT = (By.CSS_SELECTOR, ".alert.alert-danger")
    ALERT_CLOSE_BUTTON = (By.CSS_SELECTOR, ".alert.alert-dismissible button.close")
    COURSE_CARDS = (By.CSS_SELECTOR, "#react-tabs-1 .search-results .result-item")
    PUBLISH_BUTTON = (By.CSS_SELECTOR, ".action-bar button.publish")
    SAVE_BUTTON = (By.CSS_SELECTOR, ".action-bar button.save")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".error-message.minicaps")


class RegistrationModalLocators(object):
    REGISTRATION_MODAL = (By.CSS_SELECTOR, ".registration-modal")
    REGISTRATION_MODAL_TITLE = (By.CSS_SELECTOR, ".registration-modal-content h4")
    MODAL_OVERLAY = (By.CSS_SELECTOR, ".modal-overlay")
    EMAIL_FIELD = (By.ID, "id_email")
    PASSWORD_FIELD = (By.ID, "id_password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, ".modal-actions button[type=submit]")

