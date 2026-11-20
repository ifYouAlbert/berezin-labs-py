                                                                       
                                          
   
import unittest
from plan import MAINTENANCE_PLAN, RECOVERY_PLAN
from plan_runner import validate_plan, PlanError


class PlanTests(unittest.TestCase):
    def test_01_maintenance_plan_is_valid(self):
        self.assertTrue(validate_plan(MAINTENANCE_PLAN,'maintenance'))

    def test_02_recovery_plan_is_valid(self):
        self.assertTrue(validate_plan(RECOVERY_PLAN,'recovery'))

    def test_03_archive_requires_previous_backup(self):
        with self.assertRaises(PlanError):
            validate_plan(['CHECK','ARCHIVE','BACKUP_B0','CHECK','BACKUP_B1'],'maintenance')

    def test_04_new_backup_only_after_verification(self):
        with self.assertRaises(PlanError):
            validate_plan(['CHECK','BACKUP_B0','ARCHIVE','BACKUP_B1','CHECK'],'maintenance')

    def test_05_diagnostic_step_precedes_restore(self):
        with self.assertRaises(PlanError):
            validate_plan(['RESTORE_B1','DIAGNOSE','CHECK'],'recovery')

    def test_06_incomplete_plan_rejected(self):
        with self.assertRaises(PlanError):
            validate_plan(['CHECK','BACKUP_B0','ARCHIVE','BACKUP_B1'],'maintenance')

if __name__=='__main__':
    unittest.main(verbosity=2)
