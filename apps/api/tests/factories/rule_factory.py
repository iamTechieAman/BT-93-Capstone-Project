import uuid

from smart_gst.rates.models import TariffRateRule


class TariffRuleFactory:
    @staticmethod
    def build(
        hsn_code: str = "42031010",
        description: str = "Articles of apparel and clothing accessories, of leather",
        rate: float = 18.0,
        notification_no: str = "1/2017-Central Tax (Rate)",
        notification_date: str = "2017-06-28",
        schedule: str = "Schedule III",
        serial_no: str = "111",
        effective_from: str = "2017-07-01",
        source_url: str = "https://cbic-gst.gov.in/pdf/Notification1-CGST-Rate.pdf",
    ) -> TariffRateRule:
        return TariffRateRule(
            id=str(uuid.uuid4()),
            hsn_code=hsn_code,
            description=description,
            rate=rate,
            notification_no=notification_no,
            notification_date=notification_date,
            schedule=schedule,
            serial_no=serial_no,
            effective_from=effective_from,
            source_url=source_url,
        )

    @staticmethod
    def create(db, **kwargs) -> TariffRateRule:
        rule = TariffRuleFactory.build(**kwargs)
        db.add(rule)
        db.commit()
        db.refresh(rule)
        return rule
