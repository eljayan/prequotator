import re
from win32com import client
from Item import Item
from Database import Database
class Prequotation:

    items = []


    def __init__(self, pathToFile):
        xl = client.Dispatch("Excel.Application")
        xl.Visible = True
        self.workbook = xl.Workbooks.Open(pathToFile)
        self.englishSheet = xl.Sheets("English")
        self.pre = xl.Sheets("Pre-Liquidacion Parcial x Items")

        self.setCustomsValue()
        self.setAdvalorem()
        self.setFodinfa()
        self.setSafeguard()
        self.setVAT()
        self.setTotalTax()


    def setCustomsValue(self):
        self.customsValue = self.englishSheet.Cells(31,6).value

    def setAdvalorem(self):
        self.adValorem = self.englishSheet.Cells(51,6).value

    def setFodinfa(self):
        self.fodinfa = self.englishSheet.Cells(54,6).value

    def setSafeguard(self):
        self.safeguard = self.englishSheet.Cells(57,6).value

    def setVAT(self):
        self.vat = self.englishSheet.Cells(60,6).value
        return

    def setTotalTax(self):
        self.totalTax = self.englishSheet.Cells(62,6).value

    def selfCheckTotalTax(self):
        autosum = self.adValorem+self.fodinfa+self.safeguard+self.vat
        return autosum == self.totalTax


    def setItems(self):
        rstart = self.rageStart()
        rend = self.rangeEnd()
        for r in range(rstart, rend):
            it = Item()
            it.setModel(self.pre.Cells(r, 6).value)
            it.setHsCode(self.pre.Cells(r, 8).value)
            it.setCustomsValue(self.pre.Cells(r,16).value)
            it.setAdValorem(self.pre.Cells(r,18).value)
            it.setSafeguard(self.pre.Cells(r,20).value)
            it.setFodinfa(self.pre.Cells(r,22).value)
            it.setVat(self.pre.Cells(r,26).value)
            it.setTotalTax(self.pre.Cells(r,27).value)

            if it.description is None:
                continue

            self.items.append(it)


        #print "range start: {}, range end {}".format(rstart,rend)



    def rageStart(self):
        pattern = re.compile("Producto")
        for cel in self.pre.Usedrange:
            if not isinstance(cel.value, basestring):
                continue
            if cel.value is None:
                continue

            if pattern.search(cel.value):
                return cel.Row

    def rangeEnd(self):
        pattern = re.compile("SON:")
        for cel in self.pre.Usedrange:
            if not isinstance(cel.value, basestring):
                continue

            if pattern.search(cel.value):
                return cel.Row

    def createSummary(self):
        summary = self.workbook.WorkSheets.Add()
        summary.Name = "summary"
        summary.Cells(1,1).value = "item"
        summary.Cells(1,2).value = "model"
        summary.Cells(1,3).value = "description"
        summary.Cells(1,4).value = "hstt"
        summary.Cells(1,5).value = "hshuawei"
        summary.Cells(1,6).value = "total tax tt"
        summary.Cells(1,7).value = "total tax huawei"


if __name__ == "__main__":
    prequotation = Prequotation("D:/myScripts/prequotator/Orden 2016-TQ-01735.xls")

    print prequotation.customsValue
    print prequotation.adValorem
    print prequotation.fodinfa
    print prequotation.safeguard
    print prequotation.vat
    print prequotation.totalTax
    print prequotation.selfCheckTotalTax()
    prequotation.createSummary()
    prequotation.setItems()