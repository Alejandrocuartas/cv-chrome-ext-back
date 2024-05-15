""" Generate LinkedIn CV """

from dataclasses import dataclass, asdict

@dataclass
class GenerateCVRequest:
    """ Generate CV Request """
    html_s3_key: str

@dataclass
class Experience:
    """ Experience """
    company: str
    company_logo: str
    title: str
    date_range: str
    description: str

    def to_dict(self):
        """ Convert to dictionary """
        return asdict(self)

@dataclass
class ParsedCvHTML:
    """ Parsed HTML """
    profile_name: str
    heading: str
    resume: str
    profile_photo: str
    experiences: list[Experience]

    def to_dict(self):
        """ Convert to dictionary """
        return asdict(self)
