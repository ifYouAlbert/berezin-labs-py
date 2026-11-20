                                                                   
                                                 
                                                  
   
import json
import tempfile
import unittest
from pathlib import Path

from maintenance import create_backup, restore_backup
from checks import inspect_system

ROOT = Path(__file__).resolve().parent
FILES = ("users.json", "tickets.json")


class BackupRestoreTests(unittest.TestCase):
    def setUp(self):
                                                                               
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.data = self.root / "data"
        self.data.mkdir()
        for name in FILES:
            (self.data / name).write_bytes((ROOT / "fixtures" / name).read_bytes())

    def test_01_backup_creates_both_files(self):
                                                                       
        dst = self.root / "B0"
        returned = create_backup(self.data, dst)
        self.assertEqual(Path(returned), dst)
        for name in FILES:
            self.assertTrue((dst / name).is_file(), name)

    def test_02_backup_content_matches(self):
                                                                          
        dst = self.root / "B0"
        create_backup(self.data, dst)
        for name in FILES:
            self.assertEqual((dst / name).read_bytes(), (self.data / name).read_bytes(), name)

    def test_03_backup_cannot_overwrite(self):
                                                                        
        dst = self.root / "B0"
        create_backup(self.data, dst)
        before = {name: (dst / name).read_bytes() for name in FILES}
        with self.assertRaises(FileExistsError):
            create_backup(self.data, dst)
        self.assertEqual(before, {name: (dst / name).read_bytes() for name in FILES})

    def test_04_restore_after_corruption(self):
                                                                      
        backup = self.root / "B1"
        create_backup(self.data, backup)
        (self.data / "tickets.json").write_text('{broken', encoding='utf-8')
        returned = restore_backup(backup, self.data)
        self.assertEqual(Path(returned), self.data)
        self.assertTrue(inspect_system(self.data)['ok'])
        for name in FILES:
            self.assertEqual((self.data / name).read_bytes(), (backup / name).read_bytes(), name)

    def test_05_restore_rejects_missing_file(self):
                                                                       
        backup = self.root / "B1"
        backup.mkdir()
        (backup / "users.json").write_bytes((self.data / "users.json").read_bytes())
        before = {name: (self.data / name).read_bytes() for name in FILES}
        with self.assertRaises((FileNotFoundError, ValueError)):
            restore_backup(backup, self.data)
        self.assertEqual(before, {name: (self.data / name).read_bytes() for name in FILES})

    def test_06_restore_rejects_broken_json(self):
                                                                           
        backup = self.root / "B1"
        backup.mkdir()
        (backup / "users.json").write_bytes((self.data / "users.json").read_bytes())
        (backup / "tickets.json").write_text('{broken', encoding='utf-8')
        before = {name: (self.data / name).read_bytes() for name in FILES}
        with self.assertRaises((ValueError, json.JSONDecodeError)):
            restore_backup(backup, self.data)
        self.assertEqual(before, {name: (self.data / name).read_bytes() for name in FILES})


if __name__ == "__main__":
    unittest.main(verbosity=2)
