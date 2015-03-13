#!/usr/bin/env python
PKG = 'gcal_routine'
NAME = 'gcal_tester'

import rospy
import unittest
import rostest
import sys


from gcal_routine.tools import GCal
from gcal_routine.queue_routine_runner import GCalRoutineRunner
from roslib.packages import find_resource


class GCalTest(unittest.TestCase):
    def __init__(self, *args):
        super(GCalTest, self).__init__(*args)
        self.filename = find_resource(PKG, 'test.json')[0]
        rospy.init_node(NAME)

    def _added(self, a, t):
        print '===   added task: %s' % str(t)
        self.assertEqual(t.start_node_id, 'place5')

    def _removed(self, a, t):
        print '=== removed task: %s' % str(t)
        # in this test we should never call this!
        self.fail()

    def test_gcal(self):
        gcal = GCal(None,
                    None,
                    add_cb=self._added, remove_cb=self._removed,
                    file_name=self.filename)
        self.assertEqual(len(gcal.get_task_list()), 0)
        self.assertTrue(gcal.update())
        self.assertEqual(len(gcal.get_task_list()), 4)
        gcal.shift_to_now()

    def test_runner(self):
        runner = GCalRoutineRunner(None)
        gcal = GCal(None,
                    None,
                    add_cb=runner.add_task, remove_cb=runner.remove_task,
                    file_name=self.filename)
        self.assertTrue(gcal.update())
        gcal.shift_to_now()
        runner.schedule_tasks()



if __name__ == '__main__':
    rostest.rosrun(PKG, NAME, GCalTest, sys.argv)
