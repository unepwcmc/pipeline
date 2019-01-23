# Test case
import os
import unittest
import arcpy


class TestMerge(unittest.TestCase):

	# when merged, total number of feature should match
	def test_merge_numberconsistent(self):
		
		sourcedb = '..' + os.sep + 'data.gdb'
		testgdb = '..' + os.sep + 'testoutput.gdb'
		merge_num = int(arcpy.GetCount_management(testgdb + os.sep + 'merge')[0])
		combined_pt_poly_num = int(arcpy.GetCount_management(sourcedb + os.sep + 'poly')[0]) + \
		int(arcpy.GetCount_management(sourcedb + os.sep + 'pt')[0])

		self.assertEqual(merge_num, combined_pt_poly_num)


if __name__ == '__main__':
	unittest.main()