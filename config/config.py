import codecs
import configparser

# Read the configuration file
with codecs.open('config/config.ini', 'r', encoding='utf-8') as f:
    configs = configparser.ConfigParser()
    configs.read_file(f)

bot_token = str(configs['credentials']['bot_token'])

bot_name = str(configs['customizations']['bot_name'])
bot_status = str(configs['customizations']['bot_status'])
eightball_footer = str(configs['customizations']['eightball_footer'])

command_prefix = str(configs['settings']['command_prefix'])
display_confirmation = configs.getboolean('settings', 'display_confirmation')
delete_confirmation = configs.getboolean('settings', 'delete_confirmation')
wait_time = int(configs['settings']['seconds_before_deleting_confirmation'])
reply = configs.getboolean('settings', 'reply')
delete_invocation = configs.getboolean('settings', 'delete_invocation')
