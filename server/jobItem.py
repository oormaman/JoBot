class Job:
    def __init__(self, job_id, affiliation1, affiliation2, job_name, link, description, site_name):
        self._id = job_id
        self._job_name = job_name
        self._link = link
        self._description = description
        self._site_name = site_name
        self._affiliation1 = affiliation1
        self._affiliation2 = affiliation2

    @property
    def job_name(self):
        return self._job_name.strip()

    @property
    def id(self):
        return self._id.strip()

    @property
    def link(self):
        return self._link.strip()

    @property
    def description(self):
        return self._description.strip()

    @property
    def site_name(self):
        return self._site_name.strip()

    @property
    def affiliation1(self):
        return self._affiliation1.strip()

    @property
    def affiliation2(self):
        return self._affiliation2.strip()

    def set_affiliation1(self, affiliation1):
        self._affiliation1 = affiliation1

    def set_affiliation2(self, affiliation2):
        self._affiliation2 = affiliation2
