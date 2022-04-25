from utilities import Taxes ,Fees ,PaymentGateway,PaymentMode

class PaymentProcessor:

    DEFAULT_NONE_PROCESSOR = None

    def __init__(self, amt, paymode) -> None:
        self._amt :float = amt
        self._paymode :PaymentMode = paymode
        self._total_payment_amt :float = 0

    def process_payment(self) -> None:
        self._total_payment_amt = self.calculate_total_payment_amount()
        pmt_gtwy  = PaymentGateway(self._total_payment_amt)
        pmt_gtwy.pay_by_payment_mode(self._paymode)

    def calculate_total_payment_amount(self) ->float:
        total_taxes :float = self._calculate_taxes(self._amt)
        total_fees :float = self._calculate_fees(self._amt)
        return round(self._amt + total_taxes + total_fees,2)

    @staticmethod
    def _calculate_taxes(base_amt :float) ->float:
        tax = Taxes()
        amt_CGST , amt_SGST , total_GST_amt  = tax.calculate_GST(base_amt)
        print(f"Calculated CGST at {tax.CGST*100}% is INR {amt_CGST}")
        print(f"Calculated SGST at {tax.SGST*100}% is INR {amt_SGST}")
        print(f"Total Tax = {total_GST_amt}")
        return total_GST_amt

    @staticmethod
    def _calculate_fees(base_amount : float) ->int:
        fee = Fees()
        delivery_flat_fee :int = fee.get_delivery_flat_fee(base_amount)
        print(f"Applicable Delivery Fee = {delivery_flat_fee}")
        return delivery_flat_fee

    def calculate_reverse_payment_amount(self) ->float:
        return self._total_payment_amt

    def reverse_payment(self) ->None:
        print(f"Payment for INR {self.calculate_reverse_payment_amount()} has been reversed to the original payment mode -- {self._paymode.value}")