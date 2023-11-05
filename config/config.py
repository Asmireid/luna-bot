import codecs
import configparser


def load_config():
    # Read the configuration file
    with codecs.open('config/config.ini', 'r', encoding='utf-8') as f:
        configurations = configparser.ConfigParser()
        configurations.read_file(f)
    return configurations


configs = load_config()
bot_token = configs['credentials']['bot_token']

bot_name = configs['customizations']['bot_name']
bot_activity = configs['customizations']['bot_activity']
embed_footer = configs['customizations']['embed_footer']

command_prefix = configs['settings']['command_prefix']
display_confirmation = configs.getboolean('settings', 'display_confirmation')
delete_confirmation = configs.getboolean('settings', 'delete_confirmation')
wait_time = configs.getint('settings', 'seconds_before_deleting_confirmation')
reply = configs.getboolean('settings', 'reply')
mention_author = configs.getboolean('settings', 'mention_author')
delete_invocation = configs.getboolean('settings', 'delete_invocation')
ephemeral = configs.getboolean('settings', 'ephemeral')
