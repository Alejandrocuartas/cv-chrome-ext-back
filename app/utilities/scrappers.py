""" Helper functions for the application """

import json
# pylint: disable=import-error
from bs4 import BeautifulSoup, Tag # type: ignore
from ..types.generate_cv import ParsedCvHTML, Experience

def extract_data_from_request(html: str):
    """ Extract data from a request. """

    parsed_data = parse_html_to_event_schema(html)
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
    resume_section_parent = soup.find_all(
        'section',
        class_='artdeco-card pv-profile-card break-words mt2'
    )
    if len(resume_section_parent) > 0:
        for div in resume_section_parent:
            sub_soup = BeautifulSoup(str(div), 'html.parser')
            child1 = sub_soup.find(
                'div',
                class_='display-flex ph5 pv3'
            )
            if isinstance(child1, Tag):
                child2 = child1.find(
                    'div',
                    class_='YEUQjCRdAayyPJoelGmaEfzUvJrSHPnLKjUnQ'
                )
                if isinstance(child2, Tag):
                    child3 = child2.find(
                        'div',
                        class_='dOlsoPEBmaghjERSXAbqcOuRCiXrsEkEnE'
                    )
                    if isinstance(child3, Tag):
                        resume_span = child3.find(
                            'span',
                            class_='visually-hidden'
                        )
                        if isinstance(resume_span, Tag):
                            resume = resume_span.text.strip()
                            break

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
            class_='ViJVhuHdFudvBxfKtzmkJMYDOrGxA pv-top-card-profile-picture__image--show evi-image ember-view'
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
        profile_photo=profile_photo
    )

    return parsed_html

def get_ul_of_experiences(soup: BeautifulSoup) -> Tag | None:
    """ Get the ul of experiences. from the HTML."""
    ul_experiences = soup.find_all(
            'ul',
            class_='BtfbvVmlfKAeHtqUpLjwfzizjYOXxWsmwGkng'
        )

    valid_uls: list[Tag] = []
    for ul in ul_experiences:
        li_items = ul.find_all(
            'li',
            class_='artdeco-list__item tFNJGdgZPdGDcLtjPOQVjywuRIunMYsMs oPjOMAOSqFVcWFiuHPdqyHuAGuTEXZcFUQg'
        )
        is_valid = False
        if len(li_items) > 0:
            for li in li_items:
                sub_soup = BeautifulSoup(str(li), 'html.parser')
                element_in_li = sub_soup.find(
                    'div',
                    class_='VCbAJOyhaRwVphesKXELAJHtESiYyECkJo XaACUcxyNUBWWiWtTartGuquUQBxkkTrBsY EDzeFvuUObHTPtsPbjICqHJImfwFNArpZY',
                    attrs={
                        'data-view-name': 'profile-component-entity'
                    }
                )
                if isinstance(element_in_li, Tag):
                    experience_element = element_in_li.find(
                        'a',
                        attrs={
                            'data-field': 'experience_company_logo'
                        }
                    )
                    if experience_element is not None:
                        is_valid = True
                        break
        if is_valid:
            valid_uls.append(ul)

    if len(valid_uls) == 0:
        return None

    return valid_uls[0]

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

        description_element = sub_soup.find(
            'div',
            class_='dOlsoPEBmaghjERSXAbqcOuRCiXrsEkEnE inline-show-more-text--is-collapsed inline-show-more-text--is-collapsed-with-line-clamp full-width'
        )
        if isinstance(description_element, Tag):
            description_span = description_element.find(
                'span',
                class_='visually-hidden'
            )
            if isinstance(description_span, Tag):
                description = description_span.text.strip()

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
