import json
import logging

from xmodule.modulestore import search
from xmodule.modulestore.django import modulestore, ModuleI18nService
from xmodule.modulestore.exceptions import ItemNotFoundError, NoPathToItem
from xmodule.open_ended_grading_classes.controller_query_service import ControllerQueryService
from xmodule.open_ended_grading_classes.grading_service_module import GradingServiceError

from django.utils.translation import ugettext as _
from django.conf import settings

from lms.lib.xblock.runtime import LmsModuleSystem
from edxmako.shortcuts import render_to_string


log = logging.getLogger(__name__)

GRADER_DISPLAY_NAMES = {
    'ML': _("AI Assessment"),
    'PE': _("Peer Assessment"),
    'NA': _("Not yet available"),
    'BC': _("Automatic Checker"),
    'IN': _("Instructor Assessment"),
}

STUDENT_ERROR_MESSAGE = _("Error occurred while contacting the grading service.  Please notify course staff.")
STAFF_ERROR_MESSAGE = _("Error occurred while contacting the grading service.  Please notify your edX point of contact.")

SYSTEM = LmsModuleSystem(
    static_url='/static',
    track_function=None,
    get_module=None,
    render_template=render_to_string,
    replace_urls=None,
    descriptor_runtime=None,
    services={
        'i18n': ModuleI18nService(),
    },
)


def generate_problem_url(problem_url_parts, base_course_url):
    """
    From a list of problem url parts generated by search.path_to_location and a base course url, generates a url to a problem
    @param problem_url_parts: Output of search.path_to_location
    @param base_course_url: Base url of a given course
    @return: A path to the problem
    """
    problem_url = base_course_url + "/"
    for i, part in enumerate(problem_url_parts):
        if part is not None:
            if i == 1:
                problem_url += "courseware/"
            problem_url += part + "/"
    return problem_url


def does_location_exist(course_id, location):
    """
    Checks to see if a valid module exists at a given location (ie has not been deleted)
    course_id - string course id
    location - string location
    """
    try:
        search.path_to_location(modulestore(), course_id, location)
        return True
    except ItemNotFoundError:
        # If the problem cannot be found at the location received from the grading controller server,
        # it has been deleted by the course author.
        return False
    except NoPathToItem:
        # If the problem can be found, but there is no path to it, then we assume it is a draft.
        # Log a warning if the problem is not a draft (location does not end in "draft").
        if not location.endswith("draft"):
            log.warn(("Got an unexpected NoPathToItem error in staff grading with a non-draft location {0}. "
                      "Ensure that the location is valid.").format(location))
        return False


def create_controller_query_service():
    """
    Return an instance of a service that can query edX ORA.
    """
    return ControllerQueryService(settings.OPEN_ENDED_GRADING_INTERFACE, SYSTEM)


class StudentProblemList(object):
    """
    Get a list of problems that the student has attempted from ORA.
    Add in metadata as needed.
    """
    def __init__(self, course_id, user_id):
        """
        @param course_id: The id of a course object.  Get using course.id.
        @param user_id: The anonymous id of the user, from the unique_id_for_user function.
        """
        self.course_id = course_id
        self.user_id = user_id

        # We want to append this string to all of our error messages.
        self.course_error_ending = _("for course {0} and student {1}.").format(self.course_id, user_id)

        # This is our generic error message.
        self.error_text = STUDENT_ERROR_MESSAGE
        self.success = False

        # Create a service to query edX ORA.
        self.controller_qs = create_controller_query_service()

    def fetch_from_grading_service(self):
        """
        Fetch a list of problems that the student has answered from ORA.
        Handle various error conditions.
        @return: A boolean success indicator.
        """
        # In the case of multiple calls, ensure that success is false initially.
        self.success = False
        try:
            #Get list of all open ended problems that the grading server knows about
            problem_list_dict = self.controller_qs.get_grading_status_list(self.course_id, self.user_id)
        except GradingServiceError:
            log.error("Problem contacting open ended grading service " + self.course_error_ending)
            return self.success
        except ValueError:
            log.error("Problem with results from external grading service for open ended" + self.course_error_ending)
            return self.success

        success = problem_list_dict['success']
        if 'error' in problem_list_dict:
            self.error_text = problem_list_dict['error']
            return success
        if 'problem_list' not in problem_list_dict:
            log.error("Did not receive a problem list in ORA response" + self.course_error_ending)
            return success

        self.problem_list = problem_list_dict['problem_list']

        self.success = True
        return self.success

    def add_problem_data(self, base_course_url):
        """
        Add metadata to problems.
        @param base_course_url: the base url for any course.  Can get with reverse('course')
        @return: A list of valid problems in the course and their appended data.
        """
        # Our list of valid problems.
        valid_problems = []

        if not self.success or not isinstance(self.problem_list, list):
            log.error("Called add_problem_data without a valid problem list" + self.course_error_ending)
            return valid_problems

        # Iterate through all of our problems and add data.
        for problem in self.problem_list:
            try:
                # Try to load the problem.
                problem_url_parts = search.path_to_location(modulestore(), self.course_id, problem['location'])
            except (ItemNotFoundError, NoPathToItem):
                # If the problem cannot be found at the location received from the grading controller server,
                # it has been deleted by the course author. We should not display it.
                error_message = "Could not find module for course {0} at location {1}".format(self.course_id,
                                                                                              problem['location'])
                log.error(error_message)
                continue

            # Get the problem url in the courseware.
            problem_url = generate_problem_url(problem_url_parts, base_course_url)

            # Map the grader name from ORA to a human readable version.
            grader_type_display_name = GRADER_DISPLAY_NAMES.get(problem['grader_type'], "edX Assessment")
            problem['actual_url'] = problem_url
            problem['grader_type_display_name'] = grader_type_display_name
            valid_problems.append(problem)
        return valid_problems
