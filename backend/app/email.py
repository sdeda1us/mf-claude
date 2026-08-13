import logging

from app.config import settings

logger = logging.getLogger("megafantasy.email")


def send_magic_link(to_email: str, link: str) -> None:
    if not settings.resend_api_key:
        # Dev fallback: no email provider configured, log the link instead.
        logger.warning("RESEND_API_KEY not set — magic link for %s: %s", to_email, link)
        return

    import resend

    resend.api_key = settings.resend_api_key
    resend.Emails.send(
        {
            "from": settings.email_from,
            "to": [to_email],
            "subject": "Your Megafantasy login link",
            "html": (
                f"<p>Click below to log in to Megafantasy:</p>"
                f'<p><a href="{link}">{link}</a></p>'
                f"<p>This link expires in {settings.magic_link_ttl_minutes} minutes.</p>"
            ),
        }
    )
