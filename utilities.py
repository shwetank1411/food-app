from enum import Enum
from dataclasses import dataclass

class PaymentMode(Enum):

    non  =  None
    dbt  = 'DEBIT CARD'
    cdt  = 'CREDIT CARD'
    net  = 'NET BANKING'
    upi  = 'UNIFIED PAYMENT INTERFACE'
    cod  = 'CASH ON DELIVERY'

    @staticmethod
    def about() -> None:
        print("Codes for available payment modes are as follows -")
        for i in PaymentMode:
            print(f"{i.name} is a code for {i.value}")


@dataclass(frozen=True)
class PaymentGateway:

    amount: float

    def pay_by_payment_mode(self, payment_mode :PaymentMode) -> None:
        if payment_mode.name == PaymentMode.dbt.name:
            self.pay_through_debit_card()
        elif payment_mode.name == PaymentMode.cdt.name:
            self.pay_through_credit_card()
        elif payment_mode.name == PaymentMode.net.name:
            self.pay_through_net_banking()
        elif payment_mode.name == PaymentMode.upi.name:
            self.pay_through_unified_payment_interface()
        else:
            raise ValueError(f"Invalid Payment Mode - {payment_mode.value}")

    def pay_through_debit_card(self) ->None:
        print(f"Payment for INR {self.amount} through {PaymentMode.dbt.value} has been processed")
    def pay_through_credit_card(self) ->None:
        print(f"Payment for INR {self.amount} through {PaymentMode.cdt.value} has been processed")
    def pay_through_net_banking(self) ->None:
        print(f"Payment for INR {self.amount} through {PaymentMode.net.value} has been processed")
    def pay_through_unified_payment_interface(self) ->None:
        print(f"Payment for INR {self.amount} through {PaymentMode.upi.value} has been processed")


@dataclass(frozen = True)
class Taxes:

    CGST :float = 0.09
    SGST :float = 0.09

    def calculate_GST(self,base_amount :float) ->tuple[float,float,float]:
        cgst_tax_amt = round(base_amount * self.CGST,2)
        sgst_tax_amt = round(base_amount * self.SGST,2)
        tax_total = cgst_tax_amt + sgst_tax_amt
        return cgst_tax_amt,sgst_tax_amt,tax_total

@dataclass(frozen=True)
class Fees:

    THRESHOLD_AMT_FOR_FREE_DELIVERY :int = 100
    MIN_DELIVERY_FEE :int = 0
    ZERO_DELIVERY_FEE :int = 0
    MAX_DELIVERY_FEE :int = 50

    def get_delivery_flat_fee(self,base_amount :float) ->int:
        return self.MAX_DELIVERY_FEE\
            if base_amount < self.THRESHOLD_AMT_FOR_FREE_DELIVERY\
            else self.ZERO_DELIVERY_FEE