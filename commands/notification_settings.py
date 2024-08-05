from discord.ext import commands
import json

@commands.hybrid_command(description="Change the setting about the notifications. -1 is for not getting any everyday. ")
async def notification_settings(ctx, notification_hour : int = -1, new_mayssage_notification : bool = False):
    user_settings = { str(ctx.message.author.id): {
         "id": str(ctx.message.author.id),
        "notification_time": -1 if notification_hour == -1 else notification_hour % 24,
        "new_message_notification": new_mayssage_notification
    } }

    json_content : str = "" # String containing the json

    try: # Check if the setting file exist
        settings = open("data/user_settings.json", "r")
    except FileNotFoundError: # If it does not, only add the new user settings to a new file
        json_content = json.dumps(user_settings)
    else: # If it does, get the json and add the new user settings to the file
        settings_json : dict = json.loads(settings.read())

        settings.close()

        settings_json.update(user_settings)

        json_content = json.dumps(settings_json)
    finally: # Update (or create and update) the file
        settings = open("data/user_settings.json", "w")
        settings.write(json_content)
        settings.close()


    await ctx.send(f"Settings set!\nCurrent settings:\nHour of notification: {("Never" if notification_hour == -1 else str(notification_hour % 24))}\nNotifications for new Mayssage: {("Enabled" if new_mayssage_notification else "Disabled" )}")