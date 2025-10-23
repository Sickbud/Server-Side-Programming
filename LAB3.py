from datetime import date

class Customer:
    def __init__(self, firstName, lastName, email, phoneNumber):
        self.firstName = firstName
        self.lastName = lastName
        self.__email = email
        self.__phoneNumber = phoneNumber

    def getFullName(self):
        return f"{self.firstName} {self.lastName}"

    def getEmail(self):
        return self.__email

    def getPhoneNumber(self):
        return self.__phoneNumber

    def setEmail(self, newEmail):
        self.__email = newEmail

    def setPhoneNumber(self, phoneNumber):
        self.__phoneNumber = phoneNumber


class Medicine:
    def __init__(self, name, form, pricePerUnit, stock):
        self.name = name
        self.form = form
        self.pricePerUnit = pricePerUnit
        self.stock = stock

    def describe(self):
        return f"{self.name}, форма: {self.form}, ціна: {self.pricePerUnit}₴, залишок: {self.stock} шт"


class Order(Customer):
    def __init__(self, firstName, lastName, email, phoneNumber, medicine, qty, requiresRx, validUntil=None):
        super().__init__(firstName, lastName, email, phoneNumber)
        self.medicine = medicine
        self.qty = qty
        self.requiresRx = requiresRx
        self.validUntil = validUntil
        self.totalPrice = Order.calcTotal(qty, medicine.pricePerUnit)

    def orderInfo(self):
        return (f"{self.getFullName()} замовив(ла) {self.medicine.name} x{self.qty} "
                f"на {self.totalPrice}₴{' (RX)' if self.requiresRx else ''}")

    def applyDiscount(self, percent):
        self.totalPrice -= self.totalPrice * percent / 100
        return f"Нова сума після знижки: {self.totalPrice:.2f}₴"

    def canSell(self):
        if not self.requiresRx:
            return True
        return self.validUntil is not None and date.today() <= self.validUntil

    @staticmethod
    def calcTotal(qty, pricePerUnit):
        return qty * pricePerUnit


class Payment:
    def __init__(self, amount, method, transactionCode):
        self.amount = amount
        self.method = method
        self.transactionCode = transactionCode
        self.paymentDate = date.today()

    def makePayment(self):
        return f"Оплата {self.amount}₴ способом: {self.method}, транзакція #{self.transactionCode}"


class PaidOrder(Order, Payment):
    def __init__(self, firstName, lastName, email, phoneNumber, medicine, qty, requiresRx, validUntil,
                 amount, method, transactionCode):
        Order.__init__(self, firstName, lastName, email, phoneNumber, medicine, qty, requiresRx, validUntil)
        Payment.__init__(self, amount, method, transactionCode)

    def summary(self):
        return (f"{self.getFullName()} оплатив {self.amount}₴ за {self.medicine.name} x{self.qty} "
                f"({self.method}, {self.paymentDate})")

    def applyDiscount(self, percent):
        if self.amount > 1000:
            self.amount -= self.amount * percent / 100
        return f"Нова сума оплати після знижки: {self.amount:.2f}₴"


if __name__ == "__main__":
    aspirin = Medicine("Аспірин 500 мг", "таблетки", 38.5, 120)
    insulin = Medicine("Інсулін", "розчин", 420.0, 30)

    print(aspirin.describe())
    print(insulin.describe())

    o1 = Order("Микола", "Сидоренко", "n@ex.com", "+380931112233", aspirin, 3, False)
    o2 = Order("Олена", "Коваленко", "o@ex.com", "+380931234567", insulin, 2, True, date(2025, 12, 31))

    print(o1.orderInfo())
    print(o1.applyDiscount(10))
    print("Можна продати інсулін:", "Так" if o2.canSell() else "Ні")

    p1 = PaidOrder("Олена", "Коваленко", "o@ex.com", "+380931234567", insulin, 2, True, date(2025, 12, 31),
                   amount=o2.totalPrice, method="карта", transactionCode="RX999")
    print(p1.makePayment())
    print(p1.summary())
    print(p1.applyDiscount(15))