from .localization import get_locale


def get_payment_method_details(lang: str, method: str) -> tuple[str, str]:
    """Return (method title, bank-specific requisites)
    method keys: pay_dc, pay_eskhata, pay_alif
    """
    L = get_locale(lang)
    # In a real application, these would be stored securely, not in code.
    BANKS = {
        'pay_dc': (L['pay_dc_btn'], '5536914096627215'),
        'pay_eskhata': (L['pay_eskhata_btn'], '2022 9197 0000 0000'),
        'pay_alif': (L['pay_alif_btn'], '3011 5910 0000 0000'),
        'pay_visa': (L['pay_visa_btn'], '5536914096627215'),
    }
    return BANKS.get(method, ("Unknown", "N/A"))
