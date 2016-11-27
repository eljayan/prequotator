
class Item:

    description
    model
    hscode
    customsValue
    adValorem
    fodinfa
    safeguard
    vat
    totalTax

    def setDescription(self, value):
        self.description = value

    def setModel(self, value):
        self.model = value

    def setHsCode(self, value):
        self.hscode = value

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

    def autocalculate(self):
        customsValue = self.customsValue
        adValorem = customsValue * self.adValoremPercentage
        fodinfa = customsValue * self.fodinfaPercentage
        safeguard = customsValue * self.fodinfaPercentage
        vat = (customsValue+adValorem+fodinfa+safeguard) * self.vatPercentage
        return adValorem+fodinfa+safeguard+vat




