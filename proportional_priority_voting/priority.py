class Priority:
    def __init__(self):
        self.identifier = None
        self.name = None
        self.description = None
        self.capital = None
        self.annual = None
        self._rev = None

    def setIdentifier(self, identifier: str) -> None:
        self.identifier = identifier

    def setName(self, name: str) -> None:
        self.name = name

    def setDescription(self, itemDescription: str) -> None:
        self.description = description

    def setCapital(self, itemCapital: int) -> None:
        """A guess at this item's acquisition cost (capital budget)
        """
        self.capital = capital

    def setAnnual(self, itemAnnual: int) -> None:
        """A guess at this item's care/feeding/maintenance cost (operations
        budget)
        """
        self.annual = annual

    async def getByIdentifier(self, identifier: str) -> None:
        blob = await self.cq.get(identifier)
        if blob is None:
            raise KeyError
        self.setIdentifier(blob._id)
        self._rev = blob._rev
        self.setName(blob.name)
        self.setDescription(blob.description)
        self.setCapital(blob.capital)
        self.setAnnual(blob.annual)

    async def save(self) -> None:
        if self.name is None or self.name == "":
            raise KeyError
        blob = {
            'name': self.name,
            'description': self.description,
            'capital': self.capital,
            'annual': self.annual,
        }
        if self._rev:
            blob['_rev'] = self._rev
        blob2 = await self.cq.put(self.identifier, data=json.dumps(blob))
        self._rev = blob2.get('_rev', None)

    async def getRank(self) -> float:
        blob2 = await self.cq.get
        pass

    async def setMyRank(self, identity: str, ranking: int) -> None:
        pass

