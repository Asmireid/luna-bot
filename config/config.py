import configparser

# Read the configuration file
config = configparser.ConfigParser()
config.read("config/config.ini")
bot_token = str(config['credentials']['bot_token'])
command_prefix = str(config['settings']['command_prefix'])
delete_invocation = bool(config['settings']['delete_invocation'])
display_confirmation = bool(config['settings']['display_confirmation'])
delete_confirmation = bool(config['settings']['delete_confirmation'])
wait_secs = int(config['settings']['seconds_before_deleting_confirmation'])
reply = bool(config['settings']['reply'])
