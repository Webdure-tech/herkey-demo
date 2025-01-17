""" This module provides functions to generate Agora RTC tokens. """
import time

from agora_token_builder import RtcTokenBuilder, RtmTokenBuilder
from django.conf import settings

def create_agora_rtc_token_publisher(channel_name, uid=None, role='host', expire_time=86400):
    """
    Generate an Agora RTC token with the given channel name, UID, role, and expiration time.
    """
    APP_ID = settings.AGORA_APP_ID
    APP_CERTIFICATE = settings.AGORA_APP_CERTIFICATE

    if not uid:
        uid = 0  # Default UID

    if not channel_name:
        raise ValueError("Channel name is required")

    # Get role
    if role == "host":
        role = 1
    else:
        role = 2

    # Calculate privilege expire time
    current_time = int(time.time())
    privilege_expire_time = current_time + expire_time

    # Generate the token
    token = RtcTokenBuilder.buildTokenWithUid(
        APP_ID, APP_CERTIFICATE, channel_name, uid, role, privilege_expire_time
    )

    return {
        "token": token,
        "channel_name": channel_name,
        "uid": uid,
        "role": role,
        "privilege_expire_time": privilege_expire_time,
    }

def create_agora_rtm_token_publisher(channel_name, uid=None, role='host', expire_time=86400):
    """
    Generate an Agora RTC token with the given channel name, UID, role, and expiration time.
    """
    APP_ID = settings.AGORA_APP_ID
    APP_CERTIFICATE = settings.AGORA_APP_CERTIFICATE

    if not uid:
        uid = 0  # Default UID

    if not channel_name:
        raise ValueError("Channel name is required")

    # Get role
    if role == "host":
        role = 1
    else:
        role = 2

    # Calculate privilege expire time
    current_time = int(time.time())
    privilege_expire_time = current_time + expire_time
    account = str(uid)
    # Generate the token
    token = RtmTokenBuilder.buildToken(
        APP_ID, APP_CERTIFICATE, account, role, privilege_expire_time
    )

    return {
        "token": token,
        "channel_name": channel_name,
        "uid": uid,
        "role": role,
        "privilege_expire_time": privilege_expire_time,
    }