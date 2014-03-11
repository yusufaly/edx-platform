""" Contains Locations ___ """

from xmodule.modulestore.keys import CourseKey

class CourseLocation(CourseKey):
    # three local attributes: catalog name, run

    @classmethod
    def _from_string(cls, serialized):
        # Do we need to worry about the goofy i4x case?
        org, course, run = serialized.split('/')
        return match.groupdict()
        # pase_course_id
        # Two forms for serialized: one we haven't decided, one that is org/course/run everywhere (d/c)
        pass

    def _to_string(self):
        # reverse from_string
        pass

    def org(self):
        # return prop
        pass

    def run(self):
        # return prop

        pass

        # try not to add url parseable things