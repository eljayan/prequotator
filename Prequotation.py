import re
from win32com import client
from Item import Item
import Database

class Prequotation:

    def __init__(self, pathToFile):
        xl = client.Dispatch("Excel.Application")
        xl.Visible = True

        self.items = []
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
            it.setDescription(self.pre.Cells(r,3).value)
            it.setHsCode(self.pre.Cells(r, 8).value)
            it.setCustomsValue(self.pre.Cells(r,16).value)
            it.setAdValorem(self.pre.Cells(r,18).value)
            it.setSafeguard(self.pre.Cells(r,20).value)
            it.setFodinfa(self.pre.Cells(r,22).value)
            it.setVat(self.pre.Cells(r,26).value)
            it.setTotalTax(self.pre.Cells(r,27).value)

            #if there is no description, this is not a valid item
            if it.description is None:
                continue


            #find the hs code according to huawei
            if it.model:
                huaweiHsCode = Database.queryBom(it.model)
                it.setHsCodeHuawei(huaweiHsCode)


            #find torres y torres hs code tariffs
            cursor = Database.queryHS(it.hscode)

            if cursor.count() > 0:
                adv = float(cursor[0]["Ad Valorem"].replace("%", ""))/100.00
                fod = float(cursor[0]["Fodinfa"].replace("%", ""))/100.00
                vat = float(cursor[0]["VAT"].replace("%", ""))/100.00
                saf = float(cursor[0]["Safeguard"].replace("%", ""))/100.00

                it.setAdValoremPercentage(adv)
                it.setFodindaPercentage(fod)
                it.setVatPercentage(vat)
                it.setSafeguardPercentage(saf)

                it.autocalculate()

            self.items.append(it)


    def rageStart(self):
        pattern = re.compile("Producto")
        for cel in self.pre.Usedrange:
            if not isinstance(cel.value, basestring):
                continue
            if cel.value is None:
                continue

            if pattern.search(cel.value):
                return cel.Row + 1

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

        r = 2 #first row number
        i = 1 #item number
        ttTaxTotal = float(0.00)
        hwTaxTotal = float(0.00)

        for item in self.items:
            summary.Cells(r, 1).Value = i
            summary.Cells(r, 2).Value = item.model
            summary.Cells(r, 3).Value = item.description
            summary.Cells(r, 4).Value = item.hscode
            summary.Cells(r, 5).Value = item.hsCodeHuawei
            summary.Cells(r, 6).Value = item.totalTax
            summary.Cells(r, 7).Value = item.autoCalculatedTax

            #some formatting
            summary.Cells(r, 7).Numberformat = "$#,##0.00_);($#,##0.00)"
            summary.Cells(r, 3).Numberformat = "General"
            summary.Cells(r, 5).Numberformat = "General"

            ttTaxTotal += float(item.totalTax)
            hwTaxTotal += float(item.autoCalculatedTax)
            r+=1
            i+=1

        summary.Cells(r+2, 1).value = "Total TT:"
        summary.Cells(r+2, 2).value = ttTaxTotal
        summary.Cells(r+2, 2).Numberformat = "$#,##0.00_);($#,##0.00)"

        summary.Cells(r+3, 1).value = "Total HW:"
        summary.Cells(r+3, 2).value = hwTaxTotal
        summary.Cells(r+3, 2).Numberformat= "$#,##0.00_);($#,##0.00)"

        summary.Cells(r+4, 1).value = "Prequotation amount:"
        summary.Cells(r+4, 2).value = hwTaxTotal-10.00
        summary.Cells(r+4, 2).Numberformat= "$#,##0.00_);($#,##0.00)"
        

if __name__ == "__main__":
    prequotation = Prequotation("D:/myScripts/prequotator/error sin salvaguardia Orden 2016-TQ-01694.xls")

    print prequotation.customsValue
    print prequotation.adValorem
    print prequotation.fodinfa
    print prequotation.safeguard
    print prequotation.vat
    print prequotation.totalTax
    print prequotation.selfCheckTotalTax()
    prequotation.setItems()
    prequotation.createSummary()
    for i in prequotation.items:
        print vars(i)

