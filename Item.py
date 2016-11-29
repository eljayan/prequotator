
class Item:

    def __int__(self):
        self.description = None
        self.model =None
        self.hscode =None
        self.hsCodeHuawei = None
        self.customsValue = None
        self.adValorem = None
        self.adValoremPercentage = None
        self.fodinfa =None
        self.fodinfaPercentage = None
        self.vat = None
        self.vatPercentage = None
        self.safeguard = None
        self.safeguardPercentage = None

    def setDescription(self, value):
        self.description = value

    def setModel(self, value):
        self.model = value

    def setHsCode(self, value):
        self.hscode = value

    def setHsCodeHuawei(self, value):
        self.hsCodeHuawei = value

    def setCustomsValue(self, value):
        self.customsValue = value

    def setAdValorem(self,value):
        self.adValorem = value

    def setAdValoremPercentage(self,value):
        self.adValoremPercentage = value

    def setFodinfa(self,value):
        self.fodinfa = value

    def setFodindaPercentage(self,value):
        self.fodinfaPercentage = value

    def setSafeguard(self,value):
        self.safeguard = value

    def setSafeguardPercentage(self,value):
        self.safeguardPercentage = value

    def setVat(self,value):
        self.vat = value

    def setVatPercentage(self,value):
        self.vatPercentage = value

    def setTotalTax(self, value):
        self.totalTax = value

    def setAutoCalculatedTax(self, value):
        self.autoCalculatedTax = value

    def autocalculate(self):
        '''autocalculates taxes according to Hs code provided by T&T'''
        try:
            customsValue = float(self.customsValue)
            adValorem = customsValue * self.adValoremPercentage
            fodinfa = customsValue * self.fodinfaPercentage
            safeguard = customsValue * self.safeguardPercentage
            vat = (customsValue+adValorem+fodinfa+safeguard) * self.vatPercentage
            self.setAutoCalculatedTax(adValorem+fodinfa+safeguard+vat)
        except:
            self.setAutoCalculatedTax(0)



