import codecs
import configparser

# Read the configuration file
with codecs.open('config/config.ini', 'r', encoding='utf-8') as f:
    config = configparser.ConfigParser()
    config.read_file(f)

bot_token = str(config['credentials']['bot_token'])

bot_name = str(config['customizations']['bot_name'])
eightball_footer = str(config['customizations']['eightball_footer'])

command_prefix = str(config['settings']['command_prefix'])
delete_invocation = bool(config['settings']['delete_invocation'])
display_confirmation = bool(config['settings']['display_confirmation'])
delete_confirmation = bool(config['settings']['delete_confirmation'])
wait_secs = int(config['settings']['seconds_before_deleting_confirmation'])
reply = bool(config['settings']['reply'])
