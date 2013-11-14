import json
import csv
import dateutil

from optparse import make_option
from textwrap import dedent

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from courseware.models import StudentModule
from xmodule.combined_open_ended_module import CombinedOpenEndedModule

class Command(BaseCommand):
    """
    Command to fix up OEE response after a certain date that were reset because of an out of sync error

    Prints a csv that indicates which problems were fixed for which students, and which
    problems weren't able to be recovered (because the student had submitted a new answer after
    the out of sync error)
    """
    help = dedent(__doc__).strip()
    args = "<start date>"
    option_list = BaseCommand.option_list + (
        make_option(
            '--commit',
            action='store_true',
            dest='commit',
            default=False,
            help="Commit changes to courseware_studentmodule on success"
        ),
        make_option(
            '--batch',
            action='store',
            dest='batch',
            default=1000,
            help="Number of users to update before committing"
        )
    )

    def parse_task_states(self, task_states):
        return [json.loads(task_state) for task_state in task_states]

    def dump_task_states(self, task_states):
        return [json.dumps(task_state) for task_state in task_states]

    def is_reset_child_state(self, task_child):
        return (
            task_child['child_state'] == 'initial' and
            task_child['child_history'] == []
        )

    def is_reset_task_states(self, task_state):
        return all(self.is_reset_child_state(child) for child in task_state)

    def states_sort_key(self, idx_task_states):
        """
        Return a key for sorting a list of indexed task_states, by validity,
        most recent score, and then by index
        """
        idx, task_states = idx_task_states
        valid = not self.is_reset_task_states(task_states)
        total_score = sum(child['child_history'][-1].get('score', 0) for child in task_states if child['child_history'])
        return valid, total_score, idx

    @transaction.commit_manually()
    def handle(self, *args, **options):
        try:
            output_csv = csv.writer(self.stdout)
            output_csv.writerow(["Count", "Reset?", "User Id", "Problem Id", "Reset to submission"])
            for count, student_module in enumerate(StudentModule.objects.filter(
                module_type='combinedopenended',
                modified__gt=dateutil.parser.parse(' '.join(args))
            ).values('student_id', 'state', 'module_state_key')):
                state = json.loads(student_module['state'])
                current_task_states = self.parse_task_states(state['task_states'])
                old_task_states = [self.parse_task_states(task_states) for task_states in state['old_task_states']]

                sorted_states = sorted(enumerate(old_task_states + [current_task_states]), key=self.states_sort_key, reverse=True)

                idx, best_task_states = sorted_states[0]

                if best_task_states == current_task_states:
                    output_csv.writerow([count, False, student_module['student_id'], student_module['module_state_key'], None])
                    continue

                state['old_task_states'].append(state['task_states'])
                state['task_states'] = self.dump_task_states(best_task_states)

                # The state is ASSESSING unless all of the children are done, or all
                # of the children haven't been started yet
                if all(child['child_state'] == CombinedOpenEndedModule.DONE for child in best_task_states):
                    state['state'] = CombinedOpenEndedModule.DONE
                elif all(child['child_state'] == CombinedOpenEndedModule.INITIAL for child in best_task_states):
                    state['state'] = CombinedOpenEndedModule.INITIAL
                else:
                    state['state'] = CombinedOpenEndedModule.ASSESSING

                # The current task number is the index of the last completed child + 1,
                # limited by the number of tasks
                last_completed_child = next((i for i, child in reversed(list(enumerate(best_task_states))) if child['child_state'] == CombinedOpenEndedModule.DONE), 0)
                state['current_task_number'] = min(last_completed_child + 1, len(best_task_states))

                student_module.state = json.dumps(state)
                student_module.save()
                output_csv.writerow([count, True, student_module['student_id'], student_module['module_state_key'], best_task_states])

                if count % options['batch'] == 0:
                    if options['commit']:
                        transaction.commit()
                    else:
                        transaction.rollback()

        except:
            transaction.rollback()
            raise
        else:
            if options['commit']:
                transaction.commit()
            else:
                transaction.rollback()
