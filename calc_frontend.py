import streamlit as st
import json
import datetime
from os import getcwd, chdir, path

class BrokerageCalculator:
    def __init__(self, buyPrice, sellPrice, qty):
        chdir(path.dirname(path.abspath(__file__)))
        self.buyPrice = float(buyPrice)
        self.sellPrice = float(sellPrice)
        self.qty = int(qty)
        self.turnover = (self.buyPrice * self.qty) + (self.sellPrice * self.qty)
        self.avgPrice = self.turnover / (self.qty * 2)
        self.order: str = ""
        directory = getcwd()
        self.journalFile = directory + "/journal.json"

    def _getMaxBrokerage(self, brokerage: float) -> float:
        return 40.0 if brokerage > 40.0 else brokerage

    def _getRiskRewardRatio(self, orderType: str, secondLeg: str) -> float:
        secondLeg = float(secondLeg)
        reward: float = 0.0
        risk: float = 0.0
        if orderType.lower() != 'b' and orderType.lower() != 's':
            st.error("Invalid order type.")
        if orderType.lower() == "b":
            risk = self.buyPrice - secondLeg
            reward = self.sellPrice - self.buyPrice
        else:
            risk = secondLeg - self.sellPrice
            reward = self.sellPrice - self.buyPrice

        return reward / risk

    def addOrder(self, orderType: str, secondLeg: str) -> None:
        ratio = self._getRiskRewardRatio(orderType, secondLeg)
        if ratio == 0.0:
            st.error("Something went wrong. Use -h for usage.")
        st.write(f"Reward:Risk ratio: {ratio}")
        now = datetime.datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%H:%M:%S")

        data = {
                "orderType": self.order,
                "position": orderType.lower(),
                "ratio": ratio,
                "time": time,
                "result": "P" if self.netProfit > 0 else "L",
                "netPL": self.netProfit,
                "quantity": self.qty
                }
        try:
            f = open(self.journalFile, "r")
            jsonD = json.load(f)
            if date not in jsonD:
                jsonD[date] = []
            f.close()
        except FileNotFoundError:
            jsonD = {}
            jsonD[date] = []
            pass

        f = open(self.journalFile, "w")
        jsonD[date].append(data)
        json.dump(jsonD, f, indent=4)

    def intradayEquity(self) -> None:
        self.order = "Intraday"
        brokerage = self.turnover * 0.0002
        brokerage = self._getMaxBrokerage(brokerage)
        sttCharges = self.qty * self.avgPrice * 0.00025
        sebiCharges = self.turnover * 0.000002
        stampCharges = self.qty * self.avgPrice * 0.00003
        exchangeCharges = self.turnover * 0.0000325

        totalCharges = brokerage + sttCharges + sebiCharges + stampCharges + exchangeCharges
        gst = totalCharges * 0.18
        self.netProfit = ((self.sellPrice - self.buyPrice) * self.qty) - (totalCharges + gst)
        pointsToBreakeven = (totalCharges + gst) / self.qty
        st.write(f"Total charges: {(totalCharges + gst)}")
        st.write(f"Points to break even: {pointsToBreakeven}")
        st.write(f"Net profit: {self.netProfit}")

    def deliveryEquity(self, days: int = 0, isCashPlus: bool = False) -> None:
        self.order = "Delivery"
        brokerage = self.turnover * 0.002
        brokerage = self._getMaxBrokerage(brokerage)
        sttCharges = self.qty * self.avgPrice * 0.00025
        sebiCharges = self.turnover * 0.000002
        stampCharges = self.qty * self.avgPrice * 0.00003
        exchangeCharges = self.turnover * 0.0000325
        if isCashPlus:
            self.order = "Delivery (Cash+)"
            interest = (self.turnover * 0.00025) * days
        else:
            interest = 0

        totalCharges = brokerage + sttCharges + sebiCharges + stampCharges + exchangeCharges + interest

        gst = totalCharges * 0.18

        self.netProfit = ((self.sellPrice - self.buyPrice) * self.qty) - (totalCharges + gst)
        pointsToBreakeven = (totalCharges + gst) / self.qty

        st.write(f"Total charges: {(totalCharges + gst)}")
        st.write(f"Points to break even: {pointsToBreakeven}")
        if isCashPlus:
            st.write(f"Total interest for {days} days: {interest}")
        st.write(f"Net profit: {self.netProfit}")

    def options(self) -> None:
        self.order = "Options"
        brokerage = 40.0
        sttCharges = self.qty * self.avgPrice * 0.0005
        sebiCharges = self.turnover * 0.000002
        stampCharges = self.qty * self.avgPrice * 0.00003
        exchangeCharges = self.turnover * 0.00053

        totalCharges = brokerage + sttCharges + sebiCharges + stampCharges + exchangeCharges
        gst = totalCharges * 0.18

        self.netProfit = ((self.sellPrice - self.buyPrice) * self.qty) - (totalCharges + gst)
        pointsToBreakeven = (totalCharges + gst) / self.qty

        st.write(f"Total charges: {(totalCharges + gst)}")
        st.write(f"Points to break even: {pointsToBreakeven}")
        st.write(f"Net profit: {self.netProfit}")

def main():
    st.title("Brokerage Calculator")

    transaction_type = st.selectbox("Select Transaction Type", ["Intraday", "Delivery", "Delivery (Cash+)", "Options"])

    if transaction_type == "Intraday":
        buy_price = st.number_input("Enter Buy Price")
        sell_price = st.number_input("Enter Sell Price")
        qty = st.number_input("Enter Quantity", step=1, value=1)
        calc = BrokerageCalculator(buy_price, sell_price, qty)
        calc.intradayEquity()

    elif transaction_type == "Delivery":
        buy_price = st.number_input("Enter Buy Price")
        sell_price = st.number_input("Enter Sell Price")
        qty = st.number_input("Enter Quantity", step=1, value=1)
        calc = BrokerageCalculator(buy_price, sell_price, qty)
        calc.deliveryEquity()

    elif transaction_type == "Delivery (Cash+)":
        buy_price = st.number_input("Enter Buy Price")
        sell_price = st.number_input("Enter Sell Price")
        qty = st.number_input("Enter Quantity", step=1, value=1)
        days = st.number_input("Enter Number of Days", step=1, value=1)
        calc = BrokerageCalculator(buy_price, sell_price, qty)
        calc.deliveryEquity(days=days, isCashPlus=True)

    elif transaction_type == "Options":
        buy_price = st.number_input("Enter Buy Price")
        sell_price = st.number_input("Enter Sell Price")
        qty = st.number_input("Enter Quantity", step=1, value=1)
        calc = BrokerageCalculator(buy_price, sell_price, qty)
        calc.options()

if __name__ == "__main__":
    main()
