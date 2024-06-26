# disable the line length check for this file
# pylint: disable=C0301

""" Helper functions for the application """

import json
# pylint: disable=import-error
from bs4 import BeautifulSoup, Tag # type: ignore
from ..types.generate_cv import ParsedCvHTML, Experience

def extract_data_from_request(html: str, email_to: str, profile_url: str):
    """ Extract data from a request. """

    parsed_data = parse_html_to_event_schema(html)
    parsed_data.email_to = email_to
    parsed_data.profile_url = profile_url
    return json.dumps(parsed_data.to_dict(), indent=4)

def save_local_file(html: str, name: str):
    """ Save a local file. """

    with open(f'{name}.html', 'w', encoding='utf-8') as file:
        file.write(html)
    return 'success'

def parse_html_to_event_schema(html: str) -> ParsedCvHTML:
    """ Parse HTML to JSON. """

    soup = BeautifulSoup(html, 'html.parser')

    profile_name = ''
    name_element = soup.find('title')
    if name_element is not None:
        profile_name = name_element.text.strip().replace(' | LinkedIn', '')

    heading = ''
    heading_element = soup.find(
        class_='artdeco-entity-lockup__subtitle ember-view truncate',
    )
    if heading_element is not None:
        heading = heading_element.text.strip()

    resume = ''
    resume_section_parent = soup.find(
        'div',
        class_='display-flex ph5 pv3'
    )

    if isinstance(resume_section_parent, Tag):
        resume_section = resume_section_parent.find(
            'span',
            class_='visually-hidden'
        )

        if isinstance(resume_section, Tag):
            resume = resume_section.text.strip()

    profile_photo: str = ''
    logged_user_profile_photo_element = soup.find(
        class_='evi-image ember-view profile-photo-edit__preview'
    )
    if isinstance(logged_user_profile_photo_element, Tag):
        src = logged_user_profile_photo_element.get('src')
        if isinstance(src, str):
            profile_photo = src
    else:
        profile_photo_element = soup.find(
            'img',
            class_='pv-top-card-profile-picture__image--show'
        )
        if isinstance(profile_photo_element, Tag):
            src = profile_photo_element.get('src')
            if isinstance(src, str):
                profile_photo = src

    experiences = collect_experiences(soup)

    parsed_html = ParsedCvHTML(
        profile_name=profile_name,
        heading=heading,
        resume=resume,
        experiences=experiences,
        profile_photo=profile_photo,
        email_to='',
        profile_url='',
    )

    return parsed_html

def get_ul_of_experiences(soup: BeautifulSoup) -> Tag | None:
    """ Get the ul of experiences. from the HTML."""
    existing_uls = soup.find_all(
            'ul',
        )

    for ul in existing_uls:
        a_experience = ul.find('a', attrs={'data-field': 'experience_company_logo'})
        if isinstance(a_experience, Tag):
            return ul

    return None

def collect_experiences(soup: BeautifulSoup) -> list[Experience]:
    """ Collect experiences from HTML. """

    experiences_ul = get_ul_of_experiences(soup)

    if experiences_ul is None:
        return []

    experience_items = experiences_ul.find_all(
        'li',
        class_='artdeco-list__item'
    )

    if len(experience_items) == 0:
        return []

    experiences: list[Experience] = []

    for ei in experience_items:
        company=''
        company_logo=''
        title=''
        date_range:str=''
        description=''

        sub_soup = BeautifulSoup(str(ei), 'html.parser')
        title_container = sub_soup.find(
            'div',
            class_='display-flex align-items-center mr1 t-bold'
        )
        if title_container is not None:
            title_element =  title_container.find('span')
            if isinstance(title_element, Tag):
                title = title_element.text.strip()

        company_logo_element = sub_soup.find(
            'img',
            class_='ivm-view-attr__img--centered EntityPhoto-square-3 evi-image lazy-image ember-view'
        )
        if isinstance(company_logo_element, Tag):
            src = company_logo_element.get('src')
            if isinstance(src, str):
                company_logo = src

        company_element = sub_soup.find(
            'span',
            class_='t-14 t-normal'
        )
        if isinstance(company_element, Tag):
            name = company_element.text.strip().split(' · ')
            if len(name) > 0:
                company = name[0]

        date_range_element = sub_soup.find(
            'span',
            class_='pvs-entity__caption-wrapper'
        )
        if isinstance(date_range_element, Tag):
            date_range = date_range_element.text.strip()

        texts_elements = sub_soup.find_all(
            'span',
            class_ = 'visually-hidden',
        )

        if len(texts_elements) > 0:
            description = texts_elements[-1].text.strip()

        experiences.append(
            Experience(
                company=company,
                title=title,
                date_range=date_range,
                description=description,
                company_logo=company_logo
            )
        )

    return experiences
